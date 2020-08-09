#!/usr/bin/env python3
import os
import sys
from os import path
from urllib.parse import urlparse

url = sys.argv[1]
if url.startswith("postgresql"):
    from psycopg2 import connect as connect_url

    filename = "postgresql.sql"
elif url.startswith("mysql"):
    from mysql.connector import connect

    def connect_url(url):
        parts = urlparse(url)
        kwargs = {
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
    os.exit(1)

sql_path = path.join(path.dirname(__file__), filename)

with open(sql_path) as f:
    sql = f.read()

with connect_url(url) as conn:
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
