"""
Interface for interacting with StormLock backends.

Classes:
    Backend
    LockHeldException
    LockExpiredException
    Lease

Functions:
    get_backend
    find_backend
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from importlib import metadata
from typing import NamedTuple, Optional, Type


class Lease(NamedTuple):
    """
    Representation of a leased lock.

    This contains information about a currently held lock, including
    who holds it, when it was acquired, and the id associated with the
    current lease.
    """

    principal: str
    """A description of the principal that currently holds the lock
    (ex. an email or user id)
    """
    created: datetime
    "The time the currently held lease was created."
    id: str
    "A unique identifier of the lease."


class LockHeldException(Exception):
    """
    Exception indicating the lock is already held.

    Properties:
        resource:
            The name of the resource the lock is for
        lease:
            A `Lease` containing information about the currently active lease.
            In some cases, this may be `None` if the backend is unable to determine
            the currently held lease or the lock was released between the attempted
            acquisition and retrieving the active lease (on some backends this is
            impossible).
    """

    def __init__(self, resource: str, lease: Optional[Lease]):
        super().__init__()
        self.resource = resource
        self.lease = lease


class LockExpiredException(Exception):
    """
    Exception indicating the lease on a lock has expired.

    Properties:
        resource:
            The name of the resource the lock is for
    """

    def __init__(self, resource: str):
        super().__init__()
        self.resource = resource


class Backend(ABC):
    """
    An abstract class that all stormlock backends should extend.

    The backend defines how locks are acquired and released in some kind of data store.

    Methods in this class take some or all of the following parameters:

    resource:
        The name of a resource to lock. This should be incorporated into the key
        used to store the lock state in the underlying data store of the backend.
        This is required for any operation on the lock.
    principal:
        An unique identifier for the principal, such as a user, service, machine etc.
        that acquired or is acquiring a lease. Basically, something to identify who
        is currently holding the lock.
    lease_id:
        An opaque identifier for a lease on a held lock. Each backend is free to use
        a representation that is convenient for identifying individual leases. Most
        operations on existing leases require this in order to ensure the lock is still
        held.
    ttl:
        A "time to live", or maximum age of a lease. Every lease has an expiration
        associated with it. If the lease expires, the lock is automatically released. A
        lease can be renewed to extend it's lifetime.  This effectively adds the TTL to
        the current time to get the new expiration time.  Most backends will use the TTL
        passed to the `renew` method, but some (such as etcd) may use TTL set when
        acquiring the lock. Check the documentation for the backend you are using.

    Methods:
        lock(resource, principal, ttl):
            Attempt to acquire a lease on the lock for a resource with a principal
            (e.g. user) with a time-to-live after which the lease is automatically
            released.
        unlock(resource, lease_id):
            Release a lease on the lock for a resource.
        renew(resource, lease_id, ttl):
            Attempt to renew a lease.
        current(resource):
            Get the current lease.
        is_current(resource, lease_id):
            Check if a lease is currently active.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        The `__init__` method of a backend should take keyword arguments that come from
        the stormlock config file.

        Each argument should be annotated with either the expected type.
        Supported types are:
            - `str` and `Optional[str]`
            - `int` and `Optional[int]`
            - `bool`
        """

    @abstractmethod
    def lock(self, resource: str, principal: str, ttl: timedelta,) -> str:
        """
        Implementation of acquiring a lock.

        This should attempt to acquire a lock, if successful, return
        the id for the lease that was acquired.
        If the lock is already held, raises a `LockContendedException`
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

        Raises a `LockExpiredException` if the lock has expired.
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
    "Find the Backend class associated with a name using package metadata."
    backends = metadata.entry_points()["stormlock.backends"]
    for backend in backends:
        if backend.name == name:
            return backend.load()
    raise ValueError(f"Unable to find stormlock backend for {name}")


def get_backend(name: str, **kwargs) -> Backend:
    "Instantiate a backend based on its name."
    backend = find_backend(name)
    return backend(**kwargs)
