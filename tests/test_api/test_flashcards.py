import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app
from unittest.mock import patch, MagicMock


client = TestClient(app)

def test_create_flashcards():
    # Mock the Mistral API call
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

    with patch('app.services.flashcard_service.call_mistral_with_retry', return_value=mock_response), \
         patch('app.services.flashcard_service.generate_tts', return_value="/fake/path.mp3"), \
         patch('app.services.flashcard_service.get_topic_file', return_value=None), \
         patch('app.services.flashcard_service.os.path.exists', return_value=False), \
         patch('builtins.open', create=True) as mock_open, \
         patch('json.dump') as mock_json_dump:

        response = client.post("/flashcards", json={"topic": "greetings"})

        assert response.status_code == 200
        data = response.json()
        assert "topic" in data
        assert data["topic"] == "greetings"
        assert "added" in data
        assert len(data["added"]) > 0

@pytest.mark.asyncio
async def test_create_flashcards_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create a local mock_response for the async test
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

        with patch('app.services.flashcard_service.call_mistral_with_retry', return_value=mock_response), \
             patch('app.services.flashcard_service.generate_tts', return_value="/fake/path.mp3"), \
             patch('app.services.flashcard_service.get_topic_file', return_value=None), \
             patch('app.services.flashcard_service.os.path.exists', return_value=False), \
             patch('builtins.open', create=True) as mock_open, \
             patch('json.dump') as mock_json_dump:

            response = await ac.post("/flashcards", json={"topic": "greetings"})
            assert response.status_code == 200
            data = response.json()
            assert "topic" in data
            assert data["topic"] == "greetings"
