import os
from flask import Flask, send_from_directory
from dotenv import load_dotenv

from app.extensions import db, jwt, socketio, cors

# Blueprints
from app.auth.routes import auth_bp
from app.transactions.routes import transactions_bp
from app.dashboard.routes import dashboard_bp
from app.ai_advice.routes import ai_bp
from app.audio.routes import audio_bp
from app.admin_panel.routes import admin_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    # ✅ CORS (use this only, remove manual headers)
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:3001"}}, supports_credentials=True)

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="http://localhost:3001")

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(admin_bp)

    # File serving
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
