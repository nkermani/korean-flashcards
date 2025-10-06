# app/services/saved_service.py
# This module contains the service logic for listing and retrieving saved flashcards.

import os
import json
from app.config import DATA_DIR


def list_saved_flashcards_service():
    files = sorted(os.listdir(DATA_DIR))
    return {"saved_flashcards": files}


def get_saved_flashcards_service(filename: str):
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            flashcards = json.load(f)
        return {"filename": filename, "flashcards": flashcards}
    return {"error": "file not found"}
