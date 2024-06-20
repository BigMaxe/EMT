from flask import Blueprint, request, jsonify
from app import db
from app.models.email_list import EmailList
from app.models.user import User
from app.models.email import Email
from datetime import datetime

email_list_bp = Blueprint('email_list', __name__)

@email_list_bp.route('/email_lists', methods=['GET'])
def get_email_lists():
    """
    Get a list of all email lists.
    """
    email_lists = EmailList.query.all()
    return jsonify([email_list.to_dict() for email_list in email_lists]), 200

@email_list_bp.route('/email_list/<int:email_list_id>', methods=['GET'])
def get_email_list(email_list_id):
    """
    Get a single email list by ID.
    """
    email_list = EmailList.query.get_or_404(email_list_id)
    return jsonify(email_list.to_dict()), 200

@email_list_bp.route('/email_list', methods=['POST'])
def create_email_list():
    """
    Create a new email list.
    """
    data = request.get_json()
    if not data or 'name' not in data or 'user_id' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    email_list = EmailList(
        name=data['name'],
        user_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(email_list)
    db.session.commit()

    return jsonify(email_list.to_dict()), 201

# Update email list
@email_list_bp.route('/email_list/<int:email_list_id>', methods=['PUT'])
def update_email_list(email_list_id):
    """
    Update an existing email list.
    """
    email_list = EmailList.query.get_or_404(email_list_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    email_list.name = data.get('name', email_list.name)
    email_list.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(email_list.to_dict()), 200

# Delete email list
@email_list_bp.route('/email_list/<int:email_list_id>', methods=['DELETE'])
def delete_email_list(email_list_id):
    """
    Delete an email list.
    """
    email_list = EmailList.query.get_or_404(email_list_id)
    db.session.delete(email_list)
    db.session.commit()
    return jsonify({'message': 'Email list deleted successfully'}), 200

# Add email to email list
@email_list_bp.route('/email_list/<int:email_list_id>/add_email', methods=['POST'])
def add_email_to_list(email_list_id):
    """
    Add an email to an email list.
    """
    email_list = EmailList.query.get_or_404(email_list_id)
    data = request.get_json()

    if not data or 'email' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    email = Email(email=data['email'], email_list_id=email_list.id, created_at=datetime.utcnow())
    db.session.add(email)
    db.session.commit()

    return jsonify(email.to_dict()), 201

# Remove email from email list
@email_list_bp.route('/email_list/<int:email_list_id>/remove_email/<int:email_id>', methods=['DELETE'])
def remove_email_from_list(email_list_id, email_id):
    """
    Remove an email from an email list.
    """
    email_list = EmailList.query.get_or_404(email_list_id)
    email = Email.query.filter_by(id=email_id, email_list_id=email_list.id).first_or_404()

    db.session.delete(email)
    db.session.commit()

    return jsonify({'message': 'Email removed from list successfully'}), 200

# Get emails from email list
@email_list_bp.route('/email_list/<int:email_list_id>/emails', methods=['GET'])
def get_emails_from_list(email_list_id):
    """
    Get all emails from an email list.
    """
    email_list = EmailList.query.get_or_404(email_list_id)
    emails = Email.query.filter_by(email_list_id=email_list.id).all()
    return jsonify([email.to_dict() for email in emails]), 200
