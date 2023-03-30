"Postgresql backend"
from datetime import timedelta
from typing import Optional
from uuid import uuid4

import psycopg

from stormlock.backend import Backend, Lease, LockExpiredException, LockHeldException


class Postgresql(Backend):
    "Stormlock backend that uses postgresql as a data store."

    def __init__(self, connection: str, table: str = "stormlock"):
        super().__init__()
        self._conn = psycopg.connect(connection)
        self._conn.autocommit = True
        self._table = table

    def lock(self, resource: str, principal: str, ttl: timedelta):
        lease_id = str(uuid4())
        with self._conn.cursor() as cur:
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

    def unlock(self, resource: str, lease_id: str):
        with self._conn.cursor() as cur:
            cur.execute(
                f"""
                DELETE FROM {self._table} WHERE resource = %s AND lease = %s
                """,
                (resource, lease_id),
            )

    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        with self._conn.cursor() as cur:
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

    def current(self, resource: str) -> Optional[Lease]:
        with self._conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT principal, created, lease FROM {self._table}
                WHERE resource = %s AND expires > current_timestamp""",
                (resource,),
            )
            row = cur.fetchone()
            if row:
                principal, created, _id = row
                return Lease(principal, created, str(_id))
            return None

    def is_current(self, resource: str, lease_id: str) -> bool:
        with self._conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT count(lease) FROM {self._table}
                WHERE resource = %s AND expires > current_timestamp
                AND lease = %s""",
                (resource, lease_id),
            )
            row = cur.fetchone()
            if row:
                return row[0] > 0
            return False

    def close(self):
        self._conn.close()
