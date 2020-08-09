"Load a backend from configuration"
import contextlib
from configparser import ConfigParser
from inspect import Parameter, Signature, signature
from typing import Any, Dict, Optional, Set

from .backend import find_backend


def _read_parameter(param: Parameter, cfg: ConfigParser, section: str):
    be_conf = cfg[section]
    annot = param.annotation

    if annot in (dict, Optional[dict]):
        section_name = "{}.{}".format(section, param.name)
        if section_name in cfg:
            return dict(cfg[section_name])
        return param.default
    if param.name in be_conf:
        if annot in (str, Optional[str], Parameter.empty):
            return be_conf[param.name]
        if annot in (int, Optional[int]):
            return cfg.getint(section, param.name)
        if annot == bool:
            return cfg.getboolean(section, param.name)
        raise AssertionError(f"Unable to parse config for {annot}")
    return param.default


def _parse_arg(arg: str):
    if arg in ["true", "True"]:
        return True
    if arg in ["false", "False"]:
        return False
    with contextlib.suppress(ValueError):
        return int(arg)
    return arg


def _config_for_signature(cfg: ConfigParser, section: str, sig: Signature) -> dict:
    kwargs: Dict[str, Any] = {}
    if section not in cfg:
        return kwargs
    used_keys: Set[str] = set()
    for param in sig.parameters.values():
        if param.kind == Parameter.VAR_KEYWORD:
            for (k, val) in cfg[section].items():
                if k not in used_keys:
                    kwargs[k] = _parse_arg(val)
        elif param.kind != Parameter.VAR_POSITIONAL:
            used_keys.add(param.name)
            val = _read_parameter(param, cfg, section)
            # for now assume it is a keyword parameter
            if val != Parameter.empty:
                kwargs[param.name] = val
    return kwargs


def backend_for_config(backend_type: str, cfg: ConfigParser):
    """Load a backend from configuration"""
    backend = find_backend(backend_type)
    section = "backend." + backend_type
    kwargs = _config_for_signature(cfg, section, signature(backend))
    return backend(**kwargs)
