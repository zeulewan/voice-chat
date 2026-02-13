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

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- [Tailscale](https://tailscale.com/) (for remote access from other devices)

## Install

```bash
git clone https://github.com/zeulewan/voice-chat.git
cd voice-chat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure

Create a `.env` file with your Anthropic API key:

```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

## Run

```bash
source .venv/bin/activate
python server.py
```

The server starts on `http://127.0.0.1:3456`.

## Remote Access via Tailscale

Expose the server over HTTPS on your tailnet:

```bash
sudo tailscale serve --bg --https=3456 http://127.0.0.1:3456
```

Then open `https://<your-machine>.ts.net:3456` from any device on your tailnet.

## Usage

1. Open the web UI in your browser
2. Hold the mic button and speak
3. Release — your speech is transcribed by Whisper
4. Claude responds and Kokoro speaks the answer
