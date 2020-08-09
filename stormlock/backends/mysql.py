"Mysql backend"
import contextlib
import secrets
from datetime import timedelta
from typing import Optional

from mysql.connector import connect  # type: ignore
from stormlock.backend import Backend, Lease, LockExpiredException, LockHeldException


class MySql(Backend):
    "Stormlock backend that uses mysql (or compatible) as a data store."

    def __init__(self, table: str = "stormlock", **settings):
        super().__init__()
        self._conn = connect(**settings)
        self._table = table

    def lock(self, resource: str, principal: str, ttl: timedelta) -> str:
        lease_id = secrets.token_bytes(16)
        lease_tok = lease_id.hex().upper()
        args = {
            "res": resource,
            "princ": principal,
            "lease": lease_id,
            "ttl": ttl,
        }
        with self._transaction() as cur:
            # mysql doesn't have any way to atomically upsert with a condition,
            # so we have to try updating, and if that fails, try inserting.
            cur.execute(
                f"""UPDATE {self._table} SET lease=%(lease)s,
                    principal=%(princ)s, created=NOW(),
                    expires=DATE_ADD(NOW(), INTERVAL %(ttl)s HOUR_SECOND)
                    WHERE resource=%(res)s AND expires < NOW()""",
                args,
            )
            if cur.rowcount == 1:
                return lease_tok

            # update failed, try inserting instead
            cur.execute(
                f"""INSERT IGNORE INTO {self._table}
                    (resource, lease, principal, created, expires)
                    VALUES (%(res)s, %(lease)s, %(princ)s, NOW(),
                    DATE_ADD(NOW(), INTERVAL %(ttl)s HOUR_SECOND))""",
                args,
            )

            if cur.rowcount == 1:
                return lease_tok

            current = self.current(resource)
            self._conn.rollback()
            raise LockHeldException(resource, current)

    def unlock(self, resource: str, lease_id: str):
        with self._transaction() as cur:
            cur.execute(
                f"""DELETE FROM {self._table} WHERE resource=%s AND lease=%s""",
                (resource, bytes.fromhex(lease_id)),
            )

    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        with self._transaction() as cur:
            cur.execute(
                f"""UPDATE {self._table} SET
                    expires = DATE_ADD(NOW(), INTERVAL %(ttl)s HOUR_SECOND)
                    WHERE resource=%(res)s AND lease=%(lease)s AND expires > NOW()""",
                {"res": resource, "lease": bytes.fromhex(lease_id), "ttl": ttl},
            )
            if cur.rowcount < 1:
                raise LockExpiredException(resource)

    def current(self, resource: str) -> Optional[Lease]:
        with self._transaction() as cur:
            cur.execute(
                f"""SELECT principal, created, UPPER(HEX(lease)) FROM {self._table}
                    WHERE resource=%s AND expires > NOW()""",
                (resource,),
            )
            row = cur.fetchone()
            return row and Lease(*row)

    def is_current(self, resource: str, lease_id: str) -> bool:
        with self._transaction() as cur:
            cur.execute(
                f"""SELECT COUNT(lease) FROM {self._table} WHERE
                    resource=%s AND expires > NOW() AND lease=%s""",
                (resource, bytes.fromhex(lease_id)),
            )
            return cur.fetchone()[0]

    @contextlib.contextmanager
    def _transaction(self):
        cur = self._conn.cursor()
        try:
            yield cur
            self._conn.commit()
        except Exception as err:
            self._conn.rollback()
            raise err
        finally:
            cur.close()
