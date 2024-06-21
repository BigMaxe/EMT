# app/models/link_review.py
from app import db
import validators
import requests

class LinkReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('email_campaign.id'))
    campaign = db.relationship('EmailCampaign', backref='link_reviews')
    url = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    click_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    safety_check = db.Column(db.String(50), nullable=False)
    functionality_check = db.Column(db.String(50), nullable=False)
    shortened_link = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<LinkReview {self.url}>'

    def validate_url(self):
        # Validate the URL format
        return validators.url(self.url)

    def check_link_safety(self):
        # Using Google's Safe Browsing API
        api_key = 'YOUR_GOOGLE_API_KEY'
        url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
        payload = {
            "client": {
                "clientId": "yourcompany",
                "clientVersion": "1.5.2"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": self.url}
                ]
            }
        }
        response = requests.post(url, json=payload, params={'key': api_key})
        if response.json().get('matches'):
            self.status = 'Unsafe'
        else:
            self.status = 'Safe'

    def check_link_functionality(self):
        # Check if the link is functional
        try:
            response = requests.head(self.url)
            if response.status_code == 200:
                self.status = 'Functional'
            else:
                self.status = 'Broken'
        except requests.RequestException:
            self.status = 'Broken'

    def shorten_link(self):
        access_token = 'YOUR_BITLY_ACCESS_TOKEN'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        data = {
            "long_url": self.url,
            "domain": "bit.ly"
        }
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['link']
        return self.url

    def review_link(self):
        if not self.validate_url():
            self.status = 'Invalid'
            return

        self.check_link_safety()
        if self.status == 'Unsafe':
            return

        self.check_link_functionality()
        if self.status == 'Functional':
            self.url = self.shorten_link()

    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'url': self.url,
            'status': self.status,
            'click_count': self.click_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'safety_check': self.safety_check,
            'functionality_check': self.functionality_check,
            'shortened_link': self.shortened_link
        }
