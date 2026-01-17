from flask import Blueprint, jsonify
from sqlalchemy import func
from datetime import datetime
from models import db, User, Challenge, Trade

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/api/leaderboard/monthly', methods=['GET'])
def get_monthly_leaderboard():
    """Classement mensuel par profit en pourcentage basé sur Challenge"""
    try:
        current_month = f"{datetime.now().month:02d}"
        current_year = str(datetime.now().year)

        # Calculer le profit % à partir des balances des challenges du mois courant
        profit_percent_expr = (
            ((Challenge.current_balance - Challenge.initial_balance) / Challenge.initial_balance) * 100.0
        )

        leaderboard_query = db.session.query(
            User.username.label('username'),
            func.round(func.avg(profit_percent_expr), 2).label('avg_profit_percent'),
            func.count(Trade.id).label('total_trades')
        ).join(
            Challenge, Challenge.user_id == User.id
        ).outerjoin(
            Trade, Trade.challenge_id == Challenge.id
        ).filter(
            func.strftime('%m', Challenge.started_at) == current_month,
            func.strftime('%Y', Challenge.started_at) == current_year
        ).group_by(
            User.id,
            User.username
        ).order_by(
            func.avg(profit_percent_expr).desc()
        ).limit(10)

        results = leaderboard_query.all()

        leaderboard = []
        for rank, row in enumerate(results, start=1):
            username = row.username
            avg_profit_percent = float(row.avg_profit_percent or 0)
            total_trades = int(row.total_trades or 0)
            leaderboard.append({
                'rank': rank,
                'username': username,
                'profit_percent': avg_profit_percent,
                'avg_profit_percent': avg_profit_percent,
                'total_trades': total_trades
            })

        return jsonify(leaderboard), 200

    except Exception:
        return jsonify({'error': 'Erreur lors de la récupération du classement'}), 500
