# gui/main.py
# This is the entry point for the GUI application using Tkinter.

import tkinter as tk
from .ui.app import FlashcardUI


def run_app():
    root = tk.Tk()
    root.title("Mistral Flashcards")
    FlashcardUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
