import argparse
from datetime import timedelta
import sys
from typing import Optional

from stormlock.backend import Lease, LockExpiredException, LockHeldException
from stormlock.lock import StormLock, load_lock, parse_ttl


def add_resource_command(
    subparsers,
    cmd: str,
    *,
    takes_lease: bool = False,
    takes_ttl: bool = False,
    help: Optional[str] = None
):
    parser = subparsers.add_parser(cmd, help=help)
    parser.add_argument("resource")
    if takes_lease:
        parser.add_argument("lease_id", help="Id of an acquired lease")
    if takes_ttl:
        parser.add_argument(
            "-t", "--ttl", type=parse_ttl, help="Override time to live for lease"
        )


def build_parser():
    parser = argparse.ArgumentParser(prog="stormlock")
    parser.add_argument("-c", "--config", help="config file")
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    add_resource_command(
        subparsers, "acquire", takes_ttl=True, help="attempt to acquire a lock"
    )
    add_resource_command(subparsers, "release", takes_lease=True, help="release a lock")
    add_resource_command(
        subparsers, "renew", takes_lease=True, takes_ttl=True, help="renew a lock"
    )
    add_resource_command(subparsers, "current", help="show currently held lock")
    add_resource_command(
        subparsers, "is-held", takes_lease=True, help="check if lease is still valid"
    )
    return parser


def print_lease(lease: Lease):
    print(lease.principal)
    print(lease.id)
    print(lease.created.isoformat(timespec="milliseconds"))


def message(msg):
    print(msg, file=sys.stderr)


def acquire(lock: StormLock, ttl: Optional[timedelta]):
    try:
        lease = lock.acquire(ttl)
        print(lease)
    except LockHeldException as e:
        message("Lock held")
        print_lease(e.lease)
        sys.exit(2)


def renew(lock: StormLock, lease: str, ttl: Optional[timedelta]):
    try:
        lock.renew(lease, ttl)
    except LockExpiredException:
        message("Lock expired")
        sys.exit(3)


def current(lock: StormLock):
    lease = lock.current()
    if lease:
        print_lease(lease)
    else:
        message("no lock held")
        sys.exit(1)


def run():
    parser = build_parser()

    args = parser.parse_args()

    lock = load_lock(args.resource, args.config)

    cmd = args.cmd
    if cmd == "acquire":
        acquire(lock, args.ttl)
    elif cmd == "release":
        lock.release(args.lease_id)
    elif cmd == "renew":
        renew(lock, args.lease_id, args.ttl)
    elif cmd == "current":
        current(lock)
