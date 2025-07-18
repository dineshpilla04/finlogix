from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction import Transaction
from app.extensions import db, socketio

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()['id']
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    result = [{
        "id": t.id,
        "type": t.type,
        "category": t.category,
        "amount": t.amount,
        "note": t.note,
        "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for t in transactions]
    return jsonify(result)

@transactions_bp.route('/', methods=['POST'])
@jwt_required()
def add_transaction():
    data = request.get_json()
    user_id = get_jwt_identity()['id']

    new_txn = Transaction(
        user_id=user_id,
        type=data['type'],
        category=data['category'],
        amount=data['amount'],
        note=data.get('note', '')
    )
    db.session.add(new_txn)
    db.session.commit()

    socketio.emit("new_transaction", {"user_id": user_id})  # Real-time update

    return jsonify({"message": "Transaction added"}), 201
