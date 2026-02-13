# Planned Features

### Zero-Touch Experience

- [ ] **One-command setup** — Single script that installs all dependencies, builds Whisper with CUDA, sets up Kokoro, creates the Python venv, registers the MCP server, and configures Tailscale.

### Installation & Packaging

- [ ] **Standalone install scripts** — Remove the VoiceMode dependency by installing [whisper.cpp](https://github.com/ggerganov/whisper.cpp) and [kokoro-fastapi](https://github.com/remsky/kokoro-fastapi) directly from their upstream repos with bundled install scripts and systemd service files.
- [ ] **Health check endpoint** — `/health` endpoint on the MCP server that verifies Whisper, Kokoro, and WebSocket connectivity in one call.

### Reliability

- [ ] **Interrupt support** — Tap the mic button during audio playback to stop it immediately, skip ahead to the recording phase, and start speaking. The browser stops playback and sends `playback_done` to unblock the server.
- [ ] **Mid-task interjection** — Allow the user to speak while Claude is working (not just during playback). The browser queues the new audio and the server appends it to the context before Claude responds, so you can refine or redirect a task in progress.
- [ ] **Auto-reconnect with state recovery** — When the WebSocket drops and reconnects, preserve the conversation state instead of starting fresh.
- [ ] **Service health monitoring** — Detect when Whisper or Kokoro services go down and show a clear error in the browser UI instead of a generic failure.

### Audio & Voice

- [ ] **Voice activity detection** — Automatically detect when the user stops speaking and end recording, instead of requiring a manual tap to stop.
- [ ] **Streaming TTS** — Stream audio chunks to the browser as Kokoro generates them instead of waiting for the full MP3, reducing time-to-first-audio.
- [ ] **Voice selection in UI** — Let users pick from available Kokoro voices directly in the browser interface with a dropdown or buttons.
- [ ] **Adjustable speech speed** — Control TTS playback speed from the browser UI.
- [ ] **Whisper model selection** — Choose between Whisper model sizes (tiny, base, small, medium, large) from the UI for quality vs. speed tradeoff.

### Browser UI

- [ ] **Chat transcript** — Display the full text of both user and assistant messages in a scrollable chat view, so you can read back what was said.
- [ ] **Audio feedback cues** — Play short sounds for state transitions: a chime when Claude starts thinking, a tone when ready to listen, and a notification sound when a response is buffered.
- [ ] **Settings panel** — In-browser controls for voice, speed, Whisper model, and other configuration without editing files.
- [ ] **Conversation history** — Persist chat history across page refreshes using localStorage.
- [ ] **Keyboard shortcut** — Press-and-hold spacebar to record, release to send (desktop browsers).
- [ ] **Mobile improvements** — Optimized touch targets, haptic feedback on recording start/stop, and wake lock to prevent screen sleep during conversations.
- [ ] **Dark/light theme** — Match system preference or allow manual toggle.

### Multi-Agent

- [ ] **Shared hub** — A persistent WebSocket hub process that all MCP server instances register with. The browser connects to the hub and sees each agent as a tab. When an agent calls `converse()`, the hub buffers the TTS audio and shows a notification badge. Audio only plays when the user selects that tab. The `converse()` call blocks until the user listens and responds.

### Documentation

- [ ] **AI-optimized documentation** — Provide a machine-readable version of the docs (e.g. `llms.txt` or structured context file) alongside the human-readable site, so LLMs can install and configure voice-chat autonomously.
- [ ] **API reference** — Document all MCP tool signatures, WebSocket message types, and HTTP endpoints.
- [ ] **Troubleshooting guide** — Expanded guide covering audio quality issues, latency, Tailscale connectivity, and common failure modes.
