"Redis backend"
import secrets
import time
from datetime import datetime, timedelta
from functools import cached_property
from typing import Optional

import redis

from stormlock.backend import Backend, Lease, LockExpiredException, LockHeldException

_LUA_ACQUIRE_SCRIPT = """
local lock = redis.call('hmget', KEYS[1], 'id', 'p', 'c')
if not lock[1] then
    redis.call('hmset', KEYS[1],
        'id', ARGV[1], 'p', ARGV[2], 'c', ARGV[3])
    redis.call('expire', KEYS[1], ARGV[4])
    return false
else
    return lock
end
"""

_LUA_RELEASE_SCRIPT = """
local token = redis.call('hget', KEYS[1], 'id')
if token == ARGV[1] then
    return redis.call('del', KEYS[1])
end
"""

_LUA_RENEW_SCRIPT = """
local id = redis.call('hget', KEYS[1], 'id')
if id == ARGV[1] then
    redis.call('expire', KEYS[1], ARGV[2])
    return true
else
    return false
end
"""


def _parse_lock(lock_data) -> Lease:
    (lease_id, princ, created) = lock_data
    return Lease(princ.decode(), datetime.fromtimestamp(float(created)), lease_id.hex())


class Redis(Backend):
    """
    Stormlock backend that uses Redis as a data store.
    """

    def __init__(
        self,
        *,
        url: str = "redis://localhost:6379",
        # TODO: SSL options
    ):
        super().__init__()
        self._client = redis.Redis.from_url(url, max_connections=1,)

    @cached_property
    def _acquire(self):
        return self._client.register_script(_LUA_ACQUIRE_SCRIPT)

    @cached_property
    def _release(self):
        return self._client.register_script(_LUA_RELEASE_SCRIPT)

    @cached_property
    def _renew(self):
        return self._client.register_script(_LUA_RENEW_SCRIPT)

    def lock(
        self, resource: str, principal: str, ttl: timedelta,
    ):
        token = secrets.token_bytes(16)
        args = [token, principal, time.time(), int(ttl.total_seconds())]
        contending_lock = self._acquire(keys=[resource], args=args)
        if contending_lock:
            lease = _parse_lock(contending_lock)
            raise LockHeldException(resource, lease)
        return token.hex()

    def unlock(self, resource: str, lease_id: str):
        token = bytes.fromhex(lease_id)
        self._release(keys=[resource], args=[token])

    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        token = bytes.fromhex(lease_id)
        ttl_secs = int(ttl.total_seconds())
        if not self._renew(keys=[resource], args=[token, ttl_secs]):
            raise LockExpiredException(resource)

    def current(self, resource: str) -> Optional[Lease]:
        data = self._client.hmget(resource, "id", "p", "c")
        if data[0]:
            return _parse_lock(data)
        return None

    def is_current(self, resource: str, lease_id: str):
        token = bytes.fromhex(lease_id)
        return token == self._client.hget(resource, "id")
