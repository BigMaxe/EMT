from app import db
from datetime import datetime

class SocialInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'content': self.content,
            'timestamp': self.timestamp,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
