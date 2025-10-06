# app/services/flashcard_service.py
# This module contains the service logic for creating flashcards using the Mistral API,
# generating TTS audio, saving flashcards to files, and updating history.

from app.config import api_key, AUDIO_DIR, DATA_DIR, HISTORY_FILE
from app.mistral_client import call_mistral_with_retry
from app.tts import generate_tts
from app.history import load_history, save_history
from app.flashcard_utils import get_topic_file, parse_flashcards
from datetime import datetime
import json
import pandas as pd
import os
import re


def export_to_anki(
    flashcards: list[dict],
    output_dir: str = " anki_exports",
    filename: str = "flashcards.csv",
):
    """Export flashcards to a CSV file compatible with Anki import.
    Args:
        flashcards: list of flashcard dictionaries.
        output_dir: directory to save the csv file.
        filemname: name of the csv file.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    anki_data = []
    for card in flashcards:
        anki_data.append(
            {
                "Front": card["word"],
                "Back": f"{card['definition']}<br><br><b>Example:</b> {card.get('example', '')}<br><br><b>Synonyms:</b> {', '.join(card.get('synonyms', []))}<br><br><b>Antonyms:</b> {', '.join(card.get('antonyms', []))}",
                "Audio": (
                    f"[sound:{os.path.basename(card.get('tts_path', ''))}]"
                    if card.get("tts_path")
                    else ""
                ),
            }
        )

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(anki_data)
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)

    return output_path


def create_flashcards_service(data: dict, now=None, client=None):
    # If now is not provided, use current datetime
    if now is None:
        now = datetime.now()

    # Use now instead of datetime.now() in your function
    timestamp = now.strftime("%Y%m%d%H%M%S")
    isoformat = now.isoformat(timespec="seconds")

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
        # call_mistral_with_retry supports two calling conventions:
        # - synchronous: call_mistral_with_retry(client, prompt)
        # - async: await call_mistral_with_retry(prompt)
        # In the service we prefer the synchronous form; tests patch
        # call_mistral_with_retry directly so client may be None in tests.
        if client is None:
            resp = call_mistral_with_retry(prompt)
            # resp may be a coroutine when the single-arg async path is returned
            if hasattr(resp, "__await__"):
                # run synchronously for tests / threadpool by creating a fresh event loop
                import asyncio

                try:
                    resp = asyncio.run(resp)
                except RuntimeError:
                    # fallback for unusual environments: create a new loop explicitly
                    loop = asyncio.new_event_loop()
                    try:
                        resp = loop.run_until_complete(resp)
                    finally:
                        loop.close()
            response = resp
        else:
            response = call_mistral_with_retry(client, prompt)

        text = response.choices[0].message.content
        flashcards = parse_flashcards(text)
    except Exception as e:
        # Bubble up so callers can convert to HTTPException if needed
        raise

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
