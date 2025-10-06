# Korean Flashcards App

## Quick start

- Prepare environment:
  - macOS / Linux:
    - `source setup.sh`
  - Run the app:
    - `./start.sh`

## What this app does

This app generates and reviews Korean flashcards by topic. Each flashcard contains:
- `Word`
- `Definition`
- `Example sentence`
- `Audio pronunciation`
- `Synonyms & Antonyms`

---

Export to .csv file for Anki import

## Usage examples

- Load flashcards for a topic (UI): open the app and click **Load**.
- Run tests locally:
  - `python -m pip install -r requirements.txt`
  - `python -m pytest tests/`

---

## Project structure

### Project tree
```
├── anki_exports
│   └── flashcards.csv
├── .github
│   └── workflows
│       └── tests.yml
├── app
│   ├── config.py
│   ├── flashcard_utils.py
│   ├── history.py
│   ├── main.py
│   ├── mistral_client.py
│   ├── tts.py
│   ├── routes
│   |   ├── flashcards.py
│   |   ├── history.py
│   |   └── saved.py
│   └── services
│       ├── flashcards_service.py
│       ├── history_service.py
│       └── saved_service.py
├── gui
│   ├── main.py
│   ├── api
│   |   └── client.py
│   ├── audio
│   |   └── player.py
│   └── ui
│       ├── app.py
│       ├── layout.py
│       └── widgets.py
├── logs
├── saved_flashcards
│   ├── greetings_20231001120000.json
│   └── history.json
├── requirements.txt
├── setup.sh
├── start.sh
├── tests
│   ├── test_api
│   └── test_gui
└── tts_audio
    ├── 안녕하세요_7062.mp3
    └── 안녕하세요_7062.wav
```
### Overview

Root overview (top-level files and important folders):

- anki_exports/ — generated CSVs for Anki exports (flashcards.csv).
- .github/workflows/ — GitHub Actions workflows (CI, tests.yml).
- logs/ — runtime logs (fastapi.log, gui.log).
- requirements.txt — pinned Python deps for development and CI.
- setup.sh, start.sh — convenience scripts to bootstrap and run the app.

Core application code:

- app/
  - Description: main backend and API code used by the service and CLI.
  - .env — environment example / local secrets (do not commit secrets).
  - config.py — configuration loader.
  - main.py — FastAPI app entrypoint.
  - mistral_client.py — client wrapper for model / external API.
  - flashcard_utils.py — helpers to create/transform flashcards.
  - history.py — history persistence and helpers.
  - tts.py — text-to-speech integration.
  - routes/
    - flashcards.py — API endpoints to list/create/export flashcards.
    - history.py — endpoints for history retrieval.
    - saved.py — endpoints for saved flashcard sets.
  - services/
    - flashcard_service.py — business logic for flashcard generation & retrieval.
    - history_service.py — history management.
    - saved_service.py — saved/restore operations.

GUI / client:

- gui/
  - Description: desktop GUI using Tkinter; can be run standalone.
  - main.py — GUI entrypoint.
  - flashcards.json — shipped sample flashcards.
  - api/ — lightweight client to call backend from the GUI.
  - ui/
    - app.py — high-level UI application glue.
    - layout.py — window / layout definitions.
    - widgets.py — custom widgets and controls.
  - audio/
    - player.py — local audio playback helpers.
  - utils/
    - helpers.py — GUI utils and small helpers.

Tests:

- tests/
  - Description: pytest suite used in CI.
  - conftest.py — fixtures and shared setup.
  - test_api/ — tests for app routes and services (anki export, flashcard logic).
  - test_gui/ — GUI tests (tkinter). CI runs these headless with Xvfb or mocks.

Data and outputs:

- saved_flashcards/ — saved user flashcard sets (JSON).
- tts_audio/ — pre-generated audio assets (mp3 / wav).
- anki_exports/ — CSV exports for Anki import.

Dev artifacts / caches:

- .pytest_cache/ — pytest cache (ignored in VCS).
- .gitignore — patterns to ignore local files.

Notes
- Move large or environment-specific files (flashcard_env/, tts_audio/) out of repo if not needed in CI.
- Prefer mocking GUI in unit tests; use Xvfb in CI only when exercising UI rendering.
- Keep README and requirements in sync with .github/workflows/tests.yml.

---

## Notes & future improvements

### Notes
- CI currently runs GUI tests headless using `xvfb-run` to avoid display errors.

### Future improvements
- Consider adding richer flashcard fields:
  - Hanja origin, frequency, multiple meanings, extra examples.

---
