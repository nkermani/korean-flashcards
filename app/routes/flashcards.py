# app/routes/flashcards.py
# This module defines the routes related to flashcards, including creating new flashcards.

from fastapi import APIRouter, Body, HTTPException
from starlette.concurrency import run_in_threadpool
from app.config import DATA_DIR
from app.services.flashcard_service import create_flashcards_service, export_to_anki
from typing import Optional
import json
import os

router = APIRouter()


@router.post("/flashcards/export/anki")
async def export_flashcards_to_anki(data: dict = Body(...)):
    try:
        # Run the synchronous service in a threadpool so we don't block or misuse
        # the event loop (create_flashcards_service performs blocking I/O and
        # may call synchronous helpers that use run_until_complete).
        result = await run_in_threadpool(create_flashcards_service, data)

        # Fetch the flashcards from the saved file
        topic_file = os.path.join(DATA_DIR, result["file"])
        with open(topic_file, "r", encoding="utf-8") as f:
            flashcards = json.load(f)

        # Export to Anki
        output_path = export_to_anki(flashcards)

        return {
            "message": "Flashcards exported to Anki successfully!",
            "anki_file": output_path,
            "total_cards": len(flashcards),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to export flashcards: {str(e)}"
        )


@router.post("/flashcards")
async def create_flashcards(data: dict = Body(...)):
    try:
        # Run the synchronous service in the threadpool to avoid calling
        # run_until_complete on the server event loop.
        result = await run_in_threadpool(create_flashcards_service, data)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
