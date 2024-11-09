# Tracks issue progress and management actions
from flask import Blueprint, request, jsonify
from main import SessionLocal
from models.models import Progress, Issue

progress_tracker_bp = Blueprint('progress', __name__)

@progress_tracker_bp.route('/issue/<int:issue_id>', methods=['GET'])
def get_progress_for_issue(issue_id):
    session = SessionLocal()
    progress_entries = session.query(Progress).filter(Progress.issue_id == issue_id).all()
    session.close()
    return jsonify([{
        "id": prog.id,
        "status": prog.status,
        "action_taken": prog.action_taken,
        "last_updated": prog.last_updated
    } for prog in progress_entries])

@progress_tracker_bp.route('/update', methods=['POST'])
def update_progress():
    session = SessionLocal()
    data = request.get_json()
    new_progress = Progress(
        issue_id=data['issue_id'],
        status=data['status'],
        action_taken=data.get('action_taken', "")
    )
    session.add(new_progress)
    session.commit()
    session.close()
    return jsonify({"message": "Progress updated successfully"}), 201
