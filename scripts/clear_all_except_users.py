"""Delete all database rows while preserving the users table.

Run from the project root: python scripts/clear_all_except_users.py
"""

from sqlalchemy import MetaData

from utils.db.database import engine


PRESERVED_TABLES = {"users"}


def main():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Delete dependent tables before their parents so foreign-key constraints hold.
    tables_to_clear = [
        table
        for table in reversed(metadata.sorted_tables)
        if table.name not in PRESERVED_TABLES
    ]

    with engine.begin() as connection:
        for table in tables_to_clear:
            result = connection.execute(table.delete())
            print(f"Cleared {result.rowcount} row(s) from {table.name}.")

    print("Done. The users table was preserved.")


if __name__ == "__main__":
    main()
