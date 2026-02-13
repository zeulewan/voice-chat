# Roadmap

## Planned Features

### Installation & Packaging

- **Standalone install scripts** — Remove the VoiceMode dependency by installing [whisper.cpp](https://github.com/ggerganov/whisper.cpp) and [kokoro-fastapi](https://github.com/remsky/kokoro-fastapi) directly from their upstream repos with bundled install scripts and systemd service files.
- **One-command setup** — Single script that installs all dependencies, builds Whisper with CUDA, sets up Kokoro, creates the Python venv, registers the MCP server, and configures Tailscale.
- **Health check endpoint** — `/health` endpoint on the MCP server that verifies Whisper, Kokoro, and WebSocket connectivity in one call.

### Reliability

- **No recording timeout** — Remove the 120-second timeout on voice recording. The server should wait indefinitely for the user to speak and tap stop, rather than timing out and returning an error.
- **Auto-reconnect with state recovery** — When the WebSocket drops and reconnects, preserve the conversation state instead of starting fresh.
- **Service health monitoring** — Detect when Whisper or Kokoro services go down and show a clear error in the browser UI instead of a generic failure.

### Audio & Voice

- **Voice activity detection** — Automatically detect when the user stops speaking and end recording, instead of requiring a manual tap to stop.
- **Streaming TTS** — Stream audio chunks to the browser as Kokoro generates them instead of waiting for the full MP3, reducing time-to-first-audio.
- **Voice selection in UI** — Let users pick from available Kokoro voices (af_sky, af_alloy, am_adam, etc.) directly in the browser interface.
- **Adjustable speech speed** — Control TTS playback speed from the browser UI.

### Browser UI

- **Conversation history** — Persist chat history across page refreshes using localStorage.
- **Keyboard shortcut** — Press-and-hold spacebar to record, release to send (desktop browsers).
- **Mobile improvements** — Optimized touch targets, haptic feedback on recording start/stop, and wake lock to prevent screen sleep during conversations.
- **Dark/light theme** — Match system preference or allow manual toggle.

### Documentation

- **AI-optimized documentation** — Provide a machine-readable version of the docs (e.g. `llms.txt` or structured context file) alongside the human-readable site, so LLMs can install and configure voice-chat autonomously.
- **API reference** — Document all MCP tool signatures, WebSocket message types, and HTTP endpoints.
- **Troubleshooting guide** — Expanded guide covering audio quality issues, latency, Tailscale connectivity, and common failure modes.
