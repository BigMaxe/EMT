from flask import Blueprint, request, jsonify
from app import db
from app.models.white_label import WhiteLabelSettings
from werkzeug.utils import secure_filename
import os

white_label_bp = Blueprint('white_label', __name__)

UPLOAD_FOLDER = 'uploads/white_label'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@white_label_bp.route('/settings', methods=['GET'])
def get_white_label_settings():
    settings = WhiteLabelSettings.query.first()
    if not settings:
        return jsonify({'message': 'No white-label settings found'}), 404
    return jsonify(settings.to_dict()), 200

@white_label_bp.route('/settings', methods=['POST'])
def update_white_label_settings():
    data = request.form
    settings = WhiteLabelSettings.query.first()
    if not settings:
        settings = WhiteLabelSettings()

    settings.brand_name = data.get('brand_name', settings.brand_name)
    settings.theme_color = data.get('theme_color', settings.theme_color)
    settings.contact_email = data.get('contact_email', settings.contact_email)

    if 'logo' in request.files:
        file = request.files['logo']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        settings.logo_path = filepath

    db.session.add(settings)
    db.session.commit()
    return jsonify({'message': 'White-label settings updated successfully'}), 200

@white_label_bp.route('/settings/logo', methods=['GET'])
def get_logo():
    settings = WhiteLabelSettings.query.first()
    if not settings or not settings.logo_path:
        return jsonify({'message': 'No logo found'}), 404
    return send_file(settings.logo_path, as_attachment=False)
