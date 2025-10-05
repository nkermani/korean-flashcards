# app/tts.py
# This module provides text-to-speech functionality using gTTS, including file management and reuse

from gtts import gTTS
import os
import random


def generate_tts(word: str, audio_dir: str) -> str:
    """Generate TTS audio for a word and return the file path.

    Reuse an existing file when any file in audio_dir has the same prefix
    before the first '_' (case-insensitive). Filenames keep the original
    pattern: "<word_lower>_<random>.mp3".
    """
    os.makedirs(audio_dir, exist_ok=True)
    orig_label = (word or "").lower().strip()

    # Look for existing file whose prefix before first '_' matches the word
    try:
        for fname in os.listdir(audio_dir):
            if not fname.lower().endswith(".mp3"):
                continue
            name_no_ext = os.path.splitext(fname)[0]
            prefix = name_no_ext.split("_", 1)[0]
            if prefix.lower() == orig_label:
                return os.path.join(audio_dir, fname)
    except FileNotFoundError:
        pass

    # No existing file — create a new one with the original naming scheme
    filename = f"{orig_label}_{random.randint(1000, 9999)}.mp3"
    filepath = os.path.join(audio_dir, filename)
    try:
        tts = gTTS(text=word, lang="ko")
        tts.save(filepath)
        return filepath
    except Exception:
        # cleanup partial file if created
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass
        raise
