from app.extensions import db
from datetime import datetime

class AudioNote(db.Model):
    __tablename__ = 'audio_notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "created_at": self.created_at.isoformat()
        }
