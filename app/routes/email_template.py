from flask import Blueprint, request, jsonify
from app import db
from app.models.email_template import EmailTemplate
from app.models.user import User
from datetime import datetime

email_template_bp = Blueprint('email_template', __name__)

# Get all email templates
@email_template_bp.route('/email_templates', methods=['GET'])
def get_email_templates():
    """
    Get a list of all email templates.
    """
    email_templates = EmailTemplate.query.all()
    return jsonify([email_template.to_dict() for email_template in email_templates]), 200

# Get a single email template by ID
@email_template_bp.route('/email_template/<int:email_template_id>', methods=['GET'])
def get_email_template(email_template_id):
    """
    Get a single email template by ID.
    """
    email_template = EmailTemplate.query.get_or_404(email_template_id)
    return jsonify(email_template.to_dict()), 200

# Create a new email template
@email_template_bp.route('/email_template', methods=['POST'])
def create_email_template():
    """
    Create a new email template.
    """
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data or 'user_id' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    email_template = EmailTemplate(
        title=data['title'],
        content=data['content'],
        user_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(email_template)
    db.session.commit()

    return jsonify(email_template.to_dict()), 201

# Update an existing email template
@email_template_bp.route('/email_template/<int:email_template_id>', methods=['PUT'])
def update_email_template(email_template_id):
    """
    Update an existing email template.
    """
    email_template = EmailTemplate.query.get_or_404(email_template_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    email_template.title = data.get('title', email_template.title)
    email_template.content = data.get('content', email_template.content)
    email_template.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(email_template.to_dict()), 200

# Delete an email template
@email_template_bp.route('/email_template/<int:email_template_id>', methods=['DELETE'])
def delete_email_template(email_template_id):
    """
    Delete an email template.
    """
    email_template = EmailTemplate.query.get_or_404(email_template_id)
    db.session.delete(email_template)
    db.session.commit()
    return jsonify({'message': 'Email template deleted successfully'}), 200

# Render an email template (e.g., for preview purposes)
/email_template_bp.route('/email_template/<int:email_template_id>/render', methods=['GET'])
def render_email_template(email_template_id):
    """
    Render an email template.
    """
    email_template = EmailTemplate.query.get_or_404(email_template_id)
    rendered_content = render_template_string(email_template.content)
    return rendered_content, 200

# Get all email templates for a specific user
/email_template_bp.route('/user/<int:user_id>/email_templates', methods=['GET'])
def get_email_templates_for_user(user_id):
    """
    Get all email templates for a specific user.
    """
    user = User.query.get_or_404(user_id)
    email_templates = EmailTemplate.query.filter_by(user_id=user.id).all()
    return jsonify([email_template.to_dict() for email_template in email_templates]), 200
