# Main entry point to run the app
from pathlib import Path
import json
from flask import Flask, request, jsonify
from functions import classify_input, generate_chat_response, generate_advice
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Load categories to match frontend structure
categories = {
    "underused_skills": "Under-use of Skills",
    "excessive_workload": "Excessive Workload",
    "long_hours": "Long, Unsocial or Inflexible Hours",
    "lack_of_control": "Lack of Control Over Job Design",
    "unsafe_conditions": "Unsafe or Poor Physical Conditions",
    "negative_culture": "Negative Organizational Culture",
    "limited_support": "Limited Support from Colleagues",
    "violence_harassment": "Violence, Harassment, or Bullying",
    "discrimination": "Discrimination and Exclusion",
    "unclear_role": "Unclear Job Role",
    "under_promotion": "Under- or Over-promotion",
    "job_insecurity": "Job Insecurity or Inadequate Pay",
    "work_home_conflict": "Conflicting Home/Work Demands"
}

@app.route('/classify_feedback', methods=['POST'])
def classify_feedback():
    data = request.json
    content = data.get("content")

    if not content:
        return jsonify({"error": "No content provided"}), 400

    # Call the classify_input function to get category and sentiment
    response = classify_input(content, categories)

    # Ensure response is a dictionary, not a string
    print("User input:", content, "Response:", response)  # This should be a dictionary

    # Return the category and sentiment as JSON
    return jsonify(response)


@app.route('/get_chat_response', methods=['POST'])
def get_chat_response():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"response": "I'm here to chat! Please ask me something."}), 400

    # Generate a response using the separate function
    bot_response = generate_chat_response(user_message)
    return jsonify({"response": bot_response})


@app.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.json
    issue_details = data.get("issue")

    if not issue_details:
        return jsonify({"response": "No issue details were sent!"}), 400

    # Generate a response using the separate function
    advice = generate_advice(issue_details)
    # Ensure response is a dictionary, not a string
    print("Issue input:", issue_details, "Response:", advice)  # This should be a dictionary

    return jsonify({"advice": advice})




if __name__ == '__main__':
    app.run(debug=True)
