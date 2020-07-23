#!/usr/bin/env python3
import os
import sys
from os import path

url = sys.argv[1]
if url.startswith("postgresql"):
    from psycopg2 import connect

    filename = "postgresql.sql"
else:
    print("Unsupported database connection:", url, file=sys.stderr)
    os.exit(1)

sql_path = path.join(path.dirname(__file__), filename)

with open(sql_path) as f:
    sql = f.read()

with connect(url) as conn:
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
