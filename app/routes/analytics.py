from flask import Blueprint, request, jsonify
from app.models.analytics import EmailAnalytics, ClickAnalytics
from app import db
from datetime import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/email_open', methods=['POST'])
def track_email_open():
    """
    Track email open event.
    """
    data = request.get_json()

    if not data or not 'email_id' in data or not 'user_id' in data:
        return jsonify({'message': 'Invalid data'}), 400

    email_analytics = EmailAnalytics(
        email_id=data['email_id'],
        user_id=data['user_id'],
        opened_at=datetime.utcnow()
    )

    db.session.add(email_analytics)
    db.session.commit()

    return jsonify({'message': 'Email open event tracked successfully'}), 201

@analytics_bp.route('/analytics/click', methods=['POST'])
def track_click():
    """
    Track link click event.
    """
    data = request.get_json()

    if not data or not 'email_id' in data or not 'user_id' in data or not 'url' in data:
        return jsonify({'message': 'Invalid data'}), 400

    click_analytics = ClickAnalytics(
        email_id=data['email_id'],
        user_id=data['user_id'],
        url=data['url'],
        clicked_at=datetime.utcnow()
    )

    db.session.add(click_analytics)
    db.session.commit()

    return jsonify({'message': 'Click event tracked successfully'}), 201

@analytics_bp.route('/analytics/email_open/<int:email_id>', methods=['GET'])
def get_email_opens(email_id):
    """
    Get email open analytics by email ID.
    """
    email_opens = EmailAnalytics.query.filter_by(email_id=email_id).all()

    response = {
        'email_id': email_id,
        'opens': [{'user_id': open.user_id, 'opened_at': open.opened_at} for open in email_opens]
    }

    return jsonify(response)

@analytics_bp.route('/analytics/clicks/<int:email_id>', methods=['GET'])
def get_clicks(email_id):
    """
    Get click analytics by email ID.
    """
    clicks = ClickAnalytics.query.filter_by(email_id=email_id).all()

    response = {
        'email_id': email_id,
        'clicks': [{'user_id': click.user_id, 'url': click.url, 'clicked_at': click.clicked_at} for click in clicks]
    }

    return jsonify(response)
