from datetime import datetime, timedelta
import struct
import time
from typing import Optional

import etcd3
from etcd3.client import KVMetadata

from stormlock.backend import Backend, Lease, LockHeldException, LockExpiredException


class _Keys:
    prefix: bytes
    principal: bytes
    created: bytes
    end: bytes

    def __init__(self, key: str):
        self.prefix = key.encode()
        self.token = self.prefix + b"/id"
        self.principal = self.prefix + b"/p"
        self.created = self.prefix + b"/c"

    @property
    def end(self) -> bytes:
        return self.prefix + b"\xff"


def _prefix_end(key):
    return key + b"\xff"


def _parse_lease(keys: _Keys, response: [(bytes, KVMetadata)]) -> Optional[Lease]:
    token = None
    for (value, meta) in response:
        if meta.key == keys.token:
            token = value.decode()
        elif meta.key == keys.principal:
            principal = value.decode()
        elif meta.key == keys.created:
            created = datetime.fromtimestamp(struct.unpack("d", value)[0])
    return token and Lease(principal, created, token)


class Etcd(Backend):
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
        self._prefix = prefix
        self._client = etcd3.client(
            host, port, ca_cert, cert_key, cert_cert, timeout, user, password,
        )

    def lock(self, resource: str, principal: str, ttl: timedelta) -> str:
        keys = _Keys(self._prefix + resource)
        tr = self._client.transactions
        lease = self._client.lease(int(ttl.total_seconds()))
        token = format(lease.id, "x")
        created = time.time()

        success, responses = self._client.transaction(
            compare=[tr.create(keys.token) == 0],
            success=[
                tr.put(keys.token, token, lease),
                tr.put(keys.principal, principal.encode(), lease),
                tr.put(keys.created, struct.pack("d", created), lease),
            ],
            failure=[tr.get(keys.prefix, range_end=keys.end)],
        )
        if success:
            return token
        if not success:
            raise LockHeldException(resource, _parse_lease(keys, responses[0]))

    def unlock(self, resource: str, lease_id: str):
        # It's an etcd lease, so just release it
        self._client.revoke_lease(int(lease_id, 16))

    def renew(self, resource: str, lease_id: str, ttl: timedelta) -> bool:
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
