from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Transaction, User
from . import db

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get('amount')
    category = data.get('category')
    note = data.get('note')
    type_ = data.get('type')

    if type_ not in ['income', 'expense']:
        return jsonify({'msg': 'Invalid transaction type'}), 400

    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        note=note,
        type=type_
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'msg': 'Transaction added', 'transaction_id': transaction.id}), 201

@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def edit_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({'msg': 'Transaction not found'}), 404

    data = request.get_json()
    transaction.amount = data.get('amount', transaction.amount)
    transaction.category = data.get('category', transaction.category)
    transaction.note = data.get('note', transaction.note)
    transaction.type = data.get('type', transaction.type)

    db.session.commit()
    return jsonify({'msg': 'Transaction updated'})

@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({'msg': 'Transaction not found'}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'msg': 'Transaction deleted'})

@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.timestamp.desc()).all()
    result = []
    for t in transactions:
        result.append({
            'id': t.id,
            'amount': t.amount,
            'category': t.category,
            'note': t.note,
            'type': t.type,
            'timestamp': t.timestamp.isoformat()
        })
    return jsonify(result)
