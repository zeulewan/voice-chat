# Starting Voice Chat

*2026-02-13*

There isn't a good way to talk to AI agents right now. You can type to them, but verbal interaction with agents that actually do things — run commands, edit files, browse the web — barely exists. Voice Chat is an attempt to make that work well.

The speech-to-text and text-to-speech run locally on your own hardware. Whisper handles transcription on the GPU, Kokoro handles speech synthesis. No audio leaves your network. The whole thing is designed to run on a workstation with a dedicated graphics card that's always on — plug in a GPU with a few gigs of VRAM and you have a private voice interface to your AI agent.

Right now it's built around Claude Code, but the architecture isn't married to it. The MCP server and WebSocket bridge are generic enough that switching to other AI backends later is realistic.

## What we did today

Set up the docs site and started organizing the project properly. Removed hard-coded timeouts (60s playback, 120s recording) from the MCP server — these were killing conversations mid-flow. Restructured the docs into `guide/` and `roadmap/` folders with navigation tabs. Added hardware requirements, version history from v0.0.1 through v0.4.0, and a planned features list with checkboxes. Investigated the VoiceMode dependency and confirmed it's just an installer for Whisper and Kokoro — standalone install scripts are on the roadmap. Added MIT license, README, copied the slash command and skill file into the repo, and tagged v0.2.0.
