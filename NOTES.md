# Notes & Working Decisions

## User Profile & Preferences
- **Background**: Beginner in AI, coding, mechanics, CAD, and electronics.
- **Instruction Style**: Instructor / mentor tone. Pedagogical, step-by-step, explaining concepts without premature abstraction.
- **Preferred Tech Stack**:
  - Cloud / Compute: Google Colab (GPU-accelerated headless training).
  - Vision / Multi-modal: Google AI Studio / Gemini 2.0 Flash API for spatial scene understanding.
  - Simulation: Google DeepMind MuJoCo physics engine.
  - CAD: FreeCAD.
  - PCB / Schematics: KiCad.
  - Microcontroller: ESP32 family (sharing architecture with Desktop Assistant).

## Architectural Decisions
1. **Actuation Strategy**:
   - Hybrid Stepper-Servo system: NEMA 14/17 steppers with silent TMC2209 drivers for base yaw, shoulder pitch, and elbow pitch (high torque, no gear backlash, silent holding).
   - Metal-gear micro-servos for forearm roll, wrist pitch, and gripper (lightweight end-effector).
2. **Desktop Assistant Sibling Link**:
   - The Desktop Assistant (`g:\projects\desktop_assistant`) sits on top of the arm's base controller as the expressive robot head/face/ears.
   - Pogo pins (`KZM05P03UFT2-B`) provide power (+5V/GND) and UART serial interface.
   - Full wireless capability: Desktop Assistant can operate standalone on internal battery when unseated, communicating over Wi-Fi / ESP-NOW.
3. **Workspace Vision**:
   - Fixed overhead webcam viewing the table workspace. Gemini 2.0 Flash extracts target object bounding boxes and normalized coordinates, mapped via homography into MuJoCo world space.
4. **Pet Persona & Expressive Motion**:
   - The arm is treated as a living desktop companion / pet (gripper acting as a mechanical dog head).
   - Motion is not sterile industrial CNC movement: requires gaze tracking, inquisitive head-tilt ($\pm 15^\circ$ roll), breathing/idling oscillations, affectionate nudges, and behavioral states (curiosity, play, rest).
   - Motion architecture combines analytical IK boundaries with AI/procedural expressive motion synthesis.
