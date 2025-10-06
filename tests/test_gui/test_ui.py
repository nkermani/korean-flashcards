import pytest
from unittest.mock import MagicMock, patch
from gui.ui.app import FlashcardUI
import tkinter as tk

def test_flashcard_ui_initialization():
    root = tk.Tk()
    ui = FlashcardUI(root)

    assert ui.root == root
    assert ui.flashcards == []
    assert ui.current_topic is None
    assert ui.card_index is None

    root.destroy()

def test_load_topic():
    root = tk.Tk()
    ui = FlashcardUI(root)

    # Mock the API call
    mock_flashcards = [
        {
            "topic": "greetings",
            "word": "안녕하세요",
            "definition": "Hello in Korean",
            "example": "안녕하세요, 어떻게 지내세요?",
            "synonyms": ["여보세요", "반갑습니다"],
            "antonyms": ["안녕", "잘 가"]
        }
    ]

    with patch('gui.ui.app.json.load', return_value=mock_flashcards), \
        patch('gui.ui.app.os.path.exists', return_value=True), \
        patch('builtins.open', create=True):

        ui.load_topic("greetings")

        assert ui.current_topic == "greetings"
        assert ui.card_index == 0
        assert ui.word_var.get() == "안녕하세요"

    root.destroy()
