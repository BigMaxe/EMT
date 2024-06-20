from flask import Blueprint, request, jsonify
from app.models.ab_testing import ABTest, ABTestResult
from app import db
from datetime import datetime

ab_testing_bp = Blueprint('ab_testing', __name__)

@ab_testing_bp.route('/ab_tests', methods=['POST'])
def create_ab_test():
    """
    Create a new A/B test.
    """
    data = request.get_json()

    if not data or not 'name' in data or not 'variants' in data:
        return jsonify({'message': 'Invalid data'}), 400

    ab_test = ABTest(
        name=data['name'],
        description=data.get('description'),
        variants=data['variants'],
        created_at=datetime.utcnow()
    )

    db.session.add(ab_test)
    db.session.commit()

    return jsonify({'message': 'A/B test created successfully', 'id': ab_test.id}), 201

@ab_testing_bp.route('/ab_tests/<int:test_id>', methods=['GET'])
def get_ab_test(test_id):
    """
    Get an A/B test by ID.
    """
    ab_test = ABTest.query.get_or_404(test_id)
    return jsonify({
        'id': ab_test.id,
        'name': ab_test.name,
        'description': ab_test.description,
        'variants': ab_test.variants,
        'created_at': ab_test.created_at
    })

@ab_testing_bp.route('/ab_tests/<int:test_id>/results', methods=['POST'])
def record_ab_test_result(test_id):
    """
    Record a result for an A/B test.
    """
    data = request.get_json()

    if not data or not 'variant' in data or not 'conversion' in data:
        return jsonify({'message': 'Invalid data'}), 400

    ab_test = ABTest.query.get_or_404(test_id)

    if data['variant'] not in ab_test.variants:
        return jsonify({'message': 'Invalid variant'}), 400

    result = ABTestResult(
        test_id=test_id,
        variant=data['variant'],
        conversion=data['conversion'],
        recorded_at=datetime.utcnow()
    )

    db.session.add(result)
    db.session.commit()

    return jsonify({'message': 'A/B test result recorded successfully'}), 201

@ab_testing_bp.route('/ab_tests/<int:test_id>/results', methods=['GET'])
def get_ab_test_results(test_id):
    """
    Get results for an A/B test.
    """
    ab_test = ABTest.query.get_or_404(test_id)
    results = ABTestResult.query.filter_by(test_id=test_id).all()

    response = {
        'id': ab_test.id,
        'name': ab_test.name,
        'description': ab_test.description,
        'variants': ab_test.variants,
        'results': []
    }

    for result in results:
        response['results'].append({
            'variant': result.variant,
            'conversion': result.conversion,
            'recorded_at': result.recorded_at
        })

    return jsonify(response)
