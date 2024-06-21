from flask import Blueprint, request, jsonify
from app import db
from app.models.form import Form, FormField
from app.models.form_response import FormResponse
from datetime import datetime

form_builder_bp = Blueprint('form_builder', __name__)

# Get all forms
@form_builder_bp.route('/forms', methods=['GET'])
def get_forms():
    forms = Form.query.all()
    return jsonify([form.to_dict() for form in forms]), 200

# Get a single form by ID
@form_builder_bp.route('/form/<int:form_id>', methods=['GET'])
def get_form(form_id):
    form = Form.query.get_or_404(form_id)
    return jsonify(form.to_dict()), 200

# Create a new form
@form_builder_bp.route('/form', methods=['POST'])
def create_form():
    data = request.get_json()
    if not data or 'title' not in data or 'fields' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    form = Form(
        title=data['title'],
        description=data.get('description', ''),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(form)
    db.session.commit()

    for field in data['fields']:
        form_field = FormField(
            form_id=form.id,
            field_name=field['name'],
            field_type=field['type'],
            field_options=field.get('options', {}),
            required=field.get('required', False)
        )
        db.session.add(form_field)

    db.session.commit()
    return jsonify(form.to_dict()), 201

# Update an existing form
@form_builder_bp.route('/form/<int:form_id>', methods=['PUT'])
def update_form(form_id):
    form = Form.query.get_or_404(form_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    form.title = data.get('title', form.title)
    form.description = data.get('description', form.description)
    form.updated_at = datetime.utcnow()

    db.session.commit()

    # Update form fields
    if 'fields' in data:
        FormField.query.filter_by(form_id=form.id).delete()
        db.session.commit()

        for field in data['fields']:
            form_field = FormField(
                form_id=form.id,
                field_name=field['name'],
                field_type=field['type'],
                field_options=field.get('options', {}),
                required=field.get('required', False)
            )
            db.session.add(form_field)

        db.session.commit()

    return jsonify(form.to_dict()), 200

# Delete a form
@form_builder_bp.route('/form/<int:form_id>', methods=['DELETE'])
def delete_form(form_id):
    form = Form.query.get_or_404(form_id)
    FormField.query.filter_by(form_id=form.id).delete()
    db.session.delete(form)
    db.session.commit()
    return jsonify({'message': 'Form deleted successfully'}), 200

# Submit a form
@form_builder_bp.route('/form/<int:form_id>/submit', methods=['POST'])
def submit_form(form_id):
    form = Form.query.get_or_404(form_id)
    data = request.get_json()

    if not data or 'responses' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    responses = data['responses']
    for field in form.fields:
        if field.required and field.field_name not in responses:
            return jsonify({'message': f'Missing required field: {field.field_name}'}), 400

    form_response = FormResponse(
        form_id=form.id,
        responses=responses,
        submitted_at=datetime.utcnow()
    )
    db.session.add(form_response)
    db.session.commit()

    return jsonify({'message': 'Form submitted successfully'}), 200
