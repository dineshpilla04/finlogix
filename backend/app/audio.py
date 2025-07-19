from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from .models import AudioNote, User
from . import db
from datetime import datetime

audio_bp = Blueprint('audio', __name__)

UPLOAD_FOLDER = 'uploads/audio_notes'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@audio_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    transaction_id = request.form.get('transaction_id', type=int)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_id = get_jwt_identity()
        user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
        os.makedirs(user_folder, exist_ok=True)
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)

        audio_note = AudioNote(
            user_id=user_id,
            transaction_id=transaction_id,
            audio_url=filepath,
            created_at=datetime.utcnow()
        )
        db.session.add(audio_note)
        db.session.commit()

        # Update transaction to link audio_note if transaction_id provided
        if transaction_id:
            from .models import Transaction
            transaction = Transaction.query.get(transaction_id)
            if transaction:
                transaction.audio_note_id = audio_note.id
                db.session.commit()

        return jsonify({'message': 'File uploaded', 'audio_note_id': audio_note.id, 'audio_url': filepath}), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@audio_bp.route('/list', methods=['GET'])
@jwt_required()
def list_audio_notes():
    user_id = get_jwt_identity()
    audio_notes = AudioNote.query.filter_by(user_id=user_id).order_by(AudioNote.created_at.desc()).all()
    result = []
    for note in audio_notes:
        result.append({
            'id': note.id,
            'audio_url': note.audio_url,
            'created_at': note.created_at.isoformat()
        })
    return jsonify(result)
