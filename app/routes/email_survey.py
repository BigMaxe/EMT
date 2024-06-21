from flask import Blueprint, request, jsonify
from app import db
from app.models.email_survey import EmailSurvey
from app.models.user import User
from datetime import datetime

email_survey_bp = Blueprint('email_survey', __name__)

# Get all email surveys
@email_survey_bp.route('/email_surveys', methods=['GET'])
def get_email_surveys():
    """
    Get a list of all email surveys.
    """
    email_surveys = EmailSurvey.query.all()
    return jsonify([email_survey.to_dict() for email_survey in email_surveys]), 200

# Get a single email survey by ID
@email_survey_bp.route('/email_survey/<int:email_survey_id>', methods=['GET'])
def get_email_survey(email_survey_id):
    """
    Get a single email survey by ID.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    return jsonify(email_survey.to_dict()), 200

# Create a new email survey
@email_survey_bp.route('/email_survey', methods=['POST'])
def create_email_survey():
    """
    Create a new email survey.
    """
    data = request.get_json()
    if not data or 'title' not in data or 'user_id' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    email_survey = EmailSurvey(
        title=data['title'],
        description=data.get('description', ''),
        user_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(email_survey)
    db.session.commit()

    return jsonify(email_survey.to_dict()), 201

# Update an existing email survey
@email_survey_bp.route('/email_survey/<int:email_survey_id>', methods=['PUT'])
def update_email_survey(email_survey_id):
    """
    Update an existing email survey.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    email_survey.title = data.get('title', email_survey.title)
    email_survey.description = data.get('description', email_survey.description)
    email_survey.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(email_survey.to_dict()), 200

# Delete an email survey
@email_survey_bp.route('/email_survey/<int:email_survey_id>', methods=['DELETE'])
def delete_email_survey(email_survey_id):
    """
    Delete an email survey.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    db.session.delete(email_survey)
    db.session.commit()
    return jsonify({'message': 'Email survey deleted successfully'}), 200

# Add a question to an email survey
@email_survey_bp.route('/email_survey/<int:email_survey_id>/add_question', methods=['POST'])
def add_question_to_survey(email_survey_id):
    """
    Add a question to an email survey.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    data = request.get_json()

    if not data or 'question_text' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    question = Question(
        question_text=data['question_text'],
        email_survey_id=email_survey.id,
        created_at=datetime.utcnow()
    )

    db.session.add(question)
    db.session.commit()

    return jsonify(question.to_dict()), 201

# Remove a question from an email survey
@email_survey_bp.route('/email_survey/<int:email_survey_id>/remove_question/<int:question_id>', methods=['DELETE'])
def remove_question_from_survey(email_survey_id, question_id):
    """
    Remove a question from an email survey.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    question = Question.query.filter_by(id=question_id, email_survey_id=email_survey.id).first_or_404()

    db.session.delete(question)
    db.session.commit()

    return jsonify({'message': 'Question removed from survey successfully'}), 200

# Get all questions from an email survey
@email_survey_bp.route('/email_survey/<int:email_survey_id>/questions', methods=['GET'])
def get_questions_from_survey(email_survey_id):
    """
    Get all questions from an email survey.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    questions = Question.query.filter_by(email_survey_id=email_survey.id).all()
    return jsonify([question.to_dict() for question in questions]), 200

# Submit a survey response
@email_survey_bp.route('/email_survey/<int:email_survey_id>/submit_response', methods=['POST'])
def submit_survey_response(email_survey_id):
    """
    Submit a survey response.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    data = request.get_json()

    if not data or 'responses' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    response = SurveyResponse(
        email_survey_id=email_survey.id,
        responses=data['responses'],
        created_at=datetime.utcnow()
    )

    db.session.add(response)
    db.session.commit()

    return jsonify(response.to_dict()), 201

# Get survey responses
@email_survey_bp.route('/email_survey/<int:email_survey_id>/responses', methods=['GET'])
def get_survey_responses(email_survey_id):
    """
    Get all responses for an email survey.
    """
    email_survey = EmailSurvey.query.get_or_404(email_survey_id)
    responses = SurveyResponse.query.filter_by(email_survey_id=email_survey.id).all()
    return jsonify([response.to_dict() for response in responses]), 200
