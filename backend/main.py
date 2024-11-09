# Main entry point to run the app
from pathlib import Path
import json
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from vertexai.preview.language_models import TextGenerationModel
from flask import Flask
from config import config
# Manages "Top Issues" and categorization by LLM
from flask import Blueprint, request, jsonify

app = Flask(__name__)
app.config.from_object('config')


# @app.route('/create', methods=['POST'])
# def create_issue():
#     session = SessionLocal()
#     data = request.get_json()

#     # Find the category by name or ID based on input
#     category = session.query(Category).filter_by(
#         name=data['category_name']).first()
#     if not category:
#         return jsonify({"message": "Category not found"}), 400

#     # Classify the issue to get content and department
#     classification_result = classify_issue(data['content'])
#     content = classification_result.get("Primary Issue", data['content'])
#     department = classification_result.get(
#         "Relevant Department(s)", data.get('department', 'Unknown'))

#     # Create the issue linked to the category
#     new_issue = Issue(
#         content=content,
#         department=department,
#         category_id=category.id,  # Linking to existing category
#         is_positive=data.get('is_positive', False),
#         ranking=data.get('ranking', 0)
#     )

#     session.add(new_issue)
#     session.commit()
#     session.close()
#     return jsonify({"message": "Issue created successfully"}), 201


# @app.route('/<int:id>', methods=['GET'])
# def get_issue(id):
#     session = SessionLocal()
#     issue = session.query(Issue).filter(Issue.id == id).first()
#     session.close()
#     if issue:
#         return jsonify({
#             "id": issue.id,
#             "content": issue.content,
#             "department": issue.department,
#             "category": issue.category.name,
#             "ranking": issue.ranking,
#             "is_positive": issue.is_positive
#         })
#     return jsonify({"message": "Issue not found"}), 404


# @app.route('/top', methods=['GET'])
# def get_top_issues():
#     session = SessionLocal()
#     top_issues = session.query(Issue).order_by(
#         Issue.ranking.desc()).limit(10).all()
#     session.close()
#     return jsonify([{
#         "id": issue.id,
#         "content": issue.content,
#         "ranking": issue.ranking
#     } for issue in top_issues])

project_name = config['PROJECT_NAME']


def load_examples():
    examples = []
    labels = []

    # Load chat examples
    chat_files = Path("backend/examples/chats").glob("*.txt")
    for file_path in chat_files:
        with open(file_path, "r") as file:
            examples.append(file.read())
            labels.append("Chat")

    # Load meeting examples
    meeting_files = Path("backend/examples/meetings").glob("*.txt")
    for file_path in meeting_files:
        with open(file_path, "r") as file:
            examples.append(file.read())
            labels.append("Meeting")

    return examples, labels


def classify_issue(data: str) -> dict:
    # Initialize Vertex AI with project details
    vertexai.init(project=project_name, location="us-central1")

    # Set the configuration for the generative model
    generation_config = GenerationConfig(
        max_output_tokens=2048,
        temperature=0.2,
        top_p=0.8,
        top_k=40
    )

    # Load the generative model
    model = GenerativeModel("gemini-1.5-flash-002")

    # Construct the prompt for the model
    prompt = f"""
    You are an AI assistant tasked with analyzing workplace issues based on the provided content.

    Instructions:
    1. Carefully read the provided text.
    2. Identify the main issue or problem being discussed in the content.
    3. Determine the department(s) or area(s) most relevant to this issue (e.g., HR, IT, Marketing).
    4. Provide a summary that categorizes the primary issue.

    Data:
    {json.dumps(data, indent=2)}

    Response Format:
    - Primary Issue: [Brief description of the main issue]
    - Relevant Department(s): [e.g., HR, IT, Marketing]

    Please analyze and categorize the main issue in this content based on the above instructions.
    """
    print("Asked the Ai to classify the issue")

    # Generate the classification response
    response = model.generate_content(
        prompt=prompt,
        generation_config=generation_config
    )

    # Parse the response into a structured format
    response_text = response.text.strip()

    # Example of parsing the response assuming the format is consistent
    primary_issue = None
    relevant_departments = []

    # Simple extraction of primary issue and department(s) based on the expected format
    lines = response_text.split("\n")
    for line in lines:
        if line.lower().startswith("primary issue:"):
            primary_issue = line.split(":", 1)[1].strip()
        elif line.lower().startswith("relevant department(s):"):
            departments = line.split(":", 1)[1].strip()
            relevant_departments = [dept.strip()
                                    for dept in departments.split(",")]

    # Return the classification as a dictionary
    return {
        # Fallback to original content if no issue found
        "Primary Issue": primary_issue if primary_issue else data,
        "Relevant Department(s)": relevant_departments if relevant_departments else ["Unknown"]
    }


if __name__ == '__main__':
    app.run(debug=True)
    print("Running main app")
    examples, labels = load_examples()
    print("Loaded Examples:", len(examples))
    sample_data = examples[0]
    classification_result = classify_issue(sample_data)

    print("Classification Result:", classification_result)
