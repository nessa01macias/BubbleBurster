# Configuration settings (e.g., database URI)
from dotenv import load_dotenv, dotenv_values
import os

# Load environment variables from .env file
load_dotenv()

# Fallback to .env values if load_dotenv doesn't find them (for default values)
config = {
    **dotenv_values(".env"),  # load from the .env file
    **os.environ  # override with environment variables
}
