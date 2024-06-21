from app import db
from datetime import datetime

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(256), nullable=False)
    email_survey_id = db.Column(db.Integer, db.ForeignKey('email_survey.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'email_survey_id': self.email_survey_id,
            'created_at': self.created_at
        }
