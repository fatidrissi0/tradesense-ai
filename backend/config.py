import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-me')

    database_url = os.getenv('DATABASE_URL', 'sqlite:///tradesense.db')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    PLANS = {
        'starter': {'price': 200, 'balance': 5000, 'currency': 'DH'},
        'pro': {'price': 500, 'balance': 10000, 'currency': 'DH'},
        'elite': {'price': 1000, 'balance': 25000, 'currency': 'DH'}
    }

    MAX_DAILY_LOSS_PERCENT = 5
    MAX_TOTAL_LOSS_PERCENT = 10
    PROFIT_TARGET_PERCENT = 10

