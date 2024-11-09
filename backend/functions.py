from pathlib import Path
from vertexai.generative_models import GenerativeModel, GenerationConfig
from vertexai.preview.language_models import TextGenerationModel
from dotenv import load_dotenv
import vertexai
import json
import os

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
    2. From the following categories, select one or several that the content belongs to:
    Categories: 
    {categories}
    3. Select a sentiment, either positive or negative, based on the overall tone of the content.

    Content:
    {json.dumps(content, indent=2)}

    Response Format:
    {{
        "category": "chosen category",
        "sentiment": "positive/negative"
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
