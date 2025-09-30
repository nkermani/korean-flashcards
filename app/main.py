from fastapi import FastAPI
from routes import flashcards, saved, history
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from Mistral FastAPI, Korean Flashcards API is running!"}

app.include_router(flashcards.router)
app.include_router(saved.router)
app.include_router(history.router)

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()

