from app import db
from datetime import datetime

class EmailSurvey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    questions = db.relationship('Question', backref='email_survey', lazy=True)
    responses = db.relationship('SurveyResponse', backref='email_survey', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'questions': [question.to_dict() for question in self.questions],
            'responses': [response.to_dict() for response in self.responses]
        }
