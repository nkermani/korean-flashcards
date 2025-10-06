import pytest
import unittest
import json
from app.mistral_client import call_mistral_with_retry
from app.services.flashcard_service import create_flashcards_service, export_to_anki
from unittest.mock import AsyncMock, patch, MagicMock
import os
import pandas as pd
import tempfile
from datetime import datetime

def test_create_flashcards_service():
    # Mock Mistral API response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '''
    [
        {
            "word": "안녕하세요",
            "definition": "Hello in Korean",
            "example": "안녕하세요, 어떻게 지내세요?",
            "synonyms": ["여보세요", "반갑습니다"],
            "antonyms": ["안녕", "잘 가"]
        }
    ]
    '''

    # Create a fixed datetime object
    fixed_datetime = datetime(2023, 10, 1, 12, 0, 0)

    # Mock the file operations
    mock_file = MagicMock()

    with patch('app.services.flashcard_service.call_mistral_with_retry', return_value=mock_response), \
         patch('app.services.flashcard_service.generate_tts', return_value="/fake/path/안녕하세요.mp3"), \
         patch('app.services.flashcard_service.get_topic_file', return_value=None), \
         patch('app.services.flashcard_service.os.path.exists', return_value=False), \
         patch('builtins.open', return_value=mock_file), \
         patch('json.dump') as mock_json_dump:

        # Pass the fixed datetime to the function
        result = create_flashcards_service({"topic": "greetings"}, now=fixed_datetime)

        # Verify the result
        assert "topic" in result
        assert result["topic"] == "greetings"
        assert "added" in result
        assert len(result["added"]) == 1
        assert result["added"][0] == "안녕하세요"

        # Verify json.dump was called twice (once for flashcards, once for history)
        assert mock_json_dump.call_count == 2

        # Verify the calls to json.dump
        calls = mock_json_dump.call_args_list

        # First call should be for flashcards
        flashcards_call = calls[0]
        assert len(flashcards_call[0][0]) == 1  # One flashcard
        assert flashcards_call[0][0][0]["word"] == "안녕하세요"

        # Second call should be for history
        history_call = calls[1]
        assert "greetings" in history_call[0][0]
        assert history_call[0][0]["greetings"]["filename"].endswith(".json")


def test_export_to_anki():
    flashcards = [
        {
            "word": "안녕하세요",
            "definition": "Hello in Korean",
            "example": "안녕하세요, 어떻게 지내세요?",
            "synonyms": ["여보세요", "반갑습니다"],
            "antonyms": ["안녕", "잘 가"],
            "tts_path": "/fake/path/안녕하세요.mp3"
        }
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = export_to_anki(flashcards, output_dir=temp_dir)

        assert os.path.exists(output_path)
        df = pd.read_csv(output_path)
        assert len(df) == 1
        assert df.iloc[0]["Front"] == "안녕하세요"
        assert "Hello in Korean" in df.iloc[0]["Back"]


@pytest.mark.asyncio
async def test_call_mistral_with_retry():
    # Mock the async Mistral client call
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = '''
    [
        {
            "word": "안녕하세요",
            "definition": "Hello in Korean",
            "example": "안녕하세요, 어떻게 지내세요?",
            "synonyms": ["여보세요", "반갑습니다"],
            "antonyms": ["안녕", "잘 가"]
        }
    ]
    '''

    # Patch the internal async helper used by call_mistral_with_retry's single-arg form
    with patch('app.mistral_client._async_call_with_retry', return_value=mock_response):
        response = await call_mistral_with_retry("test prompt")
        assert response.choices[0].message.content is not None
