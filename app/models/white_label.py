from app import db

class WhiteLabelSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(120), nullable=True)
    logo_path = db.Column(db.String(120), nullable=True)
    theme_color = db.Column(db.String(20), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)

    def to_dict(self):
        return {
            'brand_name': self.brand_name,
            'logo_path': self.logo_path,
            'theme_color': self.theme_color,
            'contact_email': self.contact_email
        }
