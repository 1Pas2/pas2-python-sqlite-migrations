# pas2-python-sqlite-migrations

Apply ordered SQLite schema migrations inside a savepoint.

Part of **Pas2 Polyglot** by [1Pas2](https://github.com/1Pas2): independent small projects in PHP, Python, Go and C#. No runtime dependencies outside the language standard library. Initial version: 0.1.0.

## Requirements and installation

Python 3.11+. Install a checkout using `python -m pip install .`. The import name is `pas2_sqlite_migrations`. PyPI publication was not performed.

## Example

```python
import pas2_sqlite_migrations as api
import sqlite3

with sqlite3.connect(":memory:") as connection:
    print(
        api.migrate(connection, [(1, ["CREATE TABLE demo (id INTEGER PRIMARY KEY)"])])
    )
```

## API and limits

migrate(connection,migrations) takes increasing (version,[SQL statements]) pairs and records versions in _pas2_migrations. A failed batch rolls back through a savepoint, preserving any outer transaction. SQL must be trusted application code and one statement per string; supported leading verbs are explicit schema/data operations. No checksums, concurrent migrator coordination or down migrations. Pass complete historical migrations and do not reuse the internal savepoint name.

## Tests and example

From the repository root:

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
python examples/basic.py
```

Tests use the standard library or a dependency-free executable check harness. A failing assertion exits nonzero. The example is self-contained and uses local in-memory or temporary data. CI runs the same checks on Linux. No registry releases, downloads, users or production deployments are claimed.

## Contributing

Open a focused issue or pull request with reproduction steps and a behavioral test. Run the commands above before submitting. Do not include credentials or private data in reports.

## Ecosystem

[Browse Pas2 projects](https://github.com/1Pas2?tab=repositories&q=pas2-). Each repository is usable independently. The earlier TypeScript series and this polyglot series have distinct repository names.

## License

[MIT](LICENSE) © 2026 1Pas2.

1Pas2
