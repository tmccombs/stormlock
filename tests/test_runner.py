from configparser import ConfigParser
from datetime import timedelta
from time import sleep
import os
import sys

DAY=timedelta(days=1)

from stormlock import (
        backend_for_config, get_backend,
        LockHeldException, LockExpiredException)

backend_name = sys.argv[1]

base_dir = os.path.dirname(__file__)

config_file = f"{base_dir}/../example_config/{backend_name}.cfg"

cfg = ConfigParser()
if cfg.read(config_file):
    backend = backend_for_config(cfg)
else:
    backend = get_backend(backend_name)


def fail_lock(resource):
    try:
        backend.lock(resource, 'me too', timedelta(days=1))
        assert False, "successfully got contested lock"
    except LockHeldException as e:
        print(f"Lock for {e.resource} already held by "
              f"{e.principal} with {e.lease_id}")


# first clear the lock if it was left over from a previous run
current = backend.current('test1')
if current:
    backend.unlock('test1', current.id)

id1 = backend.lock('test1', 'me', DAY)
print(f"Locked test1 with {id1}")

assert backend.is_current('test1', id1)

current = backend.current('test1')
print("current=", current)
assert current.id == id1, "ids don't match"

fail_lock('test1')

backend.renew('test1', id1, DAY)

backend.unlock('test1', id1)

id2 = backend.lock('test1', 'me2', timedelta(seconds=4))
print(f"Reacquired lock with id {id2}")
sleep(2)
backend.renew('test1', id2, timedelta(seconds=4))

fail_lock('test1')

sleep(4)

try:
    backend.renew('test1', id2, timedelta(seconds=4))
    assert False, "successfully renewed expired lease"
except LockExpiredException:
    print("Lock was successfully expired")

assert not backend.is_current('test1', id2)
