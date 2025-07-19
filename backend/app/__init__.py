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
                "https://finlogix-e0jc.onrender.com"
            ]
        }
    })

    @app.before_request
    def log_request_info():
        from flask import request
        app.logger.info(f"Request: {request.method} {request.url}")
        app.logger.info(f"Headers: {dict(request.headers)}")

    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Error creating tables: {e}")
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

    @app.before_request
    def handle_options_requests():
        from flask import request, make_response
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Headers', 'Authorization,Content-Type')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

    return app
