# Configuration

## Environment Variables

All configuration is done via the `.env` file in the project root.

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `WHISPER_URL` | `http://127.0.0.1:2022` | Whisper STT server base URL |
| `KOKORO_URL` | `http://127.0.0.1:8880` | Kokoro TTS server base URL |

Example `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...
WHISPER_URL=http://127.0.0.1:2022
KOKORO_URL=http://127.0.0.1:8880
```

## Voice Services

### Whisper STT

The backend forwards audio to Whisper's OpenAI-compatible endpoint:

```
POST {WHISPER_URL}/v1/audio/transcriptions
```

Whisper accepts WebM, WAV, MP3, and other common audio formats. The browser records in WebM/Opus by default.

### Kokoro TTS

The backend requests speech from Kokoro's OpenAI-compatible endpoint:

```
POST {KOKORO_URL}/v1/audio/speech
```

#### Available Voices

| Voice | Description |
|-------|-------------|
| `af_sky` | Female (default) |
| `af_alloy` | Female |
| `af_sarah` | Female |
| `am_adam` | Male |
| `am_echo` | Male |
| `am_onyx` | Male |
| `bm_fable` | Androgynous |

## Tailscale Setup

### Expose the Server

```bash
sudo tailscale serve --bg --https=3456 http://127.0.0.1:3456
```

This creates an HTTPS endpoint with automatic TLS certificates at:

```
https://<your-machine>.ts.net:3456
```

### Verify

```bash
tailscale serve status
```

### Remove

```bash
sudo tailscale serve --https=3456 off
```

## Claude Model

The backend uses `claude-sonnet-4-5-20250929` with a system prompt optimized for voice:

> Keep responses concise and conversational — they will be spoken aloud.
> Avoid markdown formatting, bullet points, or long lists.
> Respond in 1-3 short sentences unless the user asks for detail.

To change the model, edit `server.py` and update the `model` parameter in the `/api/chat` endpoint.

## Ports Summary

| Port | Service | Protocol |
|------|---------|----------|
| 3456 | Voice Chat backend | HTTP (localhost) / HTTPS (Tailscale) |
| 2022 | Whisper STT | HTTP (localhost only) |
| 8880 | Kokoro TTS | HTTP (localhost only) |
