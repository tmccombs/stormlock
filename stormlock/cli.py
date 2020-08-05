"""
Module that implements the actual CLI executable for stormlock.
"""

import argparse
import json
import sys
from datetime import timedelta
from typing import Optional

from stormlock.backend import Lease, LockExpiredException, LockHeldException
from stormlock.lock import StormLock, load_lock, parse_ttl


def _add_resource_command(
    subparsers,
    cmd: str,
    *,
    takes_lease: bool = False,
    takes_ttl: bool = False,
    helpmsg: Optional[str] = None,
) -> argparse.ArgumentParser:
    "Add a subcommand to the parser that takes a resource"
    parser = subparsers.add_parser(cmd, help=helpmsg)
    parser.add_argument("resource")
    if takes_lease:
        parser.add_argument("lease_id", help="Id of an acquired lease")
    if takes_ttl:
        parser.add_argument(
            "-t", "--ttl", type=parse_ttl, help="Override time to live for lease"
        )
    return parser


def _build_parser():
    "Create the argument parser"
    parser = argparse.ArgumentParser(prog="stormlock")
    parser.add_argument("-c", "--config", help="config file")
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    _add_resource_command(
        subparsers, "acquire", takes_ttl=True, helpmsg="attempt to acquire a lock"
    )
    _add_resource_command(
        subparsers, "release", takes_lease=True, helpmsg="release a lock"
    )
    _add_resource_command(
        subparsers, "renew", takes_lease=True, takes_ttl=True, helpmsg="renew a lock"
    )
    current_cmd = _add_resource_command(
        subparsers, "current", helpmsg="show currently held lock"
    )
    current_cmd.add_argument(
        "-f",
        "--format",
        choices=["id", "json", "lines", "oneline", "cols", "rows"],
        default="rows",
        help="format to print lease info",
    )
    current_cmd.add_argument(
        "--id-only",
        action="store_const",
        const="id",
        dest="format",
        help="equivalent to --format=id",
    )
    _add_resource_command(
        subparsers, "is-held", takes_lease=True, helpmsg="check if lease is still valid"
    )
    return parser


def print_lease(lease: Lease, fmt: str):
    "Print the information for an active lease."

    def timestamp():
        return lease.created.isoformat(timespec="milliseconds")

    def print_delimited(delim: str):
        print(delim.join([lease.principal, timestamp(), lease.id]))

    if fmt == "id":
        print(lease.id)
    elif fmt == "rows":
        print(f"Principal: {lease.principal}")
        print(f"Created: {timestamp()}")
        print(f"Id: {lease.id}")
    elif fmt == "oneline":
        print_delimited("\t")
    elif fmt == "lines":
        print_delimited("\n")
    elif fmt == "json":
        json.dump(
            {"id": lease.id, "created": timestamp(), "principal": lease.principal},
            sys.stdout,
        )
    elif fmt == "cols":
        fields = [lease.principal, timestamp(), lease.id]
        width = max(map(len, fields)) + 4
        print("{:{w}}{:{w}}{:{w}}".format("PRINCIPAL", "CREATED", "ID", w=width))
        print("{:{w}}{:{w}}{:{w}}".format(*fields, w=width))


def _message(msg):
    print(msg, file=sys.stderr)


def acquire(lock: StormLock, ttl: Optional[timedelta]):
    "attempt to acquire a lock"
    # TODO: add support for retries
    try:
        lease = lock.acquire(ttl)
        print(lease)
    except LockHeldException as exc:
        _message("Lock held")
        if exc.lease:
            print_lease(exc.lease, "id")
        else:
            _message("Held lock not found, try again?")
        sys.exit(2)


def renew(lock: StormLock, lease: str, ttl: Optional[timedelta]):
    "attempt to renew a lock"
    try:
        lock.renew(lease, ttl)
    except LockExpiredException:
        _message("Lock expired")
        sys.exit(3)


def current(lock: StormLock, fmt: str):
    "get the currently held lock"
    lease = lock.current()
    if lease:
        print_lease(lease, fmt)
    else:
        _message("no lock held")
        sys.exit(1)


def is_held(lock: StormLock, lease: str):
    "test if the lease is currently active"
    if not lock.is_current(lease):
        sys.exit(1)


def run():
    "run the CLI program"
    parser = _build_parser()

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
        current(lock, args.format)
    elif cmd == "is-held":
        is_held(lock, args.lease_id)
