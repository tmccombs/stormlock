from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from importlib import metadata
from typing import NamedTuple, Optional, Type


class Lease(NamedTuple):
    principal: str
    created: datetime
    id: str


class LockHeldException(Exception):
    """Exception indicating the lock is already held."""

    def __init__(self, resource: str, lease: Optional[Lease]):
        self.resource = resource
        self.lease = lease


class LockExpiredException(Exception):
    "Exception indicating the lock has expired."

    def __init__(self, resource: str):
        self.resource = resource


class Backend(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def lock(self, resource: str, principal: str, ttl: timedelta,) -> str:
        """
        Implementation of acquiring a lock.

        This should attempt to acquire a lock, if successful, return
        the id for the lease that was acquired.
        If the lock is already held, raises a LockContendedException
        """

    @abstractmethod
    def unlock(self, resource: str, lease_id: str):
        """
        Release a lock.

        It should release the lock for `resource` as long as the current lease
        id matches `lease_id`.
        """

    @abstractmethod
    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        """
        Attempt to renew the lease for a lock. This reset the expiration of the
        lease to the current time plus the ttl. Note that some backends
        (such as etcd) may ignore the ttl argument and simply extend the
        expiration by the original ttl.

        Raises a LockExpiredException if the lock has expired.
        """

    @abstractmethod
    def current(self, resource: str) -> Optional[Lease]:
        "Get the Lease for the current lock, if it exists"

    def is_current(self, resource: str, lease_id: str) -> bool:
        """
        Test if the given lease_id is the id for the currently active lock

        Default implementation uses `current`, but subclasses may override with
        a more efficient method.
        """
        curr = self.current(resource)
        if curr:
            return curr.id == lease_id
        return False


def find_backend(name: str) -> Type[Backend]:
    backends = metadata.entry_points()["stormlock.backends"]
    for backend in backends:
        if backend.name == name:
            return backend.load()
    raise ValueError(f"Unable to find stormlock backend for {name}")


def get_backend(name: str, **kwargs) -> Backend:
    "Instantiate a backend based on its name."
    backend = find_backend(name)
    return backend(**kwargs)
