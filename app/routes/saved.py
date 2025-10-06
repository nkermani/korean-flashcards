# app/routes/saved.py
# This module defines the routes related to saved flashcards, including listing and retrieving saved flashcards

from fastapi import APIRouter
from app.services.saved_service import (
    list_saved_flashcards_service,
    get_saved_flashcards_service,
)

router = APIRouter()


@router.get("/flashcards/saved")
def list_saved_flashcards():
    return list_saved_flashcards_service()


@router.get("/flashcards/saved/{filename}")
def get_saved_flashcards(filename: str):
    return get_saved_flashcards_service(filename)
