# app/routes/flashcards.py
# This module defines the routes related to flashcards, including creating new flashcards.

from fastapi import APIRouter, Body, HTTPException
from services.flashcard_service import create_flashcards_service

router = APIRouter()


@router.post("/flashcards")
async def create_flashcards(data: dict = Body(...)):
    try:
        result = create_flashcards_service(data)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
