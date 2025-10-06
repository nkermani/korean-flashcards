# app/config.py
# This module handles configuration settings, including loading environment variables and setting up directories.

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    # Don't raise at import time; some test environments may mock network
    # interactions and therefore don't require a real API key. Log a warning
    # instead so callers can decide how to behave.
    print(
        "[app.config] Warning: MISTRAL_API_KEY not set; Mistral client will be disabled unless provided at runtime"
    )

AUDIO_DIR = "tts_audio"
DATA_DIR = "saved_flashcards"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
