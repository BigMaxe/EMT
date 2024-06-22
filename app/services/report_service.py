import json
import os
from datetime import datetime
from flask import jsonify
from app import db
from app.models.email_campaign import EmailCampaign
from app.models.email_list import EmailList
from app.models.email_template import EmailTemplate
from app.models.email_survey import EmailSurvey
from app.models.link_review import LinkReview
from app.models.spam_filter import SpamFilter
from app.models.device_optimization import DeviceOptimization

class ReportService:
    def __init__(self):
        pass

    def generate_campaign_report(self, campaign_id):
        campaign = EmailCampaign.query.get(campaign_id)
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404

        report = {
            "campaign_name": campaign.name,
            "total_recipients": campaign.total_recipients,
            "emails_sent": campaign.emails_sent,
            "open_rate": self.calculate_open_rate(campaign),
            "click_through_rate": self.calculate_click_through_rate(campaign),
            "bounce_rate": self.calculate_bounce_rate(campaign),
            "spam_complaints": campaign.spam_complaints,
            "unsubscribes": campaign.unsubscribes,
            "sent_date": campaign.sent_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(report)

    def calculate_open_rate(self, campaign):
        if campaign.emails_sent == 0:
            return 0
        return (campaign.opens / campaign.emails_sent) * 100

    def calculate_click_through_rate(self, campaign):
        if campaign.emails_sent == 0:
            return 0
        return (campaign.clicks / campaign.emails_sent) * 100

    def calculate_bounce_rate(self, campaign):
        if campaign.emails_sent == 0:
            return 0
        return (campaign.bounces / campaign.emails_sent) * 100

    def generate_summary_report(self):
        campaigns = EmailCampaign.query.all()
        total_campaigns = len(campaigns)
        total_emails_sent = sum([campaign.emails_sent for campaign in campaigns])
        total_opens = sum([campaign.opens for campaign in campaigns])
        total_clicks = sum([campaign.clicks for campaign in campaigns])
        total_bounces = sum([campaign.bounces for campaign in campaigns])
        total_spam_complaints = sum([campaign.spam_complaints for campaign in campaigns])
        total_unsubscribes = sum([campaign.unsubscribes for campaign in campaigns])

        report = {
            "total_campaigns": total_campaigns,
            "total_emails_sent": total_emails_sent,
            "total_opens": total_opens,
            "total_clicks": total_clicks,
            "total_bounces": total_bounces,
            "total_spam_complaints": total_spam_complaints,
            "total_unsubscribes": total_unsubscribes,
            "overall_open_rate": self.calculate_overall_rate(total_opens, total_emails_sent),
            "overall_click_through_rate": self.calculate_overall_rate(total_clicks, total_emails_sent),
            "overall_bounce_rate": self.calculate_overall_rate(total_bounces, total_emails_sent)
        }
        return jsonify(report)

    def calculate_overall_rate(self, metric, total_emails_sent):
        if total_emails_sent == 0:
            return 0
        return (metric / total_emails_sent) * 100

    def export_report(self, report, file_format='json'):
        filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_format}"
        file_path = os.path.join('reports', filename)

        if file_format == 'json':
            with open(file_path, 'w') as file:
                json.dump(report, file)
        elif file_format == 'csv':
            # Convert JSON report to CSV format and write to file
            pass

        return file_path

# Usage example:
# report_service = ReportService()
# campaign_report = report_service.generate_campaign_report(1)
# summary_report = report_service.generate_summary_report()
