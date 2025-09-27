import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise RuntimeError("Missing MISTRAL_API_KEY in .env file")

AUDIO_DIR = "tts_audio"
DATA_DIR = "saved_flashcards"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
