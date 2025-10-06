# app/routes/history.py
# This module defines the routes related to flashcard history, including retrieving topic history.

from fastapi import APIRouter
from app.services.history_service import get_topic_history_service

router = APIRouter()


@router.get("/flashcards/history")
def get_topic_history():
    return get_topic_history_service()
