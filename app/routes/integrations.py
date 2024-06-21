from flask import Blueprint, request, jsonify
from app import db
from app.models.integration import Integration
from datetime import datetime
import requests

integrations_bp = Blueprint('integrations', __name__)

# Get all integrations
@integrations_bp.route('/integrations', methods=['GET'])
def get_integrations():
    integrations = Integration.query.all()
    return jsonify([integration.to_dict() for integration in integrations]), 200

# Get a single integration by ID
@integrations_bp.route('/integration/<int:integration_id>', methods=['GET'])
def get_integration(integration_id):
    integration = Integration.query.get_or_404(integration_id)
    return jsonify(integration.to_dict()), 200

# Create a new integration
@integrations_bp.route('/integration', methods=['POST'])
def create_integration():
    data = request.get_json()
    if not data or 'name' not in data or 'settings' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    integration = Integration(
        name=data['name'],
        settings=data['settings'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(integration)
    db.session.commit()
    return jsonify(integration.to_dict()), 201

# Update an existing integration
@integrations_bp.route('/integration/<int:integration_id>', methods=['PUT'])
def update_integration(integration_id):
    integration = Integration.query.get_or_404(integration_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    integration.name = data.get('name', integration.name)
    integration.settings = data.get('settings', integration.settings)
    integration.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify(integration.to_dict()), 200

# Delete an integration
@integrations_bp.route('/integration/<int:integration_id>', methods=['DELETE'])
def delete_integration(integration_id):
    integration = Integration.query.get_or_404(integration_id)
    db.session.delete(integration)
    db.session.commit()
    return jsonify({'message': 'Integration deleted successfully'}), 200

# Test an integration
@integrations_bp.route('/integration/<int:integration_id>/test', methods=['POST'])
def test_integration(integration_id):
    integration = Integration.query.get_or_404(integration_id)
    settings = integration.settings

    try:
        # Example: Make an API call to the external service
        response = requests.post(
            url=settings['api_url'],
            headers={
                'Authorization': f"Bearer {settings['api_key']}",
                'Content-Type': 'application/json'
            },
            json={'test': True}
        )

        if response.status_code == 200:
            return jsonify({'message': 'Integration test successful', 'response': response.json()}), 200
        else:
            return jsonify({'message': 'Integration test failed', 'response': response.json()}), response.status_code

    except Exception as e:
        return jsonify({'message': 'Integration test failed', 'error': str(e)}), 500
