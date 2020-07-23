"Postgresql backend"
from datetime import timedelta
from typing import Optional
from uuid import uuid4

import psycopg2  # type: ignore

from stormlock.backend import Backend, Lease, LockExpiredException, LockHeldException


class Postgresql(Backend):
    "Stormlock backend that uses postgresql as a data store."

    def __init__(self, connection: str, table: str = "stormlock"):
        super().__init__()
        self._conn = psycopg2.connect(connection)
        self._conn.autocommit = True
        self._table = table

    def lock(self, resource: str, principal: str, ttl: timedelta):
        lease_id = str(uuid4())
        cur = self._conn.cursor()
        try:
            cur.execute(
                f"""
                INSERT INTO {self._table} as t
                (resource, lease, principal, expires) VALUES
                (%(resource)s, %(lease)s, %(principal)s,
                    current_timestamp+%(ttl)s)
                ON CONFLICT (resource) DO UPDATE
                SET (lease, principal, created, expires) =
                (excluded.lease, excluded.principal,
                    DEFAULT, current_timestamp+%(ttl)s)
                WHERE t.expires < excluded.created
                """,
                {
                    "resource": resource,
                    "lease": lease_id,
                    "principal": principal,
                    "ttl": ttl,
                },
            )
            if cur.rowcount == 1:
                return str(lease_id)
            raise LockHeldException(resource, self.current(resource))
        finally:
            cur.close()

    def unlock(self, resource: str, lease_id: str):
        cur = self._conn.cursor()
        try:
            cur.execute(
                f"""
                DELETE FROM {self._table} WHERE resource = %s AND lease = %s
                """,
                (resource, lease_id),
            )
        finally:
            cur.close()

    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        cur = self._conn.cursor()
        try:
            cur.execute(
                f"""
                UPDATE {self._table} SET expires = current_timestamp + %s
                WHERE resource=%s AND lease=%s
                    AND expires > current_timestamp
                """,
                (ttl, resource, lease_id),
            )
            if cur.rowcount < 1:
                raise LockExpiredException(resource)
        finally:
            cur.close()

    def current(self, resource: str) -> Optional[Lease]:
        cur = self._conn.cursor()
        try:
            cur.execute(
                f"""
                SELECT principal, created, lease FROM {self._table}
                WHERE resource = %s AND expires > current_timestamp""",
                (resource,),
            )
            row = cur.fetchone()
            return row and Lease(*row)
        finally:
            cur.close()

    def is_current(self, resource: str, lease_id: str) -> bool:
        cur = self._conn.cursor()
        try:
            cur.execute(
                f"""
                SELECT count(lease) FROM {self._table}
                WHERE resource = %s AND expires > current_timestamp
                AND lease = %s""",
                (resource, lease_id),
            )
            return cur.fetchone()[0]
        finally:
            cur.close()
