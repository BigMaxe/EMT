from flask import Blueprint, request, jsonify
from app.models.email_campaign import EmailCampaign
from app.models.email_list import EmailList
from app.services.automation_service import AutomationService
from app import db
from datetime import datetime

automation_bp = Blueprint('automation', __name__)

@automation_bp.route('/automation/schedule', methods=['POST'])
def schedule_campaign():
    """
    Schedule an email campaign.
    """
    data = request.get_json()

    if not data or not 'campaign_id' in data or not 'scheduled_time' in data:
        return jsonify({'message': 'Invalid data'}), 400

    campaign = EmailCampaign.query.get(data['campaign_id'])

    if not campaign:
        return jsonify({'message': 'Campaign not found'}), 404

    try:
        scheduled_time = datetime.strptime(data['scheduled_time'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    campaign.scheduled_time = scheduled_time
    db.session.commit()

    return jsonify({'message': 'Campaign scheduled successfully'}), 200

@automation_bp.route('/automation/run', methods=['POST'])
def run_automation():
    """
    Run automated tasks.
    """
    AutomationService.run_pending_tasks()
    return jsonify({'message': 'Automated tasks executed successfully'}), 200

@automation_bp.route('/automation/workflow', methods=['POST'])
def create_workflow():
    """
    Create an automation workflow.
    """
    data = request.get_json()

    if not data or not 'name' in data or not 'triggers' in data or not 'actions' in data:
        return jsonify({'message': 'Invalid data'}), 400

    workflow = AutomationService.create_workflow(
        name=data['name'],
        triggers=data['triggers'],
        actions=data['actions']
    )

    return jsonify({'message': 'Workflow created successfully', 'workflow': workflow}), 201

@automation_bp.route('/automation/workflow/<int:workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """
    Get details of an automation workflow.
    """
    workflow = AutomationService.get_workflow(workflow_id)

    if not workflow:
        return jsonify({'message': 'Workflow not found'}), 404

    return jsonify({'workflow': workflow}), 200

@automation_bp.route('/automation/workflow/<int:workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    """
    Update an automation workflow.
    """
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    updated_workflow = AutomationService.update_workflow(workflow_id, data)

    if not updated_workflow:
        return jsonify({'message': 'Workflow not found or update failed'}), 404

    return jsonify({'message': 'Workflow updated successfully', 'workflow': updated_workflow}), 200

@automation_bp.route('/automation/workflow/<int:workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    """
    Delete an automation workflow.
    """
    success = AutomationService.delete_workflow(workflow_id)

    if not success:
        return jsonify({'message': 'Workflow not found or delete failed'}), 404

    return jsonify({'message': 'Workflow deleted successfully'}), 200
