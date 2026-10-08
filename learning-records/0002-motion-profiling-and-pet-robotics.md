# 0002: Trajectory Generation vs. AI, and the Pet Canine Companion Model

The user questioned the necessity of training an AI policy if classical Inverse Kinematics (IK) can translate target coordinates directly to an MCU. We unpacked how trajectory generators actually function (differentiating between MCU firmware planners and PC streaming) and resolved why pure IK produces cold, sterile industrial motion. The user articulated their true creative vision: turning the 6-DOF arm into a lifelike desktop pet companion (with the gripper acting as a dog head).

## Key Insights
- **S-Curve Execution**: An MCU does not snap to coordinates; motion profilers (whether running on the ESP32 via 7-phase S-curve timers or streamed from the PC at 50Hz) interpolate acceleration smoothly.
- **Why Classical IK Falls Short for Pets**: IK solves point-to-point Euclidean shortest paths. Real creatures exhibit curiosity, gaze tracking, head tilting, playful hesitation, compliant yielding to touch, and organic idle breathing.
- **The Justification for AI**: AI (Gemini vision for cognitive perception + RL/procedural policies for expressive motion style) is what breathes life into the arm.

## Implications
- The system evolves from an industrial pick-and-place gantry to an **Expressive Desktop Pet Companion**.
- The control stack adopts a 3-layer architecture:
  1. High-Level Brain: Gemini 2.0 Flash (Visual scene analysis, intent, pet mood state).
  2. Mid-Level Behavior: Behavior Tree (Alert, Sniff, Tilt Head, Nuzzle, Rest/Nap).
  3. Low-Level Body: Expressive Kinematics & Compliance Engine (S-curve safety geofence + organic motion synthesis).
