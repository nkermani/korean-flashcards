import tkinter as tk
from tkinter import font
from .widgets import create_label, create_button, create_entry, create_listbox
from ..api.client import fetch_saved_flashcards

def setup_layout(root,
                 load_topic_cb=None,
                 load_file_cb=None,
                 new_word_cb=None,
                 speak_cb=None):
    """Set up the main UI layout. Pass callback functions from app to avoid circular imports."""
    # Variables
    word_var = tk.StringVar()
    def_var = tk.StringVar()
    example_var = tk.StringVar()
    synonyms_var = tk.StringVar()
    antonyms_var = tk.StringVar()

    # Fonts
    bold_font = font.Font(family="Helvetica", size=16, weight="bold")

    # Labels
    create_label(root, "Word:", 0, 0, sticky="w")
    create_label(root, textvariable=word_var, row=0, column=1, sticky="w", font=bold_font)
    create_label(root, "Definition:", 1, 0, sticky="w")
    create_label(root, textvariable=def_var, row=1, column=1, sticky="w", wraplength=300)
    create_label(root, "Example:", 2, 0, sticky="w")
    create_label(root, textvariable=example_var, row=2, column=1, sticky="w", wraplength=300)
    create_label(root, "Synonyms:", 3, 0, sticky="w")
    create_label(root, textvariable=synonyms_var, row=3, column=1, sticky="w", wraplength=300)
    create_label(root, "Antonyms:", 4, 0, sticky="w")
    create_label(root, textvariable=antonyms_var, row=4, column=1, sticky="w", wraplength=300)

    # Buttons
    new_word_button = create_button(
        root,
        "🔁 New Word",
        5,
        0,
        state=tk.DISABLED,
        command=(lambda: new_word_cb() if new_word_cb else None)
    )
    speak_button = create_button(
        root,
        "🔊 Speak",
        5,
        1,
        state=tk.DISABLED,
        command=(lambda: speak_cb() if speak_cb else None)
    )
    create_button(root, "Exit", 6, 0, command=root.destroy, columnspan=2)

    # Topic entry
    topic_frame = tk.Frame(root)
    topic_frame.grid(row=7, column=0, columnspan=2, pady=10)
    create_label(topic_frame, "Topic:", 0, 0)
    topic_entry = create_entry(topic_frame, 20, 0, 1, padx=5)
    create_button(
        topic_frame,
        "Load",
        0,
        2,
        command=(lambda: load_topic_cb(topic_entry.get()) if load_topic_cb else None)
    )

    # Saved files list
    saved_files = fetch_saved_flashcards()
    listbox = None
    if saved_files:
        create_label(root, "Saved Files:", 8, 0, sticky="w", pady=5)
        listbox = create_listbox(root, 5, 40, 8, 1, pady=5)
        for filename in saved_files:
            listbox.insert(tk.END, filename)
        create_button(
            root,
            "Load File",
            9,
            0,
            command=(lambda: load_file_cb(listbox.get(tk.ACTIVE)) if (load_file_cb and listbox) else None),
            columnspan=2
        )

    # Cards list for the currently loaded topic/file
    create_label(root, "Cards:", 10, 0, sticky="w", pady=5)
    cards_listbox = create_listbox(root, 8, 40, 10, 1, pady=5)

    return {
        "word_var": word_var,
        "def_var": def_var,
        "example_var": example_var,
        "synonyms_var": synonyms_var,
        "antonyms_var": antonyms_var,
        "new_word_button": new_word_button,
        "speak_button": speak_button,
        "topic_entry": topic_entry,
        "listbox": listbox,
        "cards_listbox": cards_listbox,
    }
