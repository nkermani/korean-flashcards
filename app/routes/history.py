from fastapi import APIRouter
from services.history_service import get_topic_history_service

router = APIRouter()

@router.get("/flashcards/history")
def get_topic_history():
    return get_topic_history_service()
