"""
High level API for interacting with a Stormlock lock.

Classes:
    StormLock

Functions:
    load_lock
    parse_ttl
"""
import os
import re
from configparser import ConfigParser
from datetime import timedelta
from getpass import getuser
from socket import gethostname
from typing import Optional

from ._backend_config import backend_for_config
from .backend import Backend, Lease


class StormLock:
    """
    A lock on a single resource.

    This contains object allows you te perform operations such as acquire and release on
    the lock for a single resource, which is stored in a Stormlock backend.

    Typically, this will be created from config.

    Methods
    -------

    acquire(ttl=None):
        Acquire the lock
    release(lease_id):
        Release the lock (using the lease_id from acquire)
    renew(lease_id, ttl=None):
        Renew an acquired lease
    current():
        Get the currently active lease
    is_current(lease_id):
        Check if a lease is live
    """

    def __init__(self, backend: Backend, resource: str, principal: str, ttl: timedelta):
        """
        Create a new StormLock.

        Parameters:
            backend:
                The backend the lock is stored in
            resource:
                The name of the resource the lock is for
            principal:
                An identifier for the principal that is acting on the lock
                (such as an email address)
            ttl: The default time-to-live for a lease on the lock.
        """
        self._backend = backend
        self._resource = resource
        self._principal = principal
        self._ttl = ttl

    def acquire(self, ttl: Optional[timedelta] = None) -> str:
        """
        Attempt to acquire a lock on the resource.

        Parameters:
            ttl (optional):
                time-to-live for acquired lease. Overrides default.

        Returns:
            The lease ID for the acquired lease, if successful.

        Raises: backend.LockHeldException
            If the lock is currently held.
        """
        return self._backend.lock(self._resource, self._principal, ttl or self._ttl)

    def release(self, lease_id: str):
        """
        Release a lease on the resource.

        Parameters:
            lease_id:
                The id for a lease previously acquired with :method:`acquire`.

        NOTE: this operation is idempotent, and always succeeds, even if the lease id
        does not match the currently active lease, or there is no currently active
        lease.
        """
        self._backend.unlock(self._resource, lease_id)

    def renew(self, lease_id: str, ttl: Optional[timedelta] = None):
        """
        Attempt to renew a currently held lease.

        Parameters:
            lease_id:
                The id for a lease previously acquired with :method:`acquire`.
            ttl: optional
                A new time-to-live for the lease. This time is counted from the time of
                the renewal, *NOT* the time of the initial acquire. Defaults to using
                the ttl of the `StormLock` object.

        Raises: backend.LockExpiredException
            If the lease has expired, or has already been released.
        """
        self._backend.renew(self._resource, lease_id, ttl or self._ttl)

    def current(self) -> Optional[Lease]:
        """
        Returns a `Lease` object containing information about the currently active
        lease, or `None` if no lease is active.
        """
        return self._backend.current(self._resource)

    def is_current(self, lease_id: str) -> bool:
        """
        Test if the given lease is the currently active lease.

        Parameters:
            lease_id:
                The id for a leas previously acquired with :method:`acquire`.

        Returns:
            `True` if the id matches the active lease in the backend, `False` otherwise.
        """
        return self._backend.is_current(self._resource, lease_id)


_SEARCH_PATHS = [
    "./.stormlock.cfg",
    os.path.join(os.environ.get("XDG_CONFIG_HOME", "~/.config"), "stormlock.cfg"),
    "~/.stormlock.cfg",
]

_TTL_PAT = re.compile(r"^(\d+) *([a-z]+)$")


def _expand_unit(abbrev: str) -> str:
    for unit in ["days", "hours", "minutes", "seconds"]:
        if unit.startswith(abbrev):
            return unit
    raise ValueError(f"{abbrev} is not a valid unit")


def parse_ttl(ttl_str: str) -> timedelta:
    """
    Parse a time-to-live value from a string.

    Parameters:
        ttl_str:
            A sting in the format "*n* *unit*". Where *n* is a positive integer and
            *unit* is one of "days", "hours", "minutes", "seconds".

    Returns:
        A `datetime.timedelta` representing the time delta in the input string.
    """
    match = _TTL_PAT.match(ttl_str)
    if match is None:
        raise ValueError("Invalid TTL specification " + ttl_str)
    (val, unit) = match.groups()
    unit = _expand_unit(unit)
    kwargs = {unit: int(val)}
    return timedelta(**kwargs)


def _find_conf_file() -> str:
    if "STORMLOCK_CONFIG" in os.environ:
        return os.environ["STORMLOCK_CONFIG"]
    for path in _SEARCH_PATHS:
        if os.path.isfile(path):
            return path
    raise Exception("Unable to find stormlock configuration file")


def _get_cfg_value(cfg: ConfigParser, section: str, name: str) -> str:
    val = cfg.get(section, name, fallback=None) or cfg.get(
        "default", name, fallback=None
    )
    assert val, f"Unable to find configuration for {section}.{name}"
    return val


def load_lock(resource: str, conf_file: Optional[str] = None) -> StormLock:
    """
    Load a `StormLock` for a resource from a configuration file.

    Parameters:
        resource:
            The name of the resource the lock is for. The `StormLock` will
            be initialized with settings from either the section of the config file
            with either the resource name if it exists, or the default section.
        conf_file: optional
            If supplied, the path to a file to load config from. If unspecified,
            a config file is searched for in the following locations:
                - `./.stormlock.cfg`
                - `$XDG_CONFIG_HOME/stormlock.cfg` or `~/.config/stormlock.cfg`
                - `~/.stormlock.cfg`

    Returns:
        A new `StormLock` object.
    """
    if not conf_file:
        conf_file = _find_conf_file()
    cfg = ConfigParser()
    cfg.read(conf_file)
    principal = _get_cfg_value(cfg, resource, "principal")
    backend_type = _get_cfg_value(cfg, resource, "backend")
    ttl = parse_ttl(_get_cfg_value(cfg, resource, "ttl"))
    if not principal:
        principal = "@".join([getuser(), gethostname()])

    backend = backend_for_config(backend_type, cfg)
    return StormLock(backend, resource, principal, ttl)
