from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file
        )

    os.unlink(tmp_path)
    return {"transcript": transcript.text}

from pydantic import BaseModel

class TranscriptInput(BaseModel):
    transcript: str

@app.post("/structure")
async def structure(input: TranscriptInput):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a meeting notes assistant. 
                Given a transcript, extract and return ONLY a JSON object with this exact structure:
                {
                    "summary": "2-3 sentence summary",
                    "tasks": ["task 1", "task 2"],
                    "decisions": ["decision 1"],
                    "deadlines": ["deadline 1"]
                }
                Return only the JSON, no extra text."""
            },
            {
                "role": "user",
                "content": input.transcript
            }
        ]
    )
    
    import json
    raw = response.choices[0].message.content
    structured = json.loads(raw)
    return structured
