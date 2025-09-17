# Prompt Playground

An API wrapper around the Mistral SDK using FastAPI.

## Features
- POST /generate — Send a prompt and get back AI response

## Setup

```bash
git clone ...
cd prompt-playground
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
## Example Usage
```bash
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt": "What is AI?"}'
```




