import os

from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Access the environment variables
FLASK_KEY = os.getenv("FLASK_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")
# FIREBASE_KEY = os.getenv('FIREBASE_KEY')

# Set the default name and photo for a user
DEFAULT_NAME = "Mivro User"
DEFAULT_PHOTO = "https://images.pexels.com/photos/756856/pexels-photo-756856.jpeg"
