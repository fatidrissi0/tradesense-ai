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

    CORS(app, resources={r"/api/*": {"origins": "*" }},
    supports_credentials=True)

    # ✅ Preflight OPTIONS handler (CRUCIAL)
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({"message": "preflight ok"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
            return response, 200

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
