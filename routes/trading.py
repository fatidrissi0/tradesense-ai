from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Challenge, Trade
from datetime import datetime
from config import Config

trading_bp = Blueprint('trading', __name__)

def check_challenge_rules(challenge):
    """Vérifie les règles du challenge et retourne le statut"""
    
    # 1. Vérifier si le profit target est atteint
    profit_percent = ((challenge.current_balance - challenge.initial_balance) / challenge.initial_balance) * 100
    if profit_percent >= challenge.profit_target:
        challenge.status = 'passed'
        challenge.ended_at = datetime.utcnow()
        return {'status': 'passed', 'reason': 'Profit target reached!'}
    
    # 2. Vérifier si la perte totale maximale est dépassée
    total_loss_percent = ((challenge.initial_balance - challenge.current_balance) / challenge.initial_balance) * 100
    if total_loss_percent >= challenge.max_total_loss_percent:
        challenge.status = 'failed'
        challenge.ended_at = datetime.utcnow()
        return {'status': 'failed', 'reason': 'Max total loss exceeded'}
    
    # 3. Vérifier si la perte journalière maximale est dépassée
    daily_loss_percent = ((challenge.daily_start_balance - challenge.current_balance) / challenge.daily_start_balance) * 100
    if daily_loss_percent >= challenge.max_daily_loss_percent:
        challenge.status = 'failed'
        challenge.ended_at = datetime.utcnow()
        return {'status': 'failed', 'reason': 'Max daily loss exceeded'}
    
    return {'status': 'active'}

@trading_bp.route('/api/challenges/active', methods=['GET'])
@jwt_required()
def get_active_challenge():
    """Récupère le challenge actif de l'utilisateur"""
    try:
        user_id = get_jwt_identity()
        
        challenge = Challenge.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if not challenge:
            return jsonify({'error': 'Aucun challenge actif trouvé'}), 404
        
        return jsonify({
            'challenge': challenge.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération du challenge'}), 400

@trading_bp.route('/api/trades/execute', methods=['POST'])
@jwt_required()
def execute_trade():
    """Exécute un trade et met à jour le challenge"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('symbol') or not data.get('action') or not data.get('quantity') or not data.get('price'):
            return jsonify({'error': 'Symbol, action, quantity et price requis'}), 400
        
        symbol = data['symbol'].upper()
        action = data['action'].lower()
        quantity = float(data['quantity'])
        price = float(data['price'])
        
        if action not in ['buy', 'sell']:
            return jsonify({'error': 'Action doit être buy ou sell'}), 400
        
        if quantity <= 0 or price <= 0:
            return jsonify({'error': 'Quantity et price doivent être positifs'}), 400
        
        # Trouver le challenge actif
        challenge = Challenge.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if not challenge:
            return jsonify({'error': 'Aucun challenge actif trouvé'}), 404
        
        # Calculer la valeur du trade
        trade_value = quantity * price
        profit_loss = 0.0
        
        # Mettre à jour le solde du challenge
        if action == 'buy':
            if challenge.current_balance < trade_value:
                return jsonify({'error': 'Solde insuffisant'}), 400
            challenge.current_balance -= trade_value
        else:  # sell
            challenge.current_balance += trade_value
            # Pour un sell, on considère que le profit/loss est la différence avec le prix d'achat moyen
            # Dans une implémentation réelle, vous auriez besoin de suivre le prix d'achat moyen
            profit_loss = 0.0  # À implémenter selon votre logique de trading
        
        # Créer le trade record
        trade = Trade(
            challenge_id=challenge.id,
            user_id=user_id,
            symbol=symbol,
            action=action,
            quantity=quantity,
            price=price,
            profit_loss=profit_loss,
            timestamp=datetime.utcnow()
        )
        
        db.session.add(trade)
        
        # Vérifier les règles du challenge
        rule_check = check_challenge_rules(challenge)
        
        db.session.commit()
        
        return jsonify({
            'trade': trade.to_dict(),
            'challenge': challenge.to_dict(),
            'rule_check': rule_check
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Valeurs invalides'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de l\'exécution du trade'}), 400

@trading_bp.route('/api/trades/history', methods=['GET'])
@jwt_required()
def get_trade_history():
    """Récupère l'historique des trades de l'utilisateur"""
    try:
        user_id = get_jwt_identity()
        
        trades = Trade.query.filter_by(user_id=user_id).order_by(
            Trade.timestamp.desc()
        ).all()
        
        return jsonify({
            'trades': [trade.to_dict() for trade in trades]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération de l\'historique'}), 400