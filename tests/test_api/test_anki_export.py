import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock, mock_open
import os
import json
import pandas as pd

client = TestClient(app)

def test_export_to_anki():
    # Mock data
    mock_flashcards = [
        {
            "word": "안녕하세요",
            "definition": "Hello in Korean",
            "example": "안녕하세요, 어떻게 지내세요?",
            "synonyms": ["여보세요", "반갑습니다"],
            "antonyms": ["안녕", "잘 가"],
            "tts_path": "/fake/path/안녕하세요.mp3"
        }
    ]

    # Mock the entire flow
    with patch('app.routes.flashcards.create_flashcards_service',
              return_value={"file": "greetings_20231001.json"}), \
         patch('builtins.open', new_callable=mock_open, read_data=json.dumps(mock_flashcards)), \
         patch('app.services.flashcard_service.export_to_anki',
              return_value="/fake/path/flashcards.csv"), \
         patch('json.load', return_value=mock_flashcards):  # Add this to mock json.load

        response = client.post("/flashcards/export/anki", json={"topic": "greetings"})

        # Print response for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "anki_file" in data
        assert data["total_cards"] == 1
