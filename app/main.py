import os
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from mistralai import Mistral
from dotenv import load_dotenv
from gtts import gTTS
import os, json, re, uuid

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise RuntimeError("Missing MISTRAL_API_KEY in .env file")

client = Mistral(api_key=api_key)

app = FastAPI()

# Folder to store generated audio files
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Hello from Mistral FastAPI, Korean Flashcards API is running!"}


@app.post("/flashcards")
async def create_flashcards(data: dict = Body(...)):
    topic = data.get("topic", "general vocabulary")

    prompt = f"""
    Create 5 flashcards to help a student learn faster about the topic in KOREAN !"{topic}".
    Each flashcard must be a JSON object with:
    - word
    - definition
    - example
    - synonyms (at least 2)
    - antonyms (at least 2)
    Return a JSON array of 5 such flashcards.
    """

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    try:
        flashcards = json.loads(text)
    except:
        json_str = re.search(r'\[.*\]', text, re.S).group(0)
        flashcards = json.loads(json_str)

    # Save audio files for each word
    os.makedirs("tts_audio", exist_ok=True)
    for card in flashcards:
        filename = f"tts_audio/{card['word'].lower()}_{uuid.uuid4().hex[:6]}.mp3"
        tts = gTTS(text=card["word"], lang="ko")
        tts.save(filename)
        card["tts_path"] = filename

    return {"topic": topic, "flashcards": flashcards}


# Route to serve saved audio files
@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "file not found"}


# @app.post("/ask")
# def ask_mistral(question: str = Body(..., embed=True)):
#     response = client.chat.complete(
#         model="mistral-small",
#         messages=[{"role": "user", "content": question}]
#     )
#     return {"answer": response.choices[0].message.content}
