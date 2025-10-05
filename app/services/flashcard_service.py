# app/services/flashcard_service.py
# This module contains the service logic for creating flashcards using the Mistral API,
# generating TTS audio, saving flashcards to files, and updating history.

from mistralai import Mistral
from config import api_key, AUDIO_DIR, DATA_DIR, HISTORY_FILE
from mistral_client import call_mistral_with_retry
from tts import generate_tts
from history import load_history, save_history
from flashcard_utils import get_topic_file, parse_flashcards
from datetime import datetime
import json
import os
import re

client = Mistral(api_key=api_key)

def create_flashcards_service(data: dict):
    # normalize topic: lowercase, trim, replace whitespace with underscores
    raw_topic = data.get("topic", "general") or "general"
    topic = re.sub(r"\s+", "_", raw_topic.strip().lower())
    prompt = f"""
    Create 5 flashcards to help a student learn faster about the topic in KOREAN "{topic}".
    Each flashcard must be a JSON object with:
    - word
    - definition
    - example
    - synonyms (at least 2)
    - antonyms (at least 2)
    Return a JSON array of 5 such flashcards.
    """
    try:
        response = call_mistral_with_retry(client, prompt)
        text = response.choices[0].message.content
        flashcards = parse_flashcards(text)
    except Exception as e:
        raise e

    for card in flashcards:
        card["tts_path"] = generate_tts(card["word"], AUDIO_DIR)

    topic_file = get_topic_file(topic, DATA_DIR)
    if topic_file and os.path.exists(topic_file):
        with open(topic_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        topic_file = os.path.join(DATA_DIR, f"{topic}_{timestamp}.json")
        existing = []

    existing_words = {c["word"] for c in existing}
    new_cards = [c for c in flashcards if c["word"] not in existing_words]
    existing.extend(new_cards)

    with open(topic_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    history = load_history(HISTORY_FILE)
    now = datetime.now().isoformat(timespec="seconds")
    if topic not in history:
        history[topic] = {
            "filename": os.path.basename(topic_file),
            "created_at": now,
            "updated_at": now,
            "count": len(existing),
        }
    else:
        history[topic]["updated_at"] = now
        history[topic]["count"] = len(existing)
    save_history(history, HISTORY_FILE)

    return {
        "topic": topic,
        "added": [c["word"] for c in new_cards],
        "file": os.path.basename(topic_file),
        "total_cards": len(existing),
    }
