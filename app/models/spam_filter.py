from app import db
import spamsum
import dns.resolver
import requests
import random
import os

class SpamFilter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('email_campaign.id'))
    campaign = db.relationship('EmailCampaign', backref='spam_filters')
    filter_rules = db.Column(db.JSON, nullable=False)
    effectiveness = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<SpamFilter {self.id}>'

    def analyze_content(self, content):
        spam_keywords = ['free', 'win', 'winner', 'cash', 'prize', 'urgent']
        for keyword in spam_keywords:
            if keyword in content.lower():
                return True
        return False


    def calculate_spam_score(self, content):
        """
        Calculate the spam score of the given content using SpamAssassin.
        """
        spamassassin_url = os.getenv('SPAMASSASSIN_URL', 'http://localhost:783')  # URL to your SpamAssassin service
        headers = {'Content-Type': 'text/plain'}

        try:
            response = requests.post(spamassassin_url, data=content, headers=headers)
            response.raise_for_status()

            # Assuming SpamAssassin returns the score in the response body
            score_line = next((line for line in response.text.split('\n') if 'score=' in line), None)
            if score_line:
                score = float(score_line.split('score=')[1].split()[0])
                return score
            else:
                return 0.0
        except requests.RequestException as e:
            print(f"Error contacting SpamAssassin: {e}")
            return 0.0

    def authenticate_email(self, email):
        domain = email.split('@')[-1]

        # Check SPF record
        try:
            spf_record = dns.resolver.resolve(f'{domain}', 'TXT')
            spf_valid = any('v=spf1' in txt.to_text() for txt in spf_record)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            spf_valid = False

        # Check DKIM record
        try:
            dkim_selector = 'default._domainkey'
            dkim_record = dns.resolver.resolve(f'{dkim_selector}.{domain}', 'TXT')
            dkim_valid = any('v=DKIM1' in txt.to_text() for txt in dkim_record)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            dkim_valid = False

        # Check DMARC record
        try:
            dmarc_record = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
            dmarc_valid = any('v=DMARC1' in txt.to_text() for txt in dmarc_record)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            dmarc_valid = False

        return spf_valid, dkim_valid, dmarc_valid

    def avoid_blacklist(self, email):
        domain = email.split('@')[-1]
        api_key = os.getenv('MXTOOLBOX_API_KEY')
        api_url = f'https://api.mxtoolbox.com/api/v1/blacklist/{domain}'

        headers = {
            'Authorization': f'Bearer {api_key}'
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data.get('blacklist', False):
                blacklisted = data['blacklist']
                return any(entry['listed'] for entry in blacklisted)
            return False
        except requests.RequestException as e:
            print(f"Error contacting MXToolbox: {e}")
            return False

    def check_user_engagement(self, email):
        # Simulate user engagement metrics (open rate and click rate)
        open_rate = random.uniform(0.1, 0.5)  # Simulate open rate between 10% to 50%
        click_rate = random.uniform(0.01, 0.2)  # Simulate click rate between 1% to 20%

        # Check if engagement is above certain thresholds
        if open_rate >= 0.2 and click_rate >= 0.05:
            return True
        else:
            return False

    def apply_filter(self, email, content):
        self.analyze_content(content)
        spam_score = self.calculate_spam_score(content)
        self.authenticate_email(email)
        self.avoid_blacklist(email)
        self.check_user_engagement(email)

        if spam_score > 5.0:
            self.effectiveness = 0.0
        else:
            self.effectiveness = 100.0 - spam_score

    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'filter_rules': self.filter_rules,
            'effectiveness': self.effectiveness,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
