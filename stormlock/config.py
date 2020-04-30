from configparser import ConfigParser
from inspect import signature, Signature, Parameter
import typing
from typing import Optional

from .backend import find_backend


def _read_parameter(param: Parameter, cfg: ConfigParser):
    be_conf = cfg['backend']
    backend_type = be_conf['type']
    annot = param.annotation

    if annot == dict or annot == Optional[dict]:
        section_name = '{}.{}'.format(backend_type, param.name)
        if section_name in cfg:
            return dict(cfg[section_name])
        else:
            return param.default
    if param.name in be_conf:
        if annot == str or annot == Optional[str] or annot == Parameter.emtpy:
            return be_conf[param.name]
        if annot == int or annot == Optional[int]:
            return cfg.getint('backend', param.name)
        if annot == bool:
            return cfg.getboolean('backend', param.name)
        assert False, f"Unable to parse config for {annot}"
    else:
        return param.default


def _config_for_signature(cfg: ConfigParser, sig: Signature) -> dict:
    used_keys = set('type')
    kwargs = {}
    for param in sig.parameters.values():
        if param.kind == Parameter.VAR_KEYWORD:
            for (k, v) in cfg['backend'].items():
                if k not in used_keys:
                    kwargs[k] = v
        elif param.kind != Parameter.VAR_POSITIONAL:
            used_keys.add(param.name)
            val = _read_parameter(param, cfg)
            # for now assume it is a keyword parameter
            if val != Parameter.empty:
                kwargs[param.name] = val
    return kwargs


def backend_for_config(cfg: ConfigParser):
    '''Load a backend from configuration'''
    Backend = find_backend(cfg['backend']['type'])
    kwargs = _config_for_signature(cfg, signature(Backend))
    return Backend(**kwargs)
