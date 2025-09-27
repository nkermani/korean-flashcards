format reminder

uvicorn <folder>.<filename_without_.py>:<FastAPI_instance> --reload

Fixed the pyenv issue which was in 3.9.6 version which was not suited for tkinter. Had to fix the pyenv using this line
```
python3.11 -m venv NAME_OF_ENV
```



Summary — how things interact

app/ (FastAPI)
main.py runs the backend API.
routes/ expose endpoints (flashcards, saved, history).
services/ contain business logic (flashcard_service, history_service, etc.).
flashcard_utils.py, tts.py, mistral_client.py used by services to fetch/generate content.
gui/
main.py launches the desktop GUI.
client.py talks to the FastAPI backend (or local files) to load flashcards.
gui/ui/ contains the Tkinter UI (app.py builds windows, layout.py arranges widgets, widgets.py has small helpers).
flashcards.json is local dataset the GUI may use if the API is not used.
gui/audio/ and gui/utils/ provide playback and helpers.
Runtime flow
GUI starts -> loads flashcards (from API or flashcards.json) -> user selects a topic -> GUI stores current_topic and card_index -> UI displays current card via labels.
"New word" should increment card_index for the selected topic, wrap around, and update the displayed labels (and optionally play audio / record history via API). If the button is inert, either the handler is not wired or the handler doesn't change the stored index/update the UI.
Concrete, safe change

Add two small helpers to widgets.py so the code is decoupled and you can wire the button without touching complex UI class logic.
Then either:
Use create_new_word_button(...) from that file and pass get_state/set_state/update_display callbacks; or
Implement a simple on_new_word method inside the UI class that calls advance_topic_index(...) and updates labels.
