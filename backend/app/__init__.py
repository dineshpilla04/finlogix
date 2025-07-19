from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Update CORS to allow specific origins for frontend and deployed URLs
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": [
                "http://localhost:3000",
                "https://localhost:3000",
                "http://finlogix-e0jc.onrender.com",
                "https://finlogix-e0jc.onrender.com"
            ]
        }
    })
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)


    from .auth import auth_bp
    from .transactions import transactions_bp
    from .dashboard import dashboard_bp
    from .ai import ai_bp
    from .admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
