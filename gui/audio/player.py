import subprocess
import simpleaudio as sa
import os
from tkinter import messagebox

def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 to WAV using ffmpeg."""
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", mp3_path, wav_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to convert audio: {e}")
        return False

def play_audio(mp3_path):
    """Convert MP3 to WAV and play the audio."""
    if not os.path.exists(mp3_path):
        messagebox.showerror("Error", "Audio file not found!")
        return
    wav_path = mp3_path.replace(".mp3", ".wav")
    if not os.path.exists(wav_path):
        if not convert_mp3_to_wav(mp3_path, wav_path):
            return
    try:
        wave_obj = sa.WaveObject.from_wave_file(wav_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to play audio: {e}")
