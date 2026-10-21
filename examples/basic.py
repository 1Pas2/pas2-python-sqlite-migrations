import pas2_sqlite_migrations as api
import sqlite3

with sqlite3.connect(":memory:") as connection:
    print(
        api.migrate(connection, [(1, ["CREATE TABLE demo (id INTEGER PRIMARY KEY)"])])
    )
