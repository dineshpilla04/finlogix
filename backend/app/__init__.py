from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:QtAVXcholCNurSxVtHElBECMyvuNiwvv@mainline.proxy.rlwy.net:31816/railway'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Remove duplicate Flask app instantiation
    # app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # ✅ Correct CORS setup
    CORS(app,
         supports_credentials=True,
         resources={r"/*": {"origins": [
             "http://localhost:3000",
             "https://finlogix-gray.vercel.app"
         ]}})

    # 🔍 Log every request (optional but useful)
    @app.before_request
    def skip_options_preflight():
        from flask import request
        if request.method == 'OPTIONS':
            return '', 200

    @app.before_request
    def log_request_info():
        from flask import request
        app.logger.info(f"Request: {request.method} {request.url}")
        app.logger.info(f"Headers: {dict(request.headers)}")

    db.init_app(app)
    with app.app_context():
        from . import models
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Error creating tables: {e}")

    jwt.init_app(app)
    socketio.init_app(app)

    # Register Blueprints
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
