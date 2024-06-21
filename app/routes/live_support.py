from flask import Blueprint, request, jsonify
from app import db
from app.models.live_support import LiveSupportSession, Message
from datetime import datetime

live_support_bp = Blueprint('live_support', __name__)

# Get all live support sessions
@live_support_bp.route('/live_support_sessions', methods=['GET'])
def get_live_support_sessions():
    sessions = LiveSupportSession.query.all()
    return jsonify([session.to_dict() for session in sessions]), 200

# Get a single live support session by ID
@live_support_bp.route('/live_support_session/<int:session_id>', methods=['GET'])
def get_live_support_session(session_id):
    session = LiveSupportSession.query.get_or_404(session_id)
    return jsonify(session.to_dict()), 200

# Create a new live support session
@live_support_bp.route('/live_support_session', methods=['POST'])
def create_live_support_session():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    session = LiveSupportSession(
        user_id=data['user_id'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(session)
    db.session.commit()
    return jsonify(session.to_dict()), 201

# Add a message to a live support session
@live_support_bp.route('/live_support_session/<int:session_id>/message', methods=['POST'])
def add_message(session_id):
    session = LiveSupportSession.query.get_or_404(session_id)
    data = request.get_json()
    if not data or 'sender_id' not in data or 'content' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    message = Message(
        session_id=session.id,
        sender_id=data['sender_id'],
        content=data['content'],
        timestamp=datetime.utcnow()
    )
    session.updated_at = datetime.utcnow()
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

# End a live support session
@live_support_bp.route('/live_support_session/<int:session_id>', methods=['DELETE'])
def end_live_support_session(session_id):
    session = LiveSupportSession.query.get_or_404(session_id)
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Live support session ended successfully'}), 200
