from vertexai.preview.language_models import TextGenerationModel
from vertexai.generative_models import GenerativeModel, GenerationConfig
import vertexai
import json
from pathlib import Path
from backend import config

project_name = config['PROJECT_NAME']


def load_examples():
    examples = []
    labels = []

    # Load chat examples
    chat_files = Path("examples/chats").glob("*.txt")
    for file_path in chat_files:
        with open(file_path, "r") as file:
            examples.append(file.read())
            labels.append("Chat")

    # Load meeting examples
    meeting_files = Path("examples/meetings").glob("*.txt")
    for file_path in meeting_files:
        with open(file_path, "r") as file:
            examples.append(file.read())
            labels.append("Meeting")

    return examples, labels


def classify_issue(data: str) -> str:
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

    # Generate the classification response
    response = model.generate_content(
        prompt=prompt,
        generation_config=generation_config
    )

    return response.text


# Example usage:
if __name__ == "__main__":
    # Load some example data
    examples, labels = load_examples()
    # You could iterate over or randomly select examples
    sample_data = examples[0]

    # Classify the sample issue
    classification_result = classify_issue(sample_data)
    print("Classification Result:", classification_result)
