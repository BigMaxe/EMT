from flask import Blueprint, request, jsonify
from app.services.spam_filter_service import SpamFilterService

spam_filter_bp = Blueprint('spam_filter_bp', __name__)
spam_filter_service = SpamFilterService()

@spam_filter_bp.route('/analyze_content', methods=['POST'])
def analyze_content():
    content = request.json.get('content')
    spam_score = spam_filter_service.calculate_spam_score(content)
    return jsonify({"spam_score": spam_score})

@spam_filter_bp.route('/authenticate_email', methods=['POST'])
def authenticate_email():
    email = request.json.get('email')
    is_authenticated = spam_filter_service.authenticate_email(email)
    return jsonify({"is_authenticated": is_authenticated})

@spam_filter_bp.route('/avoid_blacklist', methods=['POST'])
def avoid_blacklist():
    email = request.json.get('email')
    is_clean = spam_filter_service.avoid_blacklist(email)
    return jsonify({"is_clean": is_clean})

@spam_filter_bp.route('/check_user_engagement', methods=['POST'])
def check_user_engagement():
    email = request.json.get('email')
    engagement_metrics = spam_filter_service.check_user_engagement(email)
    return jsonify(engagement_metrics)
