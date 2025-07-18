from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.transaction import Transaction
from app.extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if not user or not user.is_admin:
        return jsonify({"error": "Admin access only"}), 403

    users = User.query.all()
    result = [{"id": u.id, "email": u.email, "is_admin": u.is_admin} for u in users]
    return jsonify(result)
