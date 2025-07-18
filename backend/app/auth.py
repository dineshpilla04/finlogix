from flask import Blueprint, request, jsonify
from .models import User
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'msg': 'User already exists'}), 409

    user = User(username=username, email=email)
    user.set_password(password)
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
