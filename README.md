# Voice Chat

Self-hosted voice chat interface for Claude — local Whisper STT and Kokoro TTS over Tailscale.

## Quick Start

```bash
git clone https://github.com/zeulewan/voice-chat.git
cd voice-chat
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
claude mcp add -s user voice-chat -- $(pwd)/.venv/bin/python $(pwd)/mcp_server.py
```

Requires [Whisper STT](https://github.com/ggerganov/whisper.cpp) and [Kokoro TTS](https://github.com/remsky/kokoro-fastapi) running locally. See the [docs](https://zeulewan.github.io/voice-chat/) for full setup instructions.

## License

[MIT](LICENSE)
