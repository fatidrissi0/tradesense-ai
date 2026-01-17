import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_fallback')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///tradesense.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key_fallback')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    PLANS = {
        'starter': {'price': 200, 'balance': 5000, 'currency': 'DH'},
        'pro': {'price': 500, 'balance': 10000, 'currency': 'DH'},
        'elite': {'price': 1000, 'balance': 25000, 'currency': 'DH'}
    }

    MAX_DAILY_LOSS_PERCENT = 5
    MAX_TOTAL_LOSS_PERCENT = 10
    PROFIT_TARGET_PERCENT = 10

PLANS = Config.PLANS
MAX_DAILY_LOSS_PERCENT = Config.MAX_DAILY_LOSS_PERCENT
MAX_TOTAL_LOSS_PERCENT = Config.MAX_TOTAL_LOSS_PERCENT
PROFIT_TARGET_PERCENT = Config.PROFIT_TARGET_PERCENT

# Configuration environments
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
