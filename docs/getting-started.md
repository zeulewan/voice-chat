# Getting Started

## Prerequisites

!!! info "Required services"

    Voice Chat relies on two local services that must be running:

    - **Whisper STT** — GPU-accelerated speech-to-text (port 2022)
    - **Kokoro TTS** — GPU-accelerated text-to-speech (port 8880)

    These are managed by [VoiceMode](https://github.com/mbailey/voicemode):

    ```bash
    uvx voice-mode-install --yes
    voicemode whisper install
    voicemode kokoro install
    ```

You also need:

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI)
- Python 3.10+
- [Tailscale](https://tailscale.com/) (for remote access from other devices)

## Install

```bash
git clone https://github.com/zeulewan/voice-chat.git
cd voice-chat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Register MCP Server

```bash
claude mcp add -s user voice-chat -- /path/to/voice-chat/.venv/bin/python /path/to/voice-chat/mcp_server.py
```

Replace `/path/to/voice-chat` with the actual path to the cloned repo. Verify with:

```bash
claude mcp list
```

## Remote Access via Tailscale

Expose the server over HTTPS on your tailnet:

```bash
sudo tailscale serve --bg --https=3456 http://127.0.0.1:3456
```

Then open `https://<your-machine>.ts.net:3456` from any device on your tailnet.

## Usage

1. Start Claude Code — the MCP server launches automatically
2. Open the web UI in your browser (green dot = connected)
3. Run `/voice-chat` in Claude Code
4. Claude greets you — speak your request when prompted
5. Claude processes your request using its full tool set, then speaks the response
6. Continue the conversation until you say goodbye

## Troubleshooting

**MCP tools not found:** Wait 10 seconds after starting Claude Code for the MCP server to initialize, then try again.

**502 Bad Gateway in browser:** The WebSocket server hasn't started yet. Check `tail -f /tmp/voice-chat.log` for status.

**Port 3456 in use:** The server retries every 5 seconds. Kill any stale processes: `lsof -i:3456` then `kill <pid>`.
