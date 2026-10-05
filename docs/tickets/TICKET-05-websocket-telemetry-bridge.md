# TICKET-05: WebSocket Orchestrator & Desktop Assistant Telemetry Bridge

- **Status**: Blocked
- **Blocked By**: TICKET-03, TICKET-04
- **Delivers**: Central WebSocket server on host PC connecting Desktop Assistant (audio streaming / screen expressions), Gemini vision planner, and the arm motion streamer into an end-to-end voice-to-motion loop.

## Acceptance Criteria
1. Asynchronous WebSocket server running on local LAN port (e.g. `8765`).
2. Manages client connections: Desktop Assistant (head), Arm Base Controller, and Vision Planner.
3. Routes speech text $\to$ Gemini $\to$ ONNX Policy $\to$ Arm Base joint packets at 50Hz.
4. Broadcasts arm telemetry events (`"grasp_success"`, `"collision_detected"`, `"disambiguate"`) to Desktop Assistant's LCD.
