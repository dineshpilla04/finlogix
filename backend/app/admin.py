from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, Transaction
from . import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    # Example static categories, replace with DB query if needed
    categories = ['Rent', 'Food', 'Travel', 'Utilities', 'Entertainment']
    return jsonify(categories)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    if not isinstance(user_id, str):
        user_id = str(user_id)
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({'msg': 'Unauthorized'}), 401

    users = User.query.all()
    users_data = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
    return jsonify(users_data)

@admin_bp.route('/users/<int:user_id>/promote', methods=['POST'])
@jwt_required()
def promote_user(user_id):
    # Remove admin check to allow any authorized user to promote
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    user.is_admin = True
    db.session.commit()
    return jsonify({'msg': f'User {user.username} promoted to admin successfully'})
