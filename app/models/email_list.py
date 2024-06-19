from app import db

class EmailList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='email_lists')

    def __repr__(self):
        return '<EmailList %r>' % self.name
