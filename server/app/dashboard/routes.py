from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction import Transaction
from sqlalchemy import func
from app.extensions import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def dashboard_summary():
    user_id = get_jwt_identity()['id']

    income = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=user_id, type='income').scalar() or 0
    expense = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=user_id, type='expense').scalar() or 0
    balance = income - expense

    return jsonify({
        "total_income": income,
        "total_expense": expense,
        "balance": balance
    })
