__version__ = '0.1.0'

from stormlock.backend import (
        Backend, get_backend, LockHeldException, LockExpiredException)
from stormlock.config import backend_for_config

__all__ = (
    'Backend',
    'backend_for_config',
    'get_backend',
    'LockHeldException',
    'LockExpiredException'
)
