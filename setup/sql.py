#!/usr/bin/env python3
import sys
from os import path
from urllib.parse import urlparse

url = sys.argv[1]
if url.startswith("postgresql"):
    from psycopg import Connection, connect

    def connect_url(url: str) -> Connection:
        return connect(url)

    filename = "postgresql.sql"
elif url.startswith("mysql"):
    # ignore type errors here, because while the mysql and postgres connections
    # are mostly compatible, it  is hard to convince mypy of that
    from mysql.connector import MySQLConnection as Connection  # type: ignore
    from mysql.connector import connect  # type: ignore

    def connect_url(url: str) -> Connection:
        parts = urlparse(url)
        kwargs: dict = {
            "host": parts.hostname,
            "user": parts.username,
            "password": parts.password,
            "database": parts.path.lstrip("/"),
        }
        if parts.port:
            kwargs["port"] = parts.port
        print(kwargs)
        return connect(**kwargs)

    filename = "mysql.sql"
else:
    print("Unsupported database connection:", url, file=sys.stderr)
    sys.exit(1)

sql_path = path.join(path.dirname(__file__), filename)

with open(sql_path) as f:
    sql = f.read()

with connect_url(url) as conn:
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
