from flask import Blueprint, request, jsonify
from app import db
from app.models.email_campaign import EmailCampaign
from app.models.email_list import EmailList
from app.models.email_template import EmailTemplate
from app.models.user import User
from datetime import datetime
from app.services.email_service import EmailService

campaign_bp = Blueprint('campaign', __name__)

@campaign_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    """
    Get a list of all email campaigns.
    """
    campaigns = EmailCampaign.query.all()
    return jsonify([campaign.to_dict() for campaign in campaigns]), 200

@campaign_bp.route('/campaign/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """
    Get a single email campaign by ID.
    """
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    return jsonify(campaign.to_dict()), 200

@campaign_bp.route('/campaign', methods=['POST'])
def create_campaign():
    """
    Create a new email campaign.
    """
    data = request.get_json()
    if not data or 'name' not in data or 'subject' not in data or 'email_list_id' not in data or 'email_template_id' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    email_list = EmailList.query.get(data['email_list_id'])
    email_template = EmailTemplate.query.get(data['email_template_id'])
    user = User.query.get(data.get('user_id', 1))  # Default to user ID 1 if not provided

    if not email_list or not email_template or not user:
        return jsonify({'message': 'Email list, template, or user not found'}), 404

    campaign = EmailCampaign(
        name=data['name'],
        subject=data['subject'],
        email_list_id=email_list.id,
        email_template_id=email_template.id,
        user_id=user.id,
        created_at=datetime.utcnow(),
        status='Scheduled'
    )

    db.session.add(campaign)
    db.session.commit()

    return jsonify(campaign.to_dict()), 201

@campaign_bp.route('/campaign/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    """
    Update an existing email campaign.
    """
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    campaign.name = data.get('name', campaign.name)
    campaign.subject = data.get('subject', campaign.subject)
    campaign.email_list_id = data.get('email_list_id', campaign.email_list_id)
    campaign.email_template_id = data.get('email_template_id', campaign.email_template_id)
    campaign.status = data.get('status', campaign.status)
    campaign.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(campaign.to_dict()), 200

@campaign_bp.route('/campaign/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """
    Delete an email campaign.
    """
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign deleted successfully'}), 200

@campaign_bp.route('/campaign/send/<int:campaign_id>', methods=['POST'])
def send_campaign(campaign_id):
    """
    Send an email campaign.
    """
    campaign = EmailCampaign.query.get_or_404(campaign_id)

    if campaign.status != 'Scheduled':
        return jsonify({'message': 'Campaign is not scheduled for sending'}), 400

    email_service = EmailService()
    recipients = [email.email for email in campaign.email_list.emails]
    email_template = campaign.email_template.content

    try:
        email_service.send_bulk_email(campaign.subject, recipients, email_template)
        campaign.status = 'Sent'
        campaign.sent_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Campaign sent successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to send campaign: {e}'}), 500
