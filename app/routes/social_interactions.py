from flask import Blueprint, request, jsonify
from app import db
from app.models.social_interactions import SocialInteraction
from datetime import datetime

social_interactions_bp = Blueprint('social_interactions', __name__)

# Get all social interactions
@social_interactions_bp.route('/interactions', methods=['GET'])
def get_interactions():
    interactions = SocialInteraction.query.all()
    return jsonify([interaction.to_dict() for interaction in interactions]), 200

# Get a single social interaction by ID
@social_interactions_bp.route('/interaction/<int:interaction_id>', methods=['GET'])
def get_interaction(interaction_id):
    interaction = SocialInteraction.query.get_or_404(interaction_id)
    return jsonify(interaction.to_dict()), 200

# Create a new social interaction
@social_interactions_bp.route('/interaction', methods=['POST'])
def create_interaction():
    data = request.get_json()
    if not data or 'platform' not in data or 'content' not in data or 'timestamp' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    try:
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    interaction = SocialInteraction(
        platform=data['platform'],
        content=data['content'],
        timestamp=timestamp,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(interaction)
    db.session.commit()
    return jsonify(interaction.to_dict()), 201

# Update a social interaction
@social_interactions_bp.route('/interaction/<int:interaction_id>', methods=['PUT'])
def update_interaction(interaction_id):
    interaction = SocialInteraction.query.get_or_404(interaction_id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    if 'platform' in data:
        interaction.platform = data['platform']
    if 'content' in data:
        interaction.content = data['content']
    if 'timestamp' in data:
        try:
            interaction.timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400

    interaction.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(interaction.to_dict()), 200

# Delete a social interaction
@social_interactions_bp.route('/interaction/<int:interaction_id>', methods=['DELETE'])
def delete_interaction(interaction_id):
    interaction = SocialInteraction.query.get_or_404(interaction_id)
    db.session.delete(interaction)
    db.session.commit()
    return jsonify({'message': 'Interaction deleted successfully'}), 200
