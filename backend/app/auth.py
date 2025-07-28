from flask import Blueprint, request, jsonify
from .models import User
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_bp = Blueprint('auth', __name__)

def admin_required(func):
    from functools import wraps
    from flask_jwt_extended import get_jwt_identity
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({'msg': 'Admin access required'}), 403
        return func(*args, **kwargs)
    return wrapper

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    print(f"Existing user check result: {existing_user}")
    if existing_user:
        return jsonify({'msg': 'User already exists'}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    # Set default budget goals on user creation
    user.default_budget_goals = {
        "housing": 1000,
        "food": 300,
        "transportation": 150,
        "entertainment": 100,
        "savings": 200
    }
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
    return jsonify({'access_token': access_token})

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    return jsonify({
        'username': user.username,
        'email': user.email,
        'income_type': user.income_type,
        'default_budget_goals': user.default_budget_goals
    })

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    data = request.get_json()
    user.income_type = data.get('income_type', user.income_type)
    user.default_budget_goals = data.get('default_budget_goals', user.default_budget_goals)

    db.session.commit()
    return jsonify({'msg': 'Profile updated successfully'})

@auth_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'income_type': user.income_type,
            'default_budget_goals': user.default_budget_goals,
            'is_admin': user.is_admin
        })
    return jsonify(result)
