# SPEC-0001: Desktop AI Robot Arm & Desktop Assistant Integration

- **Status**: Ready for Implementation (`ready-for-agent`)
- **Date**: 2026-10-04
- **Related ADRs**:
  - [ADR 0001: Hybrid Stepper-Servo Actuation & Wireless Docking](file:///g:/projects/deskto-AI-arm/docs/adr/0001-hybrid-stepper-servo-and-wireless-docking.md)
  - [ADR 0002: Sensorless Homing, Base-Mounted Belt Drive, and WebSocket Architecture](file:///g:/projects/deskto-AI-arm/docs/adr/0002-sensorless-homing-base-steppers-and-websockets.md)
  - [ADR 0003: 24V Bus, PLA Thermal Mitigation, and Rack-and-Pinion Gripper](file:///g:/projects/deskto-AI-arm/docs/adr/0003-power-delivery-thermal-pla-and-rack-pinion-gripper.md)
  - [ADR 0004: Conversational Disambiguation, ONNX Runtime Inference, and Domain Randomization](file:///g:/projects/deskto-AI-arm/docs/adr/0004-conversational-ambiguity-onnx-and-domain-randomization.md)

---

## Problem Statement

As a beginner to robotics, AI, and electronics, building a desktop manipulator from scratch is daunting due to the complex convergence of mechanical design, kinematics math, PCB layout, and modern neural network control. Furthermore, desktop robots typically lack emotional personality and intuitive natural language interfaces, while existing hobby arms suffer from servo jitter, gear backlash, loud whining, and dangerous lack of collision detection.

The user needs a modular, quiet, precise desktop 6-DOF robot arm that physically integrates with their sibling **Desktop Assistant** (providing expressive eyes and voice interaction), uses cloud compute (Google Colab / MuJoCo) for accelerated AI training, and executes safe, intelligent object manipulation on a desk.

---

## Solution

A desktop-sized 6-DOF hybrid manipulator featuring:
1. **Physical & Electrical Dock**: An arm base cradle with ENIG gold pads mating with Desktop Assistant's `KZM05P03UFT2-B` pogo pins, delivering 5V 3A charging and automatic dock presence detection.
2. **Hybrid Stepper-Servo Drive**: NEMA 14/17 steppers with Trinamic TMC2209 silent drivers and GT2 belt reduction for the high-torque base and shoulder/elbow joints, combined with lightweight micro-servos for the wrist and rack-and-pinion gripper.
3. **Sensorless Homing & Safety**: StallGuard4 back-EMF detection for wire-free homing and automatic emergency cut-off upon collision, backed by software workspace geofencing.
4. **Cloud-Trained Sim-to-Real Policy**: A continuous-control PPO policy trained with domain randomization in Google DeepMind's MuJoCo physics engine on Google Colab, exported to ONNX for lightweight sub-5ms local PC execution.
5. **Conversational Multi-Modal Intelligence**: Overhead webcam scene parsing via Google Gemini 2.0 Flash with conversational disambiguation streamed through Desktop Assistant's microphone and speaker.

---

## User Stories

1. As a user, I want to dock my Desktop Assistant onto the robot arm's base cradle, so that its battery charges automatically via pogo pins.
2. As a user, I want the arm controller to instantly detect when Desktop Assistant is seated, so that it can trigger a greeting animation and report system readiness.
3. As a user, I want Desktop Assistant to continue working wirelessly on internal battery when unseated, so that I can hold it or place it anywhere on my desk while commanding the arm.
4. As a user, I want to speak natural voice commands (e.g., *"Pick up the marker"*) to Desktop Assistant, so that the robot performs object manipulation without requiring keyboard controls.
5. As a user, I want the robot to ask me for clarification through Desktop Assistant's speaker when multiple similar objects are on the table, so that it never grabs the wrong item by mistake.
6. As a user, I want Desktop Assistant's circular LCD to display expressive facial emotions (focused eyes while tracking, happy face on successful grasp, confused face on obstacle), so that the robotic system feels alive and engaging.
7. As a user, I want the arm's base and shoulder joints to operate silently using TMC2209 StealthChop2, so that the arm does not produce irritating high-pitch servo whine on my desk.
8. As a user, I want the arm to home itself automatically on boot without external limit switch wires, so that the mechanical links remain clean and aesthetically pleasing.
9. As a user, I want the arm to immediately stop and cut motor torque if it accidentally bumps into my hand or a desktop object, so that neither the 3D printed parts nor desk items are damaged.
10. As a user, I want to train the motion policy in Google DeepMind MuJoCo on Google Colab using free cloud GPUs, so that I can train complex neural control policies without requiring an expensive local GPU workstation.
11. As a user, I want the trained AI policy exported as an ONNX model, so that my local PC can run real-time inference with minimal CPU usage and zero PyTorch dependencies.
12. As a user, I want the AI policy trained with domain randomization in simulation, so that it transfers seamlessly to the physical 3D-printed arm despite minor belt compliance and friction differences.
13. As a user, I want the structural links printable in standard PLA with active thermal cooling, so that I can fabricate the arm on any basic 3D printer without warping.
14. As a user, I want a symmetrical parallel-jaw rack-and-pinion gripper, so that small cylindrical and rectangular desk items are grasped securely along the tool centerline.
15. As a developer, I want all messaging between PC, Desktop Assistant, and Arm Base to use structured JSON over WebSockets, so that telemetry and commands can be inspected easily in standard tools.

---

## Implementation Decisions

### 1. Electrical & Power Subsystem (Base Controller PCB)
- **Power Input**: 24V 5A DC barrel jack (2.1x5.5mm) with `SMBJ28A` TVS diode and P-channel MOSFET reverse polarity protection.
- **Buck Converter**: `TPS54302` (handles up to 28V input) generating 5.0V @ 3A for Desktop Assistant charging and servo bus, protected by a 2A PPTC resettable fuse.
- **LDO Regulator**: 3.3V low-dropout regulator for base ESP32-S3 MCU and logic.
- **Stepper Drivers**: 3x TMC2209 silent step/dir drivers configured over single-wire UART for software current control and StallGuard sensitivity tuning.
- **Dock Connector**: 5-pad ENIG gold interface matching Desktop Assistant `KZM05P03UFT2-B` pogo pins (`VBUS_5V`, `UART_TX`, `UART_RX`, `DOCK_DETECT_N`, `GND`).

### 2. Mechanical Subsystem (FreeCAD & PLA Fabrication)
- **Base Enclosure**: Encloses the base controller PCB, 24V input jack, 4010 cooling fan, and houses the Base Yaw NEMA 17 motor.
- **Top Deck**: Features a recessed cradle with dual N52 alignment magnets and gold pogo contact pads to hold Desktop Assistant.
- **Belt Drive**: 2GT synchronous timing belts (6mm width) transferring torque from base-mounted steppers to the shoulder and elbow pivot bearings.
- **End-Effector**: Dual rack-and-pinion parallel gripper driven by a single metal-gear micro-servo (MG90S) with silicone contact pads.

### 3. Firmware Subsystem (ESP32-S3 Arm Controller)
- **Framework**: ESP-IDF with FreeRTOS.
- **Stepper Engine**: Hardware timer generating smooth acceleration S-curves (Jerk-limited motion).
- **Homing State Machine**: Boots $\to$ lowers current to 200mA $\to$ moves towards hard stop $\to$ detects `DIAG` pin trigger $\to$ sets coordinate to zero $\to$ backs off 2mm $\to$ restores run current (600mA).
- **Network Interface**: WebSocket client connecting to PC WebSocket server; binary/JSON packet handler.

### 4. Software & AI Subsystem (Host PC & Google Colab)
- **Simulation**: Headless MuJoCo 3.x environment (`software/arm_env_3d.py`) modeling 6 articulated joints, table plane, and 3D reaching target.
- **Cloud Training**: Google Colab notebook (`software/train_arm_3d_6dof.ipynb`) running Stable-Baselines3 PPO with vectorized parallel environments and domain randomization.
- **Model Deployment**: Policy actor exported to `software/models/arm_policy.onnx`, evaluated locally on PC using `onnxruntime`.
- **Vision Pipeline**: Overhead webcam captures desk frame; Google Gemini 2.0 Flash (`software/gemini_vision_planner.py`) outputs target coordinates $[X, Y, Z]$ and handles conversational disambiguation.

---

## Testing Decisions

### Seams & Boundaries
1. **Simulation Seam (`DesktopArm3DEnv`)**: Verify the MuJoCo simulation environment independently via `software/test_sim.py` (reset, step, reward calculation, observation space bounds).
2. **ONNX Inference Seam**: Unit test verifying `onnxruntime` produces valid joint delta actions matching the PyTorch policy output within a numerical tolerance ($\epsilon < 10^{-4}$).
3. **Kinematics Math Seam**: Forward and Inverse Kinematics unit tests comparing analytical matrix calculations against MuJoCo physics forward kinematics.
4. **WebSocket Protocol Seam**: Mock WebSocket server testing message parsing, dock presence events, and emergency stop trigger responses.
5. **Firmware Motor Seam**: Hardware-in-the-loop test commanding 1,000 microsteps and verifying zero step loss.

---

## Out of Scope

- High-voltage industrial servo drives (48V+).
- Heavy metal CNC milling of arm links (all parts optimized for FDM 3D printing).
- SLAM or mobile navigation (the arm base is a desktop stationary unit).
- Training vision models from scratch (leveraging Google Gemini 2.0 Flash foundation model).
