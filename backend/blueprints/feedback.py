from flask import Blueprint, request, jsonify
from main import SessionLocal
from models.models import Feedback, Issue

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/submit', methods=['POST'])
def submit_feedback():
    session = SessionLocal()
    data = request.get_json()
    new_feedback = Feedback(
        content=data['content'],
        issue_id=data['issue_id'],
        anonymous=data.get('anonymous', False)
    )
    session.add(new_feedback)
    session.commit()
    session.close()
    return jsonify({"message": "Feedback submitted successfully"}), 201

@feedback_bp.route('/issue/<int:issue_id>', methods=['GET'])
def get_feedback_for_issue(issue_id):
    session = SessionLocal()
    feedback_list = session.query(Feedback).filter(Feedback.issue_id == issue_id).all()
    session.close()
    return jsonify([{
        "id": fb.id,
        "content": fb.content,
        "anonymous": fb.anonymous,
        "timestamp": fb.timestamp
    } for fb in feedback_list])
