import sqlite3


def import_database():
    print("📦 Import de database.sql dans tradesense.db...")

    with open("database.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn = sqlite3.connect("tradesense.db")
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        existing_tables = [row[0] for row in cursor.fetchall()]
        for table_name in existing_tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        cursor.executescript(sql_script)
        conn.commit()

        cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables_count = cursor.fetchone()[0]

        def count_rows(table_name: str) -> int:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]

        users_count = count_rows("user")
        challenges_count = count_rows("challenge")
        trades_count = count_rows("trade")

        print("✅ Import terminé!")
        print(f"   - Tables: {tables_count}")
        print(f"   - Utilisateurs: {users_count}")
        print(f"   - Challenges: {challenges_count}")
        print(f"   - Trades: {trades_count}")
    finally:
        conn.close()


if __name__ == "__main__":
    import_database()

