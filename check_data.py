import sqlite3
from datetime import datetime

conn = sqlite3.connect("tradesense.db")
cursor = conn.cursor()

print("=" * 60)
print("🔍 VÉRIFICATION DES DONNÉES")
print("=" * 60)

print("\n👥 TOUS LES UTILISATEURS:")
cursor.execute("SELECT id, username, email FROM user ORDER BY id")
users = cursor.fetchall()
for user in users:
    print(f"   ID {user[0]}: {user[1]} ({user[2]})")

print(f"\n   Total: {len(users)} utilisateurs")

print("\n🎯 CHALLENGES PAR UTILISATEUR:")
cursor.execute(
    """
    SELECT u.username, c.id, c.status, c.started_at,
           ROUND(((c.current_balance - c.initial_balance) / c.initial_balance) * 100, 2) as profit
    FROM user u
    LEFT JOIN challenge c ON u.id = c.user_id
    ORDER BY u.id
    """
)
for row in cursor.fetchall():
    if row[1]:
        print(
            f"   {row[0]}: Challenge #{row[1]} ({row[2]}) = {row[4]}% | Date: {row[3]}"
        )
    else:
        print(f"   {row[0]}: ❌ Aucun challenge")

now = datetime.now()
print(f"\n📅 CHALLENGES AU MOIS ACTUEL ({now.year}-{now.month:02d}):")
cursor.execute(
    """
    SELECT u.username, c.id, c.started_at,
           ROUND(((c.current_balance - c.initial_balance) / c.initial_balance) * 100, 2) as profit
    FROM user u
    JOIN challenge c ON u.id = c.user_id
    WHERE strftime('%Y-%m', c.started_at) = strftime('%Y-%m', 'now')
    ORDER BY profit DESC
    """
)
results = cursor.fetchall()

if results:
    print(f"   ✅ {len(results)} challenges trouvés:")
    for row in results:
        print(f"      {row[0]}: {row[3]}% (Challenge #{row[1]}, Date: {row[2]})")
else:
    print("   ❌ AUCUN challenge trouvé ce mois!")

print(f"\n🔢 VÉRIFICATION DES IDs:")
cursor.execute("SELECT MIN(id), MAX(id) FROM user")
min_id, max_id = cursor.fetchone()
print(f"   User IDs: de {min_id} à {max_id}")

cursor.execute("SELECT COUNT(DISTINCT user_id) FROM challenge")
users_with_challenges = cursor.fetchone()[0]
print(f"   Users avec challenges: {users_with_challenges}")

print(f"\n📝 ORIGINE DES USERS:")
cursor.execute("SELECT id, username, created_at FROM user ORDER BY created_at")
for row in cursor.fetchall():
    print(f"   ID {row[0]}: {row[1]} | Créé: {row[2]}")

conn.close()

print("\n" + "=" * 60)

