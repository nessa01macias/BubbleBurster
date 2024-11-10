from pathlib import Path
from vertexai.generative_models import GenerativeModel, GenerationConfig
from vertexai.preview.language_models import TextGenerationModel
from dotenv import load_dotenv
import vertexai
import json
import os
import re
import markdown


# Load environment variables from .env file
load_dotenv()

# Access the variable
project_name = os.getenv('PROJECT_NAME')

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

aava_services = {
    "burnout": {
        "service_name": "Masters of Recovery",
        "description": "Learn methods to recover both during and after the workday. Suitable for those struggling with stress, burnout, or athletes seeking better recovery.",
        "link": "https://www.aava.fi/en/online-coachings/masters-of-recovery/"
    },
    "nutrition": {
        "service_name": "Easy Nutrition",
        "description": "Build a balanced eating model without miracle diets. Ideal for those interested in the basics of nutrition, weight loss, or seeking clarity on nutrition.",
        "link": "https://www.aava.fi/en/online-coachings/easy-nutrition/"
    },
    "energy": {
        "service_name": "Energy for Work",
        "description": "Gain motivation and tools to improve work enthusiasm and well-being. Designed for anyone seeking more energy or showing early signs of burnout.",
        "link": "https://www.aava.fi/en/online-coachings/energy-for-work/"
    },
    "stress": {
        "service_name": "Psychological Flexibility",
        "description": "Learn techniques for managing emotions, thoughts, and reactions. Ideal for anyone looking to improve mental well-being or reduce anxiety.",
        "link": "https://www.aava.fi/en/online-coachings/psychological-flexibility/"
    },
    "wellbeing_basics": {
        "service_name": "Alphabets of Wellbeing",
        "description": "Understand the basics of sleep, nutrition, and exercise to make lasting lifestyle changes. Perfect for those interested in fundamental well-being practices.",
        "link": "https://www.aava.fi/en/online-coachings/alphabets-of-wellbeing/"
    },
    "exercise": {
        "service_name": "Start Exercising",
        "description": "Gain practical knowledge to improve fitness easily and anywhere. Suitable for anyone wanting to start exercising or master basics in endurance, strength, and flexibility.",
        "link": "https://www.aava.fi/en/online-coachings/start-exercising/"
    },
    "energy_management": {
        "service_name": "Keys to Energy Management",
        "description": "Learn to manage physical, social, and mental energy for improved endurance. Great for those seeking different approaches to enhance their well-being.",
        "link": "https://www.aava.fi/en/online-coachings/keys-to-energy-management/"
    },
    "sleep": {
        "service_name": "The Most Important Sleep",
        "description": "Understand techniques to improve both sleep quality and quantity, suitable for those looking to boost energy and improve recovery.",
        "link": "https://www.aava.fi/en/online-coachings/the-most-important-sleep/"
    }
}


def find_relevant_service(issue_details: str) -> dict:
    for keyword, service_info in aava_services.items():
        # Match whole words or close variations
        if re.search(rf'\b{keyword}\b', issue_details.lower()):
            return service_info
    return None


def classify_input(content: str, categories: dict) -> dict:
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
    2. From the following categories, select one and only one that the content belongs to:
    Categories: 
    {categories}
    3. Select a sentiment, either positive or negative, based on the overall tone of the content.
    4. Generate a brief and informative summary title for the following feedback content:

    Content:
    {json.dumps(content, indent=2)}

    Response Format:
    {{
        "category": "chosen category",
        "sentiment": "positive/negative",
        "summary": "short title of the issue"
    }}
    """

    try:
        # Generate the classification response
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        # Clean the response text to remove ```json and ```
        response_text = response.text.replace("```json", "").replace("```", "").strip()
        print("Cleaned AI response:", response_text)  # Log cleaned response for debugging

        if not response_text:
            return {"category": None, "sentiment": None, "error": "Empty response from AI model"}

        # Parse the response into a dictionary
        return json.loads(response_text)

    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return {"category": None, "sentiment": None, "error": f"JSON decode error: {e}"}
    except Exception as e:
        print("Error in AI classification:", str(e))
        return {"category": None, "sentiment": None, "error": str(e)}


def generate_chat_response(user_message: str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_name, location="us-central1")

    # Load the generative model
    model = GenerativeModel("gemini-1.5-flash-002")

    # Set the configuration for the generative model
    generation_config = GenerationConfig(
        max_output_tokens=150,
        temperature=0.5,
        top_p=0.9,
        top_k=40
    )

    # Construct the prompt for the chatbot
    prompt = f"You are a helpful assistant. Respond to the user's question or comment appropriately:\nUser: {user_message}\nBot:"

    try:
        # Generate response from the AI model
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        # Extract and return the bot's response text
        return response.text.strip()

    except Exception as e:
        print("Error generating chatbot response:", str(e))
        return "Sorry, I couldn't process that request."


def generate_advice(issue_details: str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_name, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")
    generation_config = GenerationConfig(
        max_output_tokens=500,
        temperature=0.5,
        top_p=0.9,
        top_k=40
    )

    # Construct Aava services summary
    services_description = "\n".join(
        f"{service['service_name']}: {service['description']} (Learn more: {service['link']})"
        for service in aava_services.values()
    )

    # Construct the prompt with explicit instructions for format and brevity
    prompt = (
        f"You are an AI assistant tasked with providing concise, structured advice on the following workplace issue:\n"
        f"{issue_details}\n\n"
        "Your response should be in this format:\n"
        "1. **Brief Analysis**: A short, factual analysis of the issue in one or two sentences.\n"
        "2. **Immediate Actions**: List 2-3 practical steps the individual can take right now to address the issue.\n"
        "3. **Relevant Aava Services**: If applicable, briefly recommend any relevant services from Aava Medical Centre that can provide additional support. Give the link where to find more information, example: https://www.aava.fi/en/online-coachings/masters-of-recovery\n"
        "4. **Final Advice**: Provide one or two sentences of general advice for handling the issue in the future.\n\n"
        "Relevant Aava Medical Centre services include:\n\n"
        f"{services_description}\n\n"
        "Respond concisely and directly."
    )

    # Generate advice
    try:
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        response_text = response.text.strip()
        
        # Convert markdown to HTML for frontend rendering
        advice_html = markdown.markdown(response_text)
        return advice_html

    except Exception as e:
        print("Error generating advice:", str(e))
        return "Sorry, I couldn't generate advice for this issue."
