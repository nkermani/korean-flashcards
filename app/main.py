# app/main.py
# This is the main entry point for the FastAPI application, setting up routes and starting the server.

from fastapi import FastAPI
from app.routes import flashcards, saved, history
import tkinter as tk
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello from Mistral FastAPI, Korean Flashcards API is running!"}


app.include_router(flashcards.router)
app.include_router(saved.router)
app.include_router(history.router)

# Explain why those settings in uvicorn.run are used here
# - "main:app" specifies the application instance to run.
# - host="0.0.0.0" makes the server accessible from any IP address.
# - port=8000 sets the port number for the server.
# - reload=True enables auto-reloading of the server on code changes, useful for development.


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
