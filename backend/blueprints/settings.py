# Handles visibility and access configurations

from flask import Blueprint, request, jsonify
from main import SessionLocal
from models.models import Settings

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/', methods=['GET'])
def get_settings():
    session = SessionLocal()
    settings = session.query(Settings).all()
    session.close()
    return jsonify([{
        "id": setting.id,
        "visibility": setting.visibility,
        "access_level": setting.access_level
    } for setting in settings])

@settings_bp.route('/update', methods=['POST'])
def update_settings():
    session = SessionLocal()
    data = request.get_json()
    setting = session.query(Settings).first()  # Assuming one settings row
    setting.visibility = data.get('visibility', setting.visibility)
    setting.access_level = data.get('access_level', setting.access_level)
    session.commit()
    session.close()
    return jsonify({"message": "Settings updated successfully"}), 200
