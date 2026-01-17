import os
import sqlite3
import glob


def find_databases():
    print("=" * 60)
    print("🔍 RECHERCHE DES BASES DE DONNÉES")
    print("=" * 60)

    print("\n📝 Configuration dans config.py:")
    try:
        with open("config.py", "r") as f:
            for line in f:
                if "DATABASE" in line.upper() or "SQLALCHEMY" in line:
                    print(f"   {line.strip()}")
    except FileNotFoundError:
        print("   ⚠️  config.py non trouvé")

    print("\n🔍 Fichiers .db trouvés:")
    db_files = []

    for db_file in glob.glob("*.db"):
        db_files.append(db_file)

    for db_file in glob.glob("instance/*.db"):
        db_files.append(db_file)

    for db_file in glob.glob("backend/*.db"):
        db_files.append(db_file)

    if not db_files:
        print("   ❌ Aucun fichier .db trouvé!")
        return

    for db_path in db_files:
        print(f"\n{'='*60}")
        print(f"📦 Base: {db_path}")
        print(f"{'='*60}")

        if not os.path.exists(db_path):
            print("   ❌ Fichier inexistant")
            continue

        size = os.path.getsize(db_path)
        print(f"   Taille: {size} bytes")

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='user'"
            )
            if not cursor.fetchone():
                print("   ⚠️  Table 'user' n'existe pas")
                conn.close()
                continue

            cursor.execute("SELECT COUNT(*) FROM user")
            count = cursor.fetchone()[0]
            print(f"   👥 Utilisateurs: {count}")

            if count > 0:
                cursor.execute("SELECT id, username, email FROM user ORDER BY id")
                print("   📋 Liste:")
                for user_id, username, email in cursor.fetchall():
                    print(f"      ID {user_id}: {username} ({email})")

            cursor.execute("SELECT COUNT(*) FROM challenge")
            challenges = cursor.fetchone()[0]
            print(f"   🎯 Challenges: {challenges}")

            conn.close()

        except Exception as e:
            print(f"   ❌ Erreur: {e}")

    print("\n" + "=" * 60)
    print("💡 SOLUTION:")
    print("   Flask utilise probablement la base avec VOS 10+ utilisateurs")
    print("   Supprimez cette base et gardez tradesense.db")
    print("=" * 60)


if __name__ == "__main__":
    find_databases()

