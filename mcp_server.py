"""Voice Chat MCP Server — browser audio bridge for Claude Code.

Dual-transport server:
  - FastMCP stdio ↔ Claude Code (persistent session)
  - Embedded FastAPI + WebSocket on 127.0.0.1:3456

Claude calls converse() → Kokoro TTS → browser plays audio →
browser records → Whisper STT → returns text to Claude.
"""

import asyncio
import base64
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import AsyncIterator

import httpx
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastmcp import FastMCP

WHISPER_URL = "http://127.0.0.1:2022"
KOKORO_URL = "http://127.0.0.1:8880"
WS_PORT = 3456


def log(msg: str) -> None:
    """Log to stderr (stdout is reserved for MCP stdio protocol)."""
    print(msg, file=sys.stderr, flush=True)


# --- Shared state between WebSocket and MCP tools ---


@dataclass
class Bridge:
    """Shared state between the WebSocket handler and MCP tools."""

    ws: WebSocket | None = None
    audio_queue: asyncio.Queue[bytes] = field(default_factory=asyncio.Queue)
    playback_done: asyncio.Event = field(default_factory=asyncio.Event)
    connected: asyncio.Event = field(default_factory=asyncio.Event)


bridge = Bridge()

# --- FastAPI app (WebSocket + static file serving) ---

web_app = FastAPI()


@web_app.get("/")
async def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@web_app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    log("Browser connected")

    # Last connection wins (single user)
    bridge.ws = ws
    bridge.connected.set()

    # Drain any stale audio from previous sessions
    while not bridge.audio_queue.empty():
        try:
            bridge.audio_queue.get_nowait()
        except asyncio.QueueEmpty:
            break

    try:
        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")

            if msg_type == "audio":
                audio_bytes = base64.b64decode(data["data"])
                await bridge.audio_queue.put(audio_bytes)

            elif msg_type == "playback_done":
                bridge.playback_done.set()

    except WebSocketDisconnect:
        log("Browser disconnected")
    except Exception as e:
        log(f"WebSocket error: {e}")
    finally:
        if bridge.ws is ws:
            bridge.ws = None
            bridge.connected.clear()
            bridge.playback_done.set()  # Unblock any waiting converse()


# --- FastMCP server with lifespan ---


async def run_webserver():
    """Run uvicorn as a background async task."""
    config = uvicorn.Config(
        web_app,
        host="127.0.0.1",
        port=WS_PORT,
        log_config=None,
        log_level="error",
    )
    server = uvicorn.Server(config)
    await server.serve()


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Start the WebSocket server alongside the MCP stdio server."""
    task = asyncio.create_task(run_webserver())
    log(f"WebSocket server started on port {WS_PORT}")
    try:
        yield {}
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        log("WebSocket server stopped")


mcp = FastMCP(
    name="voice-chat",
    lifespan=lifespan,
)


@mcp.tool
async def converse(
    message: str,
    wait_for_response: bool = True,
    voice: str = "af_sky",
) -> str:
    """Speak a message to the user via TTS and optionally listen for their spoken response via STT.

    Args:
        message: Text to speak to the user.
        wait_for_response: If True, listen for the user's spoken response after playback.
        voice: Kokoro TTS voice name (default: af_sky).

    Returns:
        The user's transcribed speech, or a status message if not listening.
    """
    if bridge.ws is None:
        return "Error: No browser connected. Open the Voice Chat page first."

    ws = bridge.ws

    try:
        # Send status
        await ws.send_json({"type": "status", "text": "Speaking..."})

        # TTS: text → mp3
        async with httpx.AsyncClient(timeout=30) as client:
            tts_resp = await client.post(
                f"{KOKORO_URL}/v1/audio/speech",
                json={
                    "model": "tts-1",
                    "input": message,
                    "voice": voice,
                    "response_format": "mp3",
                },
            )
            tts_resp.raise_for_status()

        # Send audio to browser
        audio_b64 = base64.b64encode(tts_resp.content).decode()
        bridge.playback_done.clear()
        await ws.send_json({"type": "audio", "data": audio_b64})

        if not wait_for_response:
            await ws.send_json({"type": "done"})
            return "Message delivered."

        # Wait for browser to finish playing audio
        await asyncio.wait_for(bridge.playback_done.wait(), timeout=60)

        if bridge.ws is None:
            return "Error: Browser disconnected during playback."

        # Drain stale audio
        while not bridge.audio_queue.empty():
            try:
                bridge.audio_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        # Tell browser to start recording
        await ws.send_json({"type": "listening"})

        # Wait for recorded audio
        audio_bytes = await asyncio.wait_for(bridge.audio_queue.get(), timeout=120)

        if bridge.ws is None:
            return "Error: Browser disconnected during recording."

        # STT: webm → text
        await ws.send_json({"type": "status", "text": "Transcribing..."})
        async with httpx.AsyncClient(timeout=30) as client:
            stt_resp = await client.post(
                f"{WHISPER_URL}/v1/audio/transcriptions",
                files={
                    "file": ("recording.webm", audio_bytes, "audio/webm"),
                },
                data={"model": "whisper-1", "response_format": "json"},
            )
            stt_resp.raise_for_status()

        text = stt_resp.json().get("text", "").strip()
        if not text:
            return "(no speech detected)"

        await ws.send_json({"type": "done"})
        return text

    except asyncio.TimeoutError:
        return "Error: Timed out waiting for response."
    except WebSocketDisconnect:
        return "Error: Browser disconnected."
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
async def voice_chat_status() -> str:
    """Check if a browser is connected to the Voice Chat WebSocket.

    Returns:
        Connection status string.
    """
    if bridge.ws is not None:
        return "Connected: Browser is connected and ready."
    return "Disconnected: No browser connected. Open https://workstation.tailee9084.ts.net:3456 in your browser."


if __name__ == "__main__":
    mcp.run()
