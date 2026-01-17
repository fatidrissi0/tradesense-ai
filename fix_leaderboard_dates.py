import sqlite3
from datetime import datetime, timedelta
import random


def fix_dates():
    conn = sqlite3.connect("tradesense.db")
    cursor = conn.cursor()

    now = datetime.now()

    cursor.execute("SELECT id FROM challenge")
    challenges = cursor.fetchall()

    for challenge in challenges:
        days_ago = random.randint(1, 7)
        date = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE challenge SET started_at = ? WHERE id = ?", (date, challenge[0])
        )

    cursor.execute("SELECT id FROM user")
    users = cursor.fetchall()

    for user in users:
        days_ago = random.randint(1, 10)
        date = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE user SET created_at = ? WHERE id = ?", (date, user[0])
        )

    cursor.execute("SELECT id FROM trade")
    trades = cursor.fetchall()

    for trade in trades:
        days_ago = random.randint(0, 6)
        date = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE trade SET timestamp = ? WHERE id = ?", (date, trade[0])
        )

    conn.commit()

    cursor.execute(
        """
        SELECT u.username,
               ROUND(((c.current_balance - c.initial_balance) / c.initial_balance) * 100, 2) as profit
        FROM user u
        JOIN challenge c ON u.id = c.user_id
        WHERE strftime('%Y-%m', c.started_at) = strftime('%Y-%m', 'now')
        ORDER BY profit DESC
        """
    )

    results = cursor.fetchall()
    print(f"✅ {len(results)} traders trouvés dans le leaderboard:")
    for username, profit in results:
        print(f"   - {username}: {profit}%")

    conn.close()


if __name__ == "__main__":
    fix_dates()

