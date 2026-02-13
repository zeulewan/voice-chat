import os
from pathlib import Path

import anthropic
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

WHISPER_URL = os.getenv("WHISPER_URL", "http://127.0.0.1:2022")
KOKORO_URL = os.getenv("KOKORO_URL", "http://127.0.0.1:8880")

claude = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a helpful voice assistant running on a Linux workstation. \
Keep responses concise and conversational — they will be spoken aloud. \
Avoid markdown formatting, bullet points, or long lists. \
Respond in 1-3 short sentences unless the user asks for detail."""


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class SpeakRequest(BaseModel):
    text: str
    voice: str = "af_sky"


@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{WHISPER_URL}/v1/audio/transcriptions",
            files={"file": (file.filename or "audio.webm", audio_bytes, file.content_type or "audio/webm")},
            data={"model": "whisper-1", "response_format": "json"},
        )
        resp.raise_for_status()
    return resp.json()


@app.post("/api/chat")
async def chat(req: ChatRequest):
    messages = []
    for msg in req.history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": req.message})

    response = claude.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    text = response.content[0].text
    return {"response": text}


@app.post("/api/speak")
async def speak(req: SpeakRequest):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{KOKORO_URL}/v1/audio/speech",
            json={
                "model": "tts-1",
                "input": req.text,
                "voice": req.voice,
                "response_format": "mp3",
            },
        )
        resp.raise_for_status()
    return Response(content=resp.content, media_type="audio/mpeg")


@app.get("/")
async def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3456)
