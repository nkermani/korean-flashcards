# app/flashcard_utils.py
# This module provides utility functions for handling flashcards, including parsing and file management.

import os
import json
import re
from datetime import datetime


def get_topic_file(topic: str, data_dir: str) -> str | None:
    """Return path of existing topic file or None if not found"""
    for f in os.listdir(data_dir):
        if f.startswith(topic + "_") and f.endswith(".json"):
            return os.path.join(data_dir, f)
    return None


def parse_flashcards(text: str) -> list[dict]:
    """Parse flashcards from Mistral API response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            json_str = re.search(r"\[.*\]", text, re.S).group(0)
            return json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Failed to parse flashcards: {str(e)}")
