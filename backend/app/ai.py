from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from .models import Transaction
from . import db
from datetime import datetime, timedelta
from collections import defaultdict
import requests
from flask import current_app

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/budget-advice', methods=['GET'])
@jwt_required()
def budget_advice():
    user_id = get_jwt_identity()

    # Fetch transactions for the last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= start_date
    ).all()

    # Aggregate spending by category
    spending = defaultdict(float)
    for t in transactions:
        if t.type == 'expense':
            spending[t.category] += t.amount

    # Prepare prompt for AI
    prompt = "You are a personal finance assistant. Analyze the following spending data and provide budget advice:\n"
    for category, amount in spending.items():
        prompt += f"- {category}: ${amount:.2f}\n"
    prompt += "Provide tips to improve budgeting and highlight any overspending."

    # Use Gemini API instead of Azure OpenAI
    gemini_api_url = os.getenv('GEMINI_API_URL')
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    current_app.logger.info(f"GEMINI_API_URL: {gemini_api_url}")
    current_app.logger.info(f"GEMINI_API_KEY: {'set' if gemini_api_key else 'not set'}")

    if not gemini_api_url or not gemini_api_key:
        return jsonify({'advice': 'Gemini API credentials not configured'}), 500

    headers = {
        'Authorization': f'Bearer {gemini_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'max_tokens': 150,
        'temperature': 0.7
    }

    try:
        response = requests.post(gemini_api_url, json=data, headers=headers)
        response.raise_for_status()
        advice = response.json().get('choices', [{}])[0].get('text', 'No advice returned')
    except Exception as e:
        advice = f"Error generating advice: {str(e)}"

    return jsonify({'advice': advice})

@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    gemini_api_url = os.getenv('GEMINI_API_URL')
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    current_app.logger.info(f"GEMINI_API_URL: {gemini_api_url}")
    current_app.logger.info(f"GEMINI_API_KEY: {'set' if gemini_api_key else 'not set'}")

    if not gemini_api_url or not gemini_api_key:
        return jsonify({'error': 'Gemini API credentials not configured'}), 500

    headers = {
        'Authorization': f'Bearer {gemini_api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': message,
        'max_tokens': 150,
        'temperature': 0.7
    }

    try:
        response = requests.post(gemini_api_url, json=payload, headers=headers)
        response.raise_for_status()
        reply = response.json().get('choices', [{}])[0].get('text', 'No response')
    except Exception as e:
        reply = f"Error generating response: {str(e)}"

    return jsonify({'reply': reply})
