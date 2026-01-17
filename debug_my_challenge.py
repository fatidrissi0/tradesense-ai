import sqlite3


def debug_my_challenge(username):
    conn = sqlite3.connect("instance/tradesense.db")
    cursor = conn.cursor()

    print("=" * 60)
    print(f"🔍 DEBUG POUR: {username}")
    print("=" * 60)

    cursor.execute(
        "SELECT id, username, email FROM user WHERE username = ?", (username,)
    )
    user = cursor.fetchone()

    if not user:
        print(f"❌ User '{username}' non trouvé!")
        return

    user_id, username, email = user
    print(f"\n👤 USER:")
    print(f"   ID: {user_id}")
    print(f"   Username: {username}")
    print(f"   Email: {email}")

    print(f"\n🎯 CHALLENGES:")
    cursor.execute(
        """
        SELECT id, plan_type, initial_balance, current_balance, status, started_at
        FROM challenge
        WHERE user_id = ?
        """,
        (user_id,),
    )

    challenges = cursor.fetchall()
    if not challenges:
        print("   ❌ Aucun challenge trouvé!")
        conn.close()
        return

    for ch_id, plan, initial, current, status, started in challenges:
        profit = ((current - initial) / initial) * 100 if initial and initial > 0 else 0
        print(f"\n   Challenge #{ch_id}:")
        print(f"      Plan: {plan}")
        print(f"      Initial: {initial} DH")
        print(f"      Current: {current} DH")
        print(f"      Profit: {profit:.2f}%")
        print(f"      Status: {status}")
        print(f"      Started: {started}")

    print(f"\n📈 TRADES:")
    cursor.execute(
        """
        SELECT id, challenge_id, symbol, action, quantity, price, profit_loss, timestamp
        FROM trade
        WHERE user_id = ?
        ORDER BY timestamp
        """,
        (user_id,),
    )

    trades = cursor.fetchall()
    if not trades:
        print("   ❌ Aucun trade trouvé!")
    else:
        for t_id, ch_id, symbol, action, qty, price, pl, ts in trades:
            print(f"   Trade #{t_id}: {action.upper()} {qty} {symbol} @ {price} DH")
            print(f"      Challenge: #{ch_id} | P/L: {pl} | Date: {ts}")

    print(f"\n🏆 DANS LE LEADERBOARD:")
    cursor.execute(
        """
        SELECT
            ROUND(AVG(((c.current_balance - c.initial_balance) / c.initial_balance) * 100), 2) as avg_profit
        FROM challenge c
        WHERE c.user_id = ?
          AND strftime('%Y-%m', c.started_at) = strftime('%Y-%m', 'now')
        """,
        (user_id,),
    )

    result = cursor.fetchone()
    leaderboard_profit = result[0] if result and result[0] is not None else 0.0
    print(f"   Profit affiché: {leaderboard_profit}%")

    if leaderboard_profit == 0.0 and challenges:
        print("\n⚠️  PROBLÈME DÉTECTÉ:")
        print("   - Vous avez des challenges")
        if trades:
            print("   - Vous avez des trades")
        print("   - Mais profit = 0.00%")
        print("\n💡 CAUSE POSSIBLE:")
        print("   - current_balance n'a pas été mis à jour après les trades")
        print("   - OU tous vos trades sont des BUY sans SELL")

    conn.close()


if __name__ == "__main__":
    username = input("Entrez votre username: ")
    debug_my_challenge(username)

