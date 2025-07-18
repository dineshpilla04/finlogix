import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.audio_note import AudioNote
from datetime import datetime

audio_bp = Blueprint('audio', __name__, url_prefix='/api/audio')

@audio_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_audio():
    user_id = get_jwt_identity()['id']
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join('uploads', filename)
    file.save(upload_path)

    audio_note = AudioNote(user_id=user_id, filename=filename, created_at=datetime.utcnow())
    db.session.add(audio_note)
    db.session.commit()

    return jsonify({"message": "Audio uploaded", "filename": filename}), 201
