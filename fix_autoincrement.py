import sqlite3


def fix_autoincrement():
    conn = sqlite3.connect("tradesense.db")
    cursor = conn.cursor()

    tables = ["user", "challenge", "trade", "payment"]

    print("🔧 Correction des auto-increments...")

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'"
    )
    has_sqlite_sequence = cursor.fetchone() is not None

    for table in tables:
        cursor.execute(f"SELECT MAX(id) FROM {table}")
        max_id = cursor.fetchone()[0]

        if max_id is None:
            max_id = 0

        if has_sqlite_sequence:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
            cursor.execute(
                f"INSERT INTO sqlite_sequence (name, seq) VALUES ('{table}', {max_id})"
            )
            print(f"✅ {table}: prochain ID sera {max_id + 1}")
        else:
            print(
                f"ℹ️ {table}: sqlite_sequence absent, prochain ID sera géré par SQLite (>= {max_id + 1})"
            )

    conn.commit()
    conn.close()

    if has_sqlite_sequence:
        print("\n✅ Auto-increments corrigés!")
        print("Vous pouvez maintenant créer de nouveaux comptes.")
    else:
        print("\nℹ️ sqlite_sequence n'existe pas dans cette base.")
        print("   Pour les colonnes 'INTEGER PRIMARY KEY', SQLite choisit automatiquement")
        print("   un nouvel ID supérieur à tous les existants (ROWID).")


if __name__ == "__main__":
    fix_autoincrement()
