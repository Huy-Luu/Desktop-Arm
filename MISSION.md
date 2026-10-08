# Mission: Desktop AI Robot Arm

## Why
Build an intelligent, desktop-sized 6-DOF robotic arm integrated with the Desktop Assistant project, using this hands-on journey to master robotic AI (MuJoCo, RL, Google Colab/Cloud), CAD (FreeCAD), embedded firmware (ESP32), and circuit design (KiCad) as a beginner.

## Success looks like
- A simulated 6-DOF robotic arm environment in MuJoCo running at high speed on Google Colab.
- An AI policy trained via Reinforcement Learning (PPO) that can reach specified 3D targets `[X, Y, Z]` with organic, natural dynamics.
- An expressive **Pet Canine Companion persona**: the arm acts like an inquisitive desktop pet (with the gripper as its "dog head"), featuring curious head-tilting ($\pm 15^\circ$ roll bias), breathing/idle micro-oscillations, affectionate nudges, and playful sniffing.
- An integrated vision & voice pipeline: user speaks to Desktop Assistant / PC, Gemini 2.0 Flash detects target coordinates and human gestures from an overhead camera, and the robot responds dynamically.
- A physical Base Controller PCB with a pogo pin dock matching Desktop Assistant's `KZM05P03UFT2-B` interface, supplying power and UART communication.
- Solid understanding of robotic fundamentals: forward/inverse kinematics, trajectory generation (S-curves), sim-to-real transfer, expressive animatronics, and power delivery.

## Constraints
- **Beginner in AI**: Explanations must be intuitive, pedagogical, avoiding overwhelming math jargon without context.
- **Google Ecosystem**: Leverage Google Colab (GPU/cloud compute), Google DeepMind MuJoCo physics, and Google AI Studio / Gemini APIs.
- **Modularity**: Must cleanly link with the cousin `desktop_assistant` hardware and firmware.

## Out of scope
- Industrial high-voltage industrial arms or heavy hydraulic systems.
- Commercial mass manufacturing (this is an educational prototype).
