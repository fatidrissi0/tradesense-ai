import sqlite3 
from datetime import datetime, timedelta 
import random 
 
def fix_dates(): 
    conn = sqlite3.connect('tradesense.db') 
    cursor = conn.cursor() 
     
    print("🔧 Correction des dates pour janvier 2026...") 
     
    # Date de base: maintenant 
    now = datetime.now() 
     
    # 1. Corriger les users (créés il y a 1-10 jours) 
    cursor.execute("SELECT id FROM user") 
    users = cursor.fetchall() 
    for user in users: 
        days_ago = random.randint(1, 10) 
        date = now - timedelta(days=days_ago) 
        cursor.execute( 
            "UPDATE user SET created_at = ? WHERE id = ?", 
            (date.strftime('%Y-%m-%d %H:%M:%S'), user[0]) 
        ) 
    print(f"✅ {len(users)} utilisateurs mis à jour") 
     
    # 2. Corriger les challenges (créés il y a 1-7 jours) 
    cursor.execute("SELECT id FROM challenge") 
    challenges = cursor.fetchall() 
    for challenge in challenges: 
        days_ago = random.randint(1, 7) 
        date = now - timedelta(days=days_ago) 
        cursor.execute( 
            "UPDATE challenge SET started_at = ? WHERE id = ?", 
            (date.strftime('%Y-%m-%d %H:%M:%S'), challenge[0]) 
        ) 
    print(f"✅ {len(challenges)} challenges mis à jour") 
     
    # 3. Corriger les trades (créés il y a 0-6 jours) 
    cursor.execute("SELECT id FROM trade") 
    trades = cursor.fetchall() 
    for trade in trades: 
        days_ago = random.randint(0, 6) 
        hours_ago = random.randint(0, 23) 
        date = now - timedelta(days=days_ago, hours=hours_ago) 
        cursor.execute( 
            "UPDATE trade SET timestamp = ? WHERE id = ?", 
            (date.strftime('%Y-%m-%d %H:%M:%S'), trade[0]) 
        ) 
    print(f"✅ {len(trades)} trades mis à jour") 
     
    # 4. Corriger les payments (créés il y a 1-7 jours) 
    cursor.execute("SELECT id FROM payment") 
    payments = cursor.fetchall() 
    for payment in payments: 
        days_ago = random.randint(1, 7) 
        date = now - timedelta(days=days_ago) 
        cursor.execute( 
            "UPDATE payment SET created_at = ? WHERE id = ?", 
            (date.strftime('%Y-%m-%d %H:%M:%S'), payment[0]) 
        ) 
    print(f"✅ {len(payments)} paiements mis à jour") 
     
    conn.commit() 
     
    # Vérification 
    print("\n📊 Vérification du leaderboard:") 
    cursor.execute(""" 
        SELECT u.username, 
               ROUND(((c.current_balance - c.initial_balance) / c.initial_balance) * 100, 2) as profit_percent 
        FROM user u 
        JOIN challenge c ON u.id = c.user_id 
        WHERE strftime('%Y-%m', c.started_at) = strftime('%Y-%m', 'now') 
        ORDER BY profit_percent DESC 
        LIMIT 10 
    """) 
     
    results = cursor.fetchall() 
    if results: 
        print(f"\n🏆 Top {len(results)} traders trouvés:") 
        for idx, (username, profit) in enumerate(results, 1): 
            print(f"   {idx}. {username}: {profit}%") 
    else: 
        print("❌ Aucun trader trouvé dans le leaderboard!") 
     
    conn.close() 
    print("\n✅ Correction terminée!") 
 
if __name__ == "__main__": 
    fix_dates() 
