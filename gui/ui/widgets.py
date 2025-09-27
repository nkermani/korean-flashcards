import tkinter as tk
from tkinter import font

def create_label(parent, text=None, row=0, column=0, sticky=None, pady=0, padx=0, font=None, textvariable=None, wraplength=None, **kwargs):
    """Create and grid a Label. Accepts either text or textvariable and common tk.Label options."""
    opts = {}
    if text is not None:
        opts["text"] = text
    if textvariable is not None:
        opts["textvariable"] = textvariable
    if font is not None:
        opts["font"] = font
    if wraplength is not None:
        opts["wraplength"] = wraplength
    # merge any additional Label options (fg, bg, anchor, etc.)
    opts.update(kwargs)

    lbl = tk.Label(parent, **opts)
    grid_opts = {"row": row, "column": column}
    if sticky:
        grid_opts["sticky"] = sticky
    if pady:
        grid_opts["pady"] = pady
    if padx:
        grid_opts["padx"] = padx
    lbl.grid(**grid_opts)
    return lbl

def create_button(root, text, row, column, command=None, state=tk.NORMAL, pady=0, columnspan=1):
    """Create a button widget."""
    button = tk.Button(root, text=text, command=command, state=state)
    button.grid(row=row, column=column, pady=pady, columnspan=columnspan)
    return button

def create_entry(root, width, row, column, padx=0):
    """Create an entry widget."""
    entry = tk.Entry(root, width=width)
    entry.grid(row=row, column=column, padx=padx)
    return entry

def create_listbox(root, height, width, row, column, pady=0):
    """Create a listbox widget."""
    listbox = tk.Listbox(root, height=height, width=width)
    listbox.grid(row=row, column=column, pady=pady)
    return listbox

def create_listbox(root, height, width, row, column, pady=0):
    """Create a listbox widget."""
    listbox = tk.Listbox(root, height=height, width=width)
    listbox.grid(row=row, column=column, pady=pady)
    return listbox

# Added helpers for "New word" behavior
def advance_topic_index(flashcards, current_topic, current_index=None):
    """
    Return (next_card, new_index) for the given topic, wrapping around.
    flashcards: list[dict] where each dict may contain 'topic' key.
    current_topic: str
    current_index: int or None
    If no cards for topic, returns (None, 0).
    """
    all_cards = flashcards or []
    # If cards include 'topic' keys, filter by current_topic.
    # If no card has a 'topic' key, treat the entire list as a single topic.
    if any("topic" in c for c in all_cards):
        cards = [c for c in all_cards if c.get("topic") == current_topic]
    else:
        cards = all_cards
    if not cards:
        return None, 0
    idx = 0 if current_index is None else current_index
    idx = (idx + 1) % len(cards)
    return cards[idx], idx

def create_new_word_button(root, text, row, column, get_state, set_state, update_display, pady=0, columnspan=1):
    """
    Create a "New word" button wired to advance topic flashcards.
    - get_state() -> (flashcards, current_topic, current_index)
    - set_state(new_index) -> store the updated index
    - update_display(card) -> update UI to show given card
    This keeps widgets.py decoupled from application state.
    """
    def _on_click():
        flashcards, current_topic, current_index = get_state()
        card, new_index = advance_topic_index(flashcards, current_topic, current_index)
        if card is None:
            return
        set_state(new_index)
        try:
            update_display(card)
        except Exception:
            # best-effort: ignore update errors so button doesn't crash app
            pass

    btn = tk.Button(root, text=text, command=_on_click)
    btn.grid(row=row, column=column, pady=pady, columnspan=columnspan)
    return btn

