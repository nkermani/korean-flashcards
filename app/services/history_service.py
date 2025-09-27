from history import load_history
from config import HISTORY_FILE

def get_topic_history_service():
    history = load_history(HISTORY_FILE)
    return history
