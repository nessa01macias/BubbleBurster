# Handles company health metrics
from flask import Blueprint, jsonify
from main import SessionLocal
from models.models import Issue

health_bp = Blueprint('health', __name__)

# Helper function to calculate health metrics for a department
def calculate_department_health(session, department):
    issues = session.query(Issue).filter(Issue.department == department).all()
    positive_count = sum(1 for issue in issues if issue.is_positive)
    negative_count = sum(1 for issue in issues if not issue.is_positive)
    total_issues = positive_count + negative_count

    return {
        "department": department,
        "positive_issues": positive_count,
        "negative_issues": negative_count,
        "total_issues": total_issues,
        "health_score": positive_count / total_issues if total_issues > 0 else 0
    }

@health_bp.route('/department/<string:department>', methods=['GET'])
def get_department_health(department):
    session = SessionLocal()
    department_health = calculate_department_health(session, department)
    session.close()
    return jsonify(department_health)

@health_bp.route('/company', methods=['GET'])
def get_company_health():
    session = SessionLocal()
    
    # Fetch all departments
    departments = session.query(Issue.department).distinct().all()
    
    # Initialize counters for overall health metrics
    total_positive_issues = 0
    total_negative_issues = 0
    total_issues = 0
    department_health_list = []

    # Calculate health for each department
    for department in departments:
        dept_health = calculate_department_health(session, department[0])
        department_health_list.append(dept_health)
        total_positive_issues += dept_health["positive_issues"]
        total_negative_issues += dept_health["negative_issues"]
        total_issues += dept_health["total_issues"]

    # Calculate overall company health score
    company_health_score = total_positive_issues / total_issues if total_issues > 0 else 0

    session.close()
    
    return jsonify({
        "total_positive_issues": total_positive_issues,
        "total_negative_issues": total_negative_issues,
        "total_issues": total_issues,
        "company_health_score": company_health_score,
        "department_health_details": department_health_list
    })
