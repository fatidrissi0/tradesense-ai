from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import db, User
from datetime import datetime
import uuid
import logging
from flask import current_app

logging.basicConfig(level=logging.DEBUG)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Username, email et password requis'}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        if len(password) < 6:
            return jsonify({'error': 'Le mot de passe doit contenir au moins 6 caractères'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Nom d\'utilisateur déjà utilisé'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email déjà utilisé'}), 400
        
        user = User(
            username=username,
            email=email,
            role='user',
            is_active=True,
            created_at=datetime.utcnow()
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.exception("Erreur register")
        return jsonify({'error': 'Erreur lors de l\'inscription'}), 400

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email et password requis'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Email ou mot de passe invalide'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Compte désactivé'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
            
    except Exception as e: 
        current_app.logger.exception("Erreur login")
        return jsonify({'error': 'Erreur lors de la connexion'}), 400


@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.exception("Erreur register")
        return jsonify({'error': 'Erreur lors de l\'inscription'}), 400

@auth_bp.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        return jsonify({
            'message': 'Déconnexion réussie'
        }), 200
    except Exception as e:
        current_app.logger.exception("Erreur register")
        return jsonify({'error': 'Erreur lors de l\'inscription'}), 400
