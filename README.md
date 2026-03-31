# 🎙️ VoiceNotes Organizer

Turn any audio recording into structured notes instantly using AI.

## What it does
- Upload or record audio
- Auto-transcribes using Whisper (via Groq)
- Extracts: Summary, Tasks, Deadlines, Decisions using LLaMA AI

## Tech Stack
- Frontend: React
- Backend: Python FastAPI
- Transcription: Groq Whisper Large V3
- AI Structuring: LLaMA 3.3 70B via Groq
- Deployment: Coming soon

## Setup

### Backend
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm start

## Status
🚧 In active development
