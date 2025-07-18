from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@ai_bp.route('/suggestions', methods=['GET'])
@jwt_required()
def get_ai_suggestions():
    user_id = get_jwt_identity()['id']

    # You can use Gemini API here. For now, mock suggestion:
    suggestion = "You spent 40% of your income on food this week. Try meal prepping."

    return jsonify({"suggestion": suggestion})
