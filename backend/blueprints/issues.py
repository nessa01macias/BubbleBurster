# Manages "Top Issues" and categorization by LLM

from flask import Blueprint, request, jsonify
from main import SessionLocal
from models.models import Issue, Category

issues_bp = Blueprint('issues', __name__)

from flask import Blueprint, request, jsonify
from main import SessionLocal
from models.models import Issue, Category

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/create', methods=['POST'])
def create_issue():
    session = SessionLocal()
    data = request.get_json()

    # Find the category by name or ID based on input
    category = session.query(Category).filter_by(name=data['category_name']).first()
    if not category:
        return jsonify({"message": "Category not found"}), 400

    # Create the issue linked to the category
    new_issue = Issue(
        content=data['content'],
        department=data['department'],
        category_id=category.id,  # Linking to existing category
        is_positive=data.get('is_positive', False),
        ranking=data.get('ranking', 0)
    )

    session.add(new_issue)
    session.commit()
    session.close()
    return jsonify({"message": "Issue created successfully"}), 201


@issues_bp.route('/<int:id>', methods=['GET'])
def get_issue(id):
    session = SessionLocal()
    issue = session.query(Issue).filter(Issue.id == id).first()
    session.close()
    if issue:
        return jsonify({
            "id": issue.id,
            "content": issue.content,
            "department": issue.department,
            "category": issue.category.name,
            "ranking": issue.ranking,
            "is_positive": issue.is_positive
        })
    return jsonify({"message": "Issue not found"}), 404

@issues_bp.route('/top', methods=['GET'])
def get_top_issues():
    session = SessionLocal()
    top_issues = session.query(Issue).order_by(Issue.ranking.desc()).limit(10).all()
    session.close()
    return jsonify([{
        "id": issue.id,
        "content": issue.content,
        "ranking": issue.ranking
    } for issue in top_issues])
