from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Transaction
from . import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    user_id = get_jwt_identity()
    if not isinstance(user_id, str):
        user_id = str(user_id)
    # Fetch transactions for the user and calculate summary
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    category_breakdown = {}
    for t in transactions:
        category_breakdown[t.category] = category_breakdown.get(t.category, 0) + t.amount

    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_breakdown': category_breakdown
    })
