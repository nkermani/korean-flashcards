import os
import json
from datetime import datetime

def load_history(history_file: str) -> dict:
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history: dict, history_file: str) -> None:
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
