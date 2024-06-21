from flask import Blueprint, jsonify, request, send_file
from flask_mail import Message
from app import mail
import random
import string
import hashlib
import os
import shortuuid
from werkzeug.utils import secure_filename
from PIL import Image
import jsonschema
import json
from cryptography.fernet import Fernet

utils_bp = Blueprint('utils', __name__)

# Generate random string
@utils_bp.route('/generate_random_string', methods=['GET'])
def generate_random_string():
    length = request.args.get('length', default=8, type=int)
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return jsonify({'random_string': random_str}), 200

# Send email
@utils_bp.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    if not data or 'recipient' not in data or 'subject' not in data or 'body' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    msg = Message(
        subject=data['subject'],
        recipients=[data['recipient']],
        body=data['body'],
        sender=os.getenv('MAIL_DEFAULT_SENDER')
    )

    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to send email: {e}'}), 500

# Hash string
@utils_bp.route('/hash_string', methods=['POST'])
def hash_string():
    data = request.get_json()
    if not data or 'string_to_hash' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    hash_object = hashlib.sha256(data['string_to_hash'].encode())
    hex_dig = hash_object.hexdigest()
    return jsonify({'hashed_string': hex_dig}), 200

# URL shortening
@utils_bp.route('/shorten_url', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    shortened_url = shortuuid.uuid(name=data['url'])
    return jsonify({'shortened_url': shortened_url}), 200

# File upload
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@utils_bp.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

# File download
@utils_bp.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

# Image processing
@utils_bp.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        img = Image.open(file)
        img = img.convert('RGB')
        processed_image_path = os.path.join(UPLOAD_FOLDER, f"processed_{filename}")
        img.save(processed_image_path)
        return send_file(processed_image_path, as_attachment=True)

# JSON validation
@utils_bp.route('/validate_json', methods=['POST'])
def validate_json():
    data = request.get_json()
    schema = data.get('schema')
    instance = data.get('instance')

    if not schema or not instance:
        return jsonify({'message': 'Invalid data'}), 400

    try:
        jsonschema.validate(instance=instance, schema=schema)
        return jsonify({'message': 'JSON is valid'}), 200
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'message': f'JSON validation error: {e.message}'}), 400

# Data encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@utils_bp.route('/encrypt_data', methods=['POST'])
def encrypt_data():
    data = request.get_json()
    if not data or 'data_to_encrypt' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    encrypted_data = cipher_suite.encrypt(data['data_to_encrypt'].encode())
    return jsonify({'encrypted_data': encrypted_data.decode()}), 200

# Data decryption
@utils_bp.route('/decrypt_data', methods=['POST'])
def decrypt_data():
    data = request.get_json()
    if not data or 'data_to_decrypt' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    decrypted_data = cipher_suite.decrypt(data['data_to_decrypt'].encode())
    return jsonify({'decrypted_data': decrypted_data.decode()}), 200

# Placeholder for additional utilities
