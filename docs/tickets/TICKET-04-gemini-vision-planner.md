# TICKET-04: Gemini 2.0 Flash Vision Planner & Conversational Disambiguation

- **Status**: Ready
- **Blocked By**: TICKET-01
- **Delivers**: Overhead webcam perception script using Google Gemini 2.0 Flash (`software/gemini_vision_planner.py`) extracting $[X, Y, Z]$ coordinates and emitting disambiguation dialogue when multiple objects match a query.

## Acceptance Criteria
1. Sends overhead desk camera frame to `gemini-2.0-flash`.
2. Returns structured JSON containing object bounding boxes, normalized coordinates, and grasp approach angle.
3. Detects ambiguous voice queries (e.g. multiple candidate objects) and returns a formatted question string for Desktop Assistant to speak.
