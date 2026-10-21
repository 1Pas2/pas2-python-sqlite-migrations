import unittest
import pas2_sqlite_migrations as api


class Tests(unittest.TestCase):
    def test_apply_and_repeat(self):
        import sqlite3

        with sqlite3.connect(":memory:") as c:
            m = [(1, ["CREATE TABLE demo (id INTEGER)"])]
            self.assertEqual(api.migrate(c, m), [1])
            self.assertEqual(api.migrate(c, m), [])

    def test_atomic_rollback(self):
        import sqlite3

        with sqlite3.connect(":memory:") as c:
            with self.assertRaises(sqlite3.Error):
                api.migrate(
                    c,
                    [
                        (
                            1,
                            [
                                "CREATE TABLE demo (id INTEGER)",
                                "INSERT INTO missing_table VALUES (1)",
                            ],
                        )
                    ],
                )
            self.assertIsNone(
                c.execute("SELECT name FROM sqlite_master WHERE name='demo'").fetchone()
            )

    def test_order_validation(self):
        import sqlite3

        with self.assertRaises(ValueError):
            api.migrate(
                sqlite3.connect(":memory:"),
                [(2, ["CREATE TABLE a(x)"]), (1, ["CREATE TABLE b(x)"])],
            )


if __name__ == "__main__":
    unittest.main()
