from app import db

class EmailAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    opened_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<EmailAnalytics email_id={self.email_id} user_id={self.user_id} opened_at={self.opened_at}>'

class ClickAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    clicked_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<ClickAnalytics email_id={self.email_id} user_id={self.user_id} url={self.url} clicked_at={self.clicked_at}>'
