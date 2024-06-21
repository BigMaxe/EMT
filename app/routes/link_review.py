from flask import Blueprint, request, jsonify
from app import db
from app.models.link_review import LinkReview
from datetime import datetime
import validators
import requests

link_review_bp = Blueprint('link_review', __name__)

# Get all link reviews
@link_review_bp.route('/link_reviews', methods=['GET'])
def get_link_reviews():
    link_reviews = LinkReview.query.all()
    return jsonify([link_review.to_dict() for link_review in link_reviews]), 200

# Get a single link review by ID
@link_review_bp.route('/link_review/<int:link_review_id>', methods=['GET'])
def get_link_review(link_review_id):
    link_review = LinkReview.query.get_or_404(link_review_id)
    return jsonify(link_review.to_dict()), 200

# Create a new link review
@link_review_bp.route('/link_review', methods=['POST'])
def create_link_review():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    url = data['url']

    if not validators.url(url):
        return jsonify({'message': 'Invalid URL'}), 400

    safety_check = check_link_safety(url)
    functionality_check = check_link_functionality(url)
    shortened_link = shorten_link(url)

    link_review = LinkReview(
        url=url,
        safety_check=safety_check,
        functionality_check=functionality_check,
        shortened_link=shortened_link,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(link_review)
    db.session.commit()
    return jsonify(link_review.to_dict()), 201

# Update an existing link review
@link_review_bp.route('/link_review/<int:link_review_id>', methods=['PUT'])
def update_link_review(link_review_id):
    link_review = LinkReview.query.get_or_404(link_review_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    link_review.url = data.get('url', link_review.url)
    link_review.safety_check = data.get('safety_check', link_review.safety_check)
    link_review.functionality_check = data.get('functionality_check', link_review.functionality_check)
    link_review.shortened_link = data.get('shortened_link', link_review.shortened_link)
    link_review.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify(link_review.to_dict()), 200

# Delete a link review
@link_review_bp.route('/link_review/<int:link_review_id>', methods=['DELETE'])
def delete_link_review(link_review_id):
    link_review = LinkReview.query.get_or_404(link_review_id)
    db.session.delete(link_review)
    db.session.commit()
    return jsonify({'message': 'Link review deleted successfully'}), 200

def check_link_safety(url):
    # Placeholder for link safety check logic
    # This could include using services like Google Safe Browsing, VirusTotal, etc.
    response = requests.get(f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={YOUR_API_KEY}',
                            json={"client": {"clientId": "yourcompany", "clientVersion": "1.5.2"},
                                  "threatInfo": {"threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                                                 "platformTypes": ["ANY_PLATFORM"],
                                                 "threatEntryTypes": ["URL"],
                                                 "threatEntries": [{"url": url}]}})
    if response.json().get('matches'):
        return 'Unsafe'
    return 'Safe'

def check_link_functionality(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return 'Functional'
        else:
            return 'Not Functional'
    except requests.exceptions.RequestException:
        return 'Not Functional'

def shorten_link(url):
    # Placeholder for link shortening logic
    # This could include using services like Bitly, TinyURL, etc.
    response = requests.post('https://api-ssl.bitly.com/v4/shorten',
                             headers={'Authorization': f'Bearer {BITLY_API_KEY}'},
                             json={"long_url": url})
    if response.status_code == 200:
        return response.json().get('link')
    return url
