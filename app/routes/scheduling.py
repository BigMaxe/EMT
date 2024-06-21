from flask import Blueprint, request, jsonify
from app import db
from app.models.scheduling import Schedule
from datetime import datetime

scheduling_bp = Blueprint('scheduling', __name__)

# Get all scheduled emails
@scheduling_bp.route('/schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.all()
    return jsonify([schedule.to_dict() for schedule in schedules]), 200

# Get a single scheduled email by ID
@scheduling_bp.route('/schedule/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    return jsonify(schedule.to_dict()), 200

# Create a new scheduled email
@scheduling_bp.route('/schedule', methods=['POST'])
def create_schedule():
    data = request.get_json()
    if not data or 'email_id' not in data or 'send_at' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    try:
        send_at = datetime.strptime(data['send_at'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    schedule = Schedule(
        email_id=data['email_id'],
        send_at=send_at,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify(schedule.to_dict()), 201

# Update a scheduled email
@scheduling_bp.route('/schedule/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400

    if 'email_id' in data:
        schedule.email_id = data['email_id']
    if 'send_at' in data:
        try:
            schedule.send_at = datetime.strptime(data['send_at'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400

    schedule.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(schedule.to_dict()), 200

# Delete a scheduled email
@scheduling_bp.route('/schedule/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule deleted successfully'}), 200
