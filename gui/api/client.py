import os
import requests
import json

API_BASE = os.environ.get("MISTRAL_API_URL", "http://localhost:8000")

def fetch_saved_flashcards():
    """
    Return a list of filenames found in gui/../saved_flashcards (JSON files).
    Non-blocking and safe if the folder doesn't exist.
    """
    folder = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "saved_flashcards"))
    try:
        if not os.path.isdir(folder):
            return []
        files = [f for f in os.listdir(folder) if f.lower().endswith(".json")]
        return sorted(files)
    except Exception:
        return []

def _find_cards(obj):
    """Recursively find and return the first list of dicts (cards) in obj, or None."""
    if obj is None:
        return None
    if isinstance(obj, list):
        # return list of dicts (cards)
        if obj and all(isinstance(i, dict) for i in obj):
            return obj
        # if list contains lists, try to find dict-list inside
        for item in obj:
            found = _find_cards(item)
            if found:
                return found
        return None
    if isinstance(obj, dict):
        # If dict looks like a single card, wrap and return
        for card_key in ("word", "front", "term", "definition", "def"):
            if card_key in obj:
                return [obj]
        # otherwise scan values for a list of dicts
        for v in obj.values():
            found = _find_cards(v)
            if found:
                return found
    return None

def generate_flashcards(topic):
    """
    Request flashcards from backend POST /flashcards.
    Returns list[dict] or [] on failure. Tries to extract nested lists if response is a dict.
    """
    if not topic:
        return []

    url = f"{API_BASE}/flashcards"
    payload = {"topic": topic}
    try:
        print(f"[gui.api.client] POST {url} payload={payload}")
        resp = requests.post(url, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        # Debug-print actual response to help diagnose shapes
        try:
            print("[gui.api.client] response body:", json.dumps(data, ensure_ascii=False)[:1000])
        except Exception:
            print("[gui.api.client] response non-serializable, type:", type(data))

        # Direct list => good
        if isinstance(data, list):
            return data

        # If dict, try common keys then recursive search
        if isinstance(data, dict):
            for key in ("cards", "flashcards", "items", "results", "data"):
                if key in data and isinstance(data[key], list):
                    return data[key]
            found = _find_cards(data)
            if found:
                return found
            # single-card dict => wrap
            if any(k in data for k in ("word", "front", "term", "definition", "def")):
                return [data]

        print(f"[gui.api.client] unexpected response shape: {type(data)}")
    except requests.HTTPError as e:
        print("[gui.api.client] HTTP error:", e)
    except Exception as e:
        print("[gui.api.client] request failed:", e)
    return []
