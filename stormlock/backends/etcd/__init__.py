"Etcd backend"
import struct
import time
from collections.abc import Iterable
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import grpc

from stormlock.backend import Backend, Lease, LockExpiredException, LockHeldException

# pylint: disable=no-name-in-module
from .proto.kv_pb2 import KeyValue

# pylint: disable=no-name-in-module
from .proto.rpc_pb2 import (
    AuthenticateRequest,
    Compare,
    LeaseGrantRequest,
    LeaseKeepAliveRequest,
    LeaseRevokeRequest,
    PutRequest,
    RangeRequest,
    RequestOp,
    TxnRequest,
)
from .proto.rpc_pb2_grpc import AuthStub, KVStub, LeaseStub


# pylint: disable=R0903
class _Keys:
    prefix: bytes
    "prefix at beginning of all keys"
    principal: bytes
    "key for the principal"
    created: bytes
    "key for the created timestamp"
    token: bytes
    "key for the unique token for the lease"

    def __init__(self, key: str):
        super().__init__()
        self.prefix = key.encode()
        self.token = self.prefix + b"/id"
        self.principal = self.prefix + b"/p"
        self.created = self.prefix + b"/c"

    @property
    def end(self) -> bytes:
        "key to use as the end of a range for all keys for the lease"
        # this could be more sophisticated, but we always use a "/"
        # and "0" comes after "/"
        return self.prefix + b"0"

    @property
    def start(self) -> bytes:
        "key to use as the beginnig of a range for all keys for the lease"
        return self.prefix + b"/"


def _parse_lease(keys: _Keys, kvs: Iterable[KeyValue]) -> Optional[Lease]:
    token = None
    for kv in kvs:
        if kv.key == keys.token:
            token = kv.value.decode()
        elif kv.key == keys.principal:
            principal = kv.value.decode()
        elif kv.key == keys.created:
            created = datetime.fromtimestamp(struct.unpack("d", kv.value)[0])
    if token:
        return Lease(principal, created, token)
    return None


def _get_chan_creds(
    ca_cert: str, cert_key: Optional[str] = None, cert_cert: Optional[str] = None
):
    "Get credentials for connection with TLS"
    private_key = None
    client_cert = None
    with open(ca_cert, "rb") as f:
        root_cert = f.read()
    if cert_key:
        with open(cert_key, "rb") as f:
            private_key = f.read()

    if cert_cert:
        with open(cert_cert, "rb") as f:
            client_cert = f.read()
    return grpc.ssl_channel_credentials(root_cert, private_key, client_cert)


class TokenMetadataPlugin(grpc.AuthMetadataPlugin):
    "AuthMetadataToken that just returns the input token"

    def __init__(self, token: str):
        self.token = token

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        callback: grpc.AuthMetadataPluginCallback,
    ):
        metadata = (("token", self.token),)
        callback(metadata, None)


class Etcd(Backend):
    """
    Stormlock backend that uses Etcd as a data store.

    Note that renewing ignores the supplied ttl.
    """

    _creds: Optional[grpc.CallCredentials]

    def __init__(
        self,
        *,
        prefix: str = "/",
        host: str = "localhost",
        port: int = 2379,
        ca_cert: Optional[str] = None,
        cert_key: Optional[str] = None,
        cert_cert: Optional[str] = None,
        timeout: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        super().__init__()

        target = f"{host}:{port}"
        if ca_cert is not None:
            chan_creds = _get_chan_creds(ca_cert, cert_key, cert_cert)
            self._channel = grpc.secure_channel(target, chan_creds)
            self.secure = True
        else:
            self._channel = grpc.insecure_channel(target)
            self.secure = False

        auth = AuthStub(self._channel)

        if user is not None or password is not None:
            if not self.secure:
                raise ValueError("Username and password not supported without SSL")
            token = auth.Authenticate(
                AuthenticateRequest(name=user, password=password)
            ).token
            # Although the etcd docs suggest creating a new channel to
            # include the creds in the channel, we just store the creds,
            # and include them in each request
            self._creds = grpc.metadata_call_credentials(TokenMetadataPlugin(token))
        else:
            self._creds = None

        self._kv = KVStub(self._channel)
        self._lease = LeaseStub(self._channel)
        self.prefix = prefix
        self._args = {
            "timeout": timeout,
            "credentials": self._creds,
        }

    def lock(self, resource: str, principal: str, ttl: timedelta) -> str:
        keys = _Keys(self.prefix + resource)
        lease = self._lease.LeaseGrant(
            LeaseGrantRequest(TTL=int(ttl.total_seconds())), **self._args
        ).ID
        token = format(lease, "x")
        created = time.time()

        txn = TxnRequest(
            compare=[
                Compare(
                    key=keys.token,
                    result=Compare.CompareResult.EQUAL,
                    target=Compare.CompareTarget.CREATE,
                    create_revision=0,
                )
            ],
            success=[
                RequestOp(
                    request_put=PutRequest(
                        key=keys.token, value=token.encode(), lease=lease
                    )
                ),
                RequestOp(
                    request_put=PutRequest(
                        key=keys.principal, value=principal.encode(), lease=lease
                    )
                ),
                RequestOp(
                    request_put=PutRequest(
                        key=keys.created, value=struct.pack("d", created), lease=lease
                    )
                ),
            ],
            failure=[
                RequestOp(
                    request_range=RangeRequest(key=keys.start, range_end=keys.end)
                )
            ],
        )
        resp = self._kv.Txn(txn)
        if resp.succeeded:
            return token
        range_resp = resp.responses[0].response_range
        held_lease = _parse_lease(keys, range_resp.kvs)
        assert held_lease, "Unable to find held lease after failing to acquire lease"
        raise LockHeldException(resource, held_lease)

    def unlock(self, resource: str, lease_id: str):
        # It's an etcd lease, so just release it
        self._lease.LeaseRevoke(LeaseRevokeRequest(ID=int(lease_id, 16)), **self._args)

    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        # Just send a single keep-alive over a stream
        req = LeaseKeepAliveRequest(ID=int(lease_id, 16))
        resp = next(self._lease.LeaseKeepAlive(iter([req]), **self._args))
        if resp.TTL <= 0:
            raise LockExpiredException(resource)

    def current(self, resource: str):
        keys = _Keys(self.prefix + resource)
        data = self._kv.Range(
            RangeRequest(
                key=keys.start,
                range_end=keys.end,
            ),
            **self._args,
        )
        # Do we need to handle pagination here?
        return _parse_lease(keys, data.kvs)

    def is_current(self, resource: str, lease_id: str) -> bool:
        key = (self.prefix + resource + "/id").encode()
        resp = self._kv.Range(RangeRequest(key=key), **self._args)
        if resp.count < 1:
            return False
        kv = resp.kvs.pop()
        return kv.value == lease_id.encode()
