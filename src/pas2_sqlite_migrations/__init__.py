import sqlite3


def migrate(
    connection: sqlite3.Connection, migrations: list[tuple[int, list[str]]]
) -> list[int]:
    ids = [version for version, _ in migrations]
    if any(type(v) is not int or v < 1 for v in ids) or ids != sorted(set(ids)):
        raise ValueError("Migration IDs must be positive, unique and increasing")
    for _, statements in migrations:
        if not statements:
            raise ValueError("Migration cannot be empty")
        for sql in statements:
            first = (
                sql.lstrip().split(None, 1)[0].rstrip(";").upper()
                if sql.strip()
                else ""
            )
            if first not in {
                "CREATE",
                "ALTER",
                "DROP",
                "INSERT",
                "UPDATE",
                "DELETE",
                "REPLACE",
            }:
                raise ValueError("Only explicit schema/data statements are supported")
    connection.execute("SAVEPOINT pas2_migrate")
    try:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS _pas2_migrations (version INTEGER PRIMARY KEY)"
        )
        applied = {
            row[0] for row in connection.execute("SELECT version FROM _pas2_migrations")
        }
        if applied - set(ids):
            raise ValueError("Migration history contains unknown versions")
        if applied and any(v not in applied and v < max(applied) for v in ids):
            raise ValueError("Cannot insert historical migrations")
        added = []
        for version, statements in migrations:
            if version in applied:
                continue
            for statement in statements:
                connection.execute(statement)
            connection.execute("INSERT INTO _pas2_migrations VALUES (?)", (version,))
            added.append(version)
        connection.execute("RELEASE pas2_migrate")
        return added
    except BaseException:
        connection.execute("ROLLBACK TO pas2_migrate")
        connection.execute("RELEASE pas2_migrate")
        raise
