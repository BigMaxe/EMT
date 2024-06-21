from app import db
from datetime import datetime

class FormResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    responses = db.Column(db.JSON, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    form = db.relationship('Form', backref=db.backref('responses', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'form_id': self.form_id,
            'responses': self.responses,
            'submitted_at': self.submitted_at
        }
