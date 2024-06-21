from app import db
from datetime import datetime

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_survey_id = db.Column(db.Integer, db.ForeignKey('email_survey.id'), nullable=False)
    responses = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email_survey_id': self.email_survey_id,
            'responses': self.responses,
            'created_at': self.created_at
        }
