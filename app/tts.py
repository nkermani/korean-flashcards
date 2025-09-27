from gtts import gTTS
import os
import random

def generate_tts(word: str, audio_dir: str) -> str:
    """Generate TTS audio for a word and return the file path."""
    filename = f"{word.lower()}_{random.randint(1000, 9999)}.mp3"
    filepath = os.path.join(audio_dir, filename)
    tts = gTTS(text=word, lang="ko")
    tts.save(filepath)
    return filepath
