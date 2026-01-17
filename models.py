from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    challenges = db.relationship('Challenge', backref='user', lazy=True)
    trades = db.relationship('Trade', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_type = db.Column(db.String(20), nullable=False)
    initial_balance = db.Column(db.Float, nullable=False)
    current_balance = db.Column(db.Float, nullable=False)
    daily_start_balance = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)
    profit_target = db.Column(db.Float, default=10.0, nullable=False)
    max_daily_loss_percent = db.Column(db.Float, default=5.0, nullable=False)
    max_total_loss_percent = db.Column(db.Float, default=10.0, nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=True)

    trades = db.relationship('Trade', backref='challenge', lazy=True)

    def to_dict(self):
        profit_percent = ((self.current_balance - self.initial_balance) / self.initial_balance * 100) if self.initial_balance else 0.0
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_type': self.plan_type,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'daily_start_balance': self.daily_start_balance,
            'status': self.status,
            'profit_target': self.profit_target,
            'max_daily_loss_percent': self.max_daily_loss_percent,
            'max_total_loss_percent': self.max_total_loss_percent,
            'started_at': self.started_at.isoformat(),
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'profit_percent': round(profit_percent, 2)
        }

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    profit_loss = db.Column(db.Float, default=0.0, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'action': self.action,
            'quantity': self.quantity,
            'price': self.price,
            'profit_loss': self.profit_loss,
            'timestamp': self.timestamp.isoformat()
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='DH', nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat()
        }

class PayPalConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paypal_client_id = db.Column(db.String(255), nullable=False)
    paypal_secret_hash = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_secret(self, paypal_secret):
        self.paypal_secret_hash = bcrypt.hashpw(
            paypal_secret.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'paypal_client_id': self.paypal_client_id,
            'updated_at': self.updated_at.isoformat()
        }
