from configparser import ConfigParser
from datetime import timedelta
from getpass import getuser
import os
from socket import gethostname
from typing import Optional

from .backend import Backend, Lease
from ._backend_config import backend_for_config


class StormLock:
    def __init__(self, backend: Backend, resource: str, principal: str, ttl: timedelta):
        self._backend = backend
        self._resource = resource
        self._principal = principal
        self._ttl = ttl

    def acquire(self, ttl: Optional[timedelta] = None) -> str:
        return self._backend.lock(self._resource, self._principal, ttl or self._ttl)

    def release(self, lease_id: str):
        self._backend.unlock(self._resource, lease_id)

    def renew(self, lease_id: str, ttl: Optional[timedelta] = None):
        self._backend.renew(self._resource, lease_id, ttl or self._ttl)

    def current(self) -> Optional[Lease]:
        return self._backend.current(self._resource)

    def is_current(self, lease_id: str) -> bool:
        return self._backend.is_current(self._resource, lease_id)


_SEARCH_PATHS = [
    "./.stormlock.cfg",
    os.path.join(os.environ.get("XDG_CONFIG_HOME", "~/.config"), "stormlock.cfg"),
    "~/.stormlock.cfg",
]


def parse_ttl(ttl_str: str) -> timedelta:
    (val, unit) = ttl_str.split(" ")
    kwargs = {unit: int(val)}
    return timedelta(**kwargs)


def _find_conf_file() -> str:
    for path in _SEARCH_PATHS:
        if os.path.isfile(path):
            return path
    raise Exception("Unable to find stormlock configuration file")


def _get_cfg_value(cfg: ConfigParser, section: str, name: str) -> Optional[str]:
    return cfg.get(section, name, fallback=None) or cfg.get(
        "default", name, fallback=None
    )


def load_lock(resource: str, conf_file: Optional[str]) -> StormLock:
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
