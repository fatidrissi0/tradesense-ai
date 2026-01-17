from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Challenge, Payment, PayPalConfig
from datetime import datetime
from config import Config
import time
import uuid

payment_bp = Blueprint('payment', __name__)

PLAN_FEATURES = {
    'starter': [
        '5000 DH balance',
        'Accès aux signaux IA',
        'Tableau de bord basique',
        'Support par email'
    ],
    'pro': [
        '10000 DH balance',
        'Accès aux signaux IA avancés',
        'Tableau de bord avancé',
        'Support prioritaire',
        'Analyse de performance détaillée'
    ],
    'elite': [
        '25000 DH balance',
        'Accès complet aux signaux IA',
        'Tableau de bord premium',
        'Support VIP 24/7',
        'Analyse de performance premium',
        'Accès anticipé aux nouvelles fonctionnalités'
    ]
}

@payment_bp.route('/api/payment/plans', methods=['GET'])
def get_plans():
    """Retourne les 3 plans disponibles avec leurs caractéristiques"""
    try:
        plans = {}
        for plan_type, plan_data in Config.PLANS.items():
            plans[plan_type] = {
                'price': plan_data['price'],
                'balance': plan_data['balance'],
                'currency': plan_data['currency'],
                'features': PLAN_FEATURES.get(plan_type, []),
                'popular': plan_type == 'pro'
            }
        return jsonify({'plans': plans}), 200
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération des plans'}), 400

@payment_bp.route('/api/payment/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """Simule un paiement et crée un challenge actif"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data or not data.get('plan_type') or not data.get('payment_method'):
            return jsonify({'error': 'Plan type et payment method requis'}), 400
        
        plan_type = data['plan_type'].lower()
        payment_method = data['payment_method'].lower()
        
        if plan_type not in Config.PLANS:
            return jsonify({'error': 'Plan type invalide'}), 400
        
        valid_methods = ['cmi', 'crypto', 'paypal']
        if payment_method not in valid_methods:
            return jsonify({'error': 'Méthode de paiement invalide'}), 400
        
        # Simulation d'un délai de traitement de paiement
        time.sleep(2)
        
        # Générer un ID de transaction unique
        transaction_id = str(uuid.uuid4())
        plan_data = Config.PLANS[plan_type]
        
        # Créer le payment record
        payment = Payment(
            user_id=user_id,
            amount=plan_data['price'],
            currency=plan_data['currency'],
            payment_method=payment_method,
            status='completed',
            transaction_id=transaction_id,
            created_at=datetime.utcnow()
        )
        
        # Créer le challenge actif
        challenge = Challenge(
            user_id=user_id,
            plan_type=plan_type,
            initial_balance=plan_data['balance'],
            current_balance=plan_data['balance'],
            daily_start_balance=plan_data['balance'],
            status='active',
            profit_target=Config.PROFIT_TARGET_PERCENT,
            max_daily_loss_percent=Config.MAX_DAILY_LOSS_PERCENT,
            max_total_loss_percent=Config.MAX_TOTAL_LOSS_PERCENT,
            started_at=datetime.utcnow()
        )
        
        db.session.add(payment)
        db.session.add(challenge)
        db.session.commit()
        
        return jsonify({
            'payment': payment.to_dict(),
            'challenge': challenge.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors du traitement du paiement'}), 400

@payment_bp.route('/api/payment/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    """Récupère l'historique des paiements de l'utilisateur"""
    try:
        user_id = get_jwt_identity()
        
        payments = Payment.query.filter_by(user_id=user_id).order_by(
            Payment.created_at.desc()
        ).all()
        
        return jsonify({
            'payments': [payment.to_dict() for payment in payments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération de l\'historique'}), 400

@payment_bp.route('/api/admin/paypal/config', methods=['POST'])
@jwt_required()
def configure_paypal():
    """Configure les credentials PayPal (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'superadmin':
            return jsonify({'error': 'Accès non autorisé'}), 403
        
        data = request.get_json()
        if not data or not data.get('paypal_client_id') or not data.get('paypal_secret'):
            return jsonify({'error': 'PayPal client ID et secret requis'}), 400
        
        paypal_client_id = data['paypal_client_id']
        paypal_secret = data['paypal_secret']
        
        # Vérifier s'il existe déjà une configuration PayPal
        config_entry = PayPalConfig.query.first()
        if config_entry:
            # Mettre à jour la configuration existante
            config_entry.paypal_client_id = paypal_client_id
            config_entry.set_secret(paypal_secret)
        else:
            # Créer une nouvelle configuration
            config_entry = PayPalConfig(paypal_client_id=paypal_client_id)
            config_entry.set_secret(paypal_secret)
            db.session.add(config_entry)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Configuration PayPal mise à jour avec succès',
            'config': config_entry.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la configuration PayPal'}), 400
