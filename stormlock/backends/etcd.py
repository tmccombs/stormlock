"Etcd backend"
import struct
import time
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

# TODO: add type stubs for etcd
import etcd3  # type: ignore
from etcd3.client import KVMetadata  # type: ignore

from stormlock.backend import Backend, Lease, LockExpiredException, LockHeldException


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
        return self.prefix + b"\xff"


def _prefix_end(key):
    return key + b"\xff"


def _parse_lease(
    keys: _Keys, response: List[Tuple[bytes, KVMetadata]]
) -> Optional[Lease]:
    token = None
    for (value, meta) in response:
        if meta.key == keys.token:
            token = value.decode()
        elif meta.key == keys.principal:
            principal = value.decode()
        elif meta.key == keys.created:
            created = datetime.fromtimestamp(struct.unpack("d", value)[0])
    if token:
        return Lease(principal, created, token)
    return None


class Etcd(Backend):
    """
    Stormlock backend that uses Etcd as a data store.

    Note that renewing ignores the supplied ttl.
    """

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
        self._prefix = prefix
        self._client = etcd3.client(
            host, port, ca_cert, cert_key, cert_cert, timeout, user, password,
        )

    def lock(self, resource: str, principal: str, ttl: timedelta) -> str:
        keys = _Keys(self._prefix + resource)
        trans = self._client.transactions
        lease = self._client.lease(int(ttl.total_seconds()))
        token = format(lease.id, "x")
        created = time.time()

        success, responses = self._client.transaction(
            compare=[trans.create(keys.token) == 0],
            success=[
                trans.put(keys.token, token, lease),
                trans.put(keys.principal, principal.encode(), lease),
                trans.put(keys.created, struct.pack("d", created), lease),
            ],
            failure=[trans.get(keys.prefix, range_end=keys.end)],
        )
        if success:
            return token
        held_lease = _parse_lease(keys, responses[0])
        assert held_lease, "Unable to find held lease after failing to acquire lease"
        raise LockHeldException(resource, held_lease)

    def unlock(self, resource: str, lease_id: str):
        # It's an etcd lease, so just release it
        self._client.revoke_lease(int(lease_id, 16))

    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        resp = next(self._client.refresh_lease(int(lease_id, 16)))
        if resp.TTL <= 0:
            raise LockExpiredException(resource)

    def current(self, resource: str):
        keys = _Keys(self._prefix + resource)
        data = self._client.get_prefix(keys.prefix)
        return _parse_lease(keys, data)

    def is_current(self, resource: str, lease_id: str) -> bool:
        key = self._prefix + resource + "/id"
        current_id, _ = self._client.get(key)
        return current_id == lease_id.encode()
