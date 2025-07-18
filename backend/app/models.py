from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    income_type = db.Column(db.String(50))
    default_budget_goals = db.Column(db.JSON)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    audio_notes = db.relationship('AudioNote', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(255))
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    audio_note_id = db.Column(db.Integer, db.ForeignKey('audio_note.id'))

class AudioNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    audio_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
