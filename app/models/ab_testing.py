from app import db

class ABTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    variants = db.Column(db.PickleType, nullable=False)  # List of variants
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<ABTest {self.name}>'

class ABTestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('ab_test.id'), nullable=False)
    variant = db.Column(db.String(100), nullable=False)
    conversion = db.Column(db.Boolean, nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False)

    ab_test = db.relationship('ABTest', backref=db.backref('results', lazy=True))

    def __repr__(self):
        return f'<ABTestResult {self.variant} - {self.conversion}>'
