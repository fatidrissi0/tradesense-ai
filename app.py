import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db
from routes.auth import auth_bp
from routes.trading import trading_bp
from routes.payment import payment_bp
from routes.leaderboard import leaderboard_bp
from routes.market import market_bp
from routes.signals import signals_bp
from routes.admin import admin_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                    "https://tradesense-o0zzu1d2w-fatima-zahra-reghini-idrissis-projects.vercel.app",
                    "https://tradesense-ai.vercel.app",
                ]
            }
        },
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        supports_credentials=False,
    )

    JWTManager(app)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(trading_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(signals_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run()
