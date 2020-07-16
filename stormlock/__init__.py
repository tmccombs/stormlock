"""
A centralized inter-process and inter-machine locking library.

Classes:
    StormLock
    Backend
    LockExpiredException
    LockHeldException

Functions:
    load_lock
    get_backend
"""
__version__ = "0.1.0"

from stormlock.backend import (
    Backend,
    LockExpiredException,
    LockHeldException,
    get_backend,
)
from stormlock.lock import StormLock, load_lock

__all__ = (
    "Backend",
    "get_backend",
    "load_lock",
    "LockExpiredException",
    "LockHeldException",
    "StormLock",
)
