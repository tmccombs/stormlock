import os
import sys
from datetime import timedelta
from time import sleep

from stormlock import LockExpiredException, LockHeldException, load_lock

resource_name = sys.argv[1]

base_dir = os.path.dirname(__file__)

config_file = f"{base_dir}/stormlock.cfg"

lock = load_lock(f"{resource_name}_test", config_file)


def fail_lock():
    try:
        lock.acquire()
        assert False, "successfully got contested lock"
    except LockHeldException as e:
        print(
            f"Lock for {e.resource} already held by " f"{e.principal} with {e.lease.id}"
        )


# first clear the lock if it was left over from a previous run
current = lock.current()
if current:
    lock.release(current.id)

id1 = lock.acquire()
print(f"Locked test1 with {id1}")

assert lock.is_current(id1)

current = lock.current()
print("current=", current)
assert current is not None and current.id == id1, "ids don't match"

fail_lock()

lock.renew(id1)

lock.release(id1)

id2 = lock.acquire(timedelta(seconds=4))
print(f"Reacquired lock with id {id2}")
sleep(2)
lock.renew(id2, timedelta(seconds=4))

fail_lock()

sleep(4)

try:
    lock.renew(id2, timedelta(seconds=4))
    assert False, "successfully renewed expired lease"
except LockExpiredException:
    print("Lock was successfully expired")

assert not lock.is_current(id2)
