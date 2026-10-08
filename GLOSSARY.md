# Domain Glossary

Ubiquitous language for the Desktop AI Robot Arm project and its integration with Desktop Assistant.

## Core Robotic & AI Concepts

### 6-DOF Manipulator
A robotic arm with 6 Degrees of Freedom (Degrees of Freedom): Base Yaw, Shoulder Pitch, Elbow Pitch, Forearm Roll, Wrist Pitch, and Tool Roll/Gripper. 6-DOF allows the end-effector to reach any arbitrary position $(X, Y, Z)$ and orientation (Roll, Pitch, Yaw) within its physical workspace envelope.

### End-Effector (EE)
The tool or gripper at the end of the robotic kinematic chain that interacts with the physical world (e.g. grasping objects).

### Forward Kinematics (FK)
Calculating the 3D position and orientation of the end-effector $(X, Y, Z)$ given a known set of joint angles $(\theta_1, \theta_2, \dots, \theta_6)$. FK is deterministic and calculated using trigonometry and transformation matrices.

### Inverse Kinematics (IK)
The reverse problem: calculating what joint angles $(\theta_1, \dots, \theta_6)$ are required to position the end-effector at a desired 3D point $(X, Y, Z)$. IK often has multiple mathematical solutions or singularities.

### Reinforcement Learning (RL)
A machine learning paradigm where an agent learns through trial-and-error interaction with an environment, maximizing a numerical reward signal.

### Proximal Policy Optimization (PPO)
An actor-critic, on-policy reinforcement learning algorithm known for training stability and strong performance in continuous robotic control tasks.

### Sim-to-Real (Sim2Real)
The process of transferring an AI policy trained in a physics simulator (MuJoCo) onto physical hardware. Bridging the "reality gap" requires accurate motor models, latency simulation, and domain randomization.

### MJCF (MuJoCo XML Format)
The XML file format used by Google DeepMind's MuJoCo physics engine to define bodies, joints, geoms, materials, actuators, and sensors.

### Homography Coordinate Mapping
A 3x3 geometric perspective transformation matrix that maps 2D camera pixel coordinates $(u, v)$ from an overhead webcam viewing a flat table directly into real-world physical coordinates $(X, Y)$ (in meters) in MuJoCo and on the physical desk. It mathematically compensates for camera angle, tilt, and lens perspective distortion.

### Synthetic Test Harness
A standalone testing environment and script that feeds mock or simulated data (such as prerecorded camera frames, synthetic desk images, or simulated sensor readings) into a software module to verify its logic, parsing, and boundary handling deterministically without requiring physical hardware or live external sensors.

---

## Hardware & Actuation Terms

### Hybrid Stepper-Servo System
An actuation architecture combining NEMA 14/17 stepper motors for high-torque base/shoulder joints with lightweight metal-gear micro-servos for the wrist and end-effector.

### TMC2209 Stepper Driver
An ultra-quiet stepper driver IC featuring Trinamic StealthChop2 (silent stepping), SpreadCycle (high dynamic torque), and StallGuard4.

### StallGuard4 / Sensorless Homing
A technology that measures motor back-EMF to detect when a motor hits a physical mechanical endstop, allowing the arm to home itself without needing physical optical or microswitch limit switches.

### GT2 Timing Belt Reduction
A synchronous toothed belt system (2mm tooth pitch) used between stepper motor shafts and joint pivots to multiply torque, eliminate gear backlash, and allow motors to be mounted close to the base center of mass.

### Pogo Pin Dock
The spring-loaded pin interface (`KZM05P03UFT2-B`) used to dock the Desktop Assistant head onto the Arm Base Controller. It delivers 5V DC power, ground, and UART serial communication.

### ESP-NOW
A fast, low-latency, connectionless Wi-Fi protocol developed by Espressif allowing direct peer-to-peer packet transmission between the Desktop Assistant and Arm Base without going through a Wi-Fi router.

### 24V Power Bus
The high-voltage DC distribution rail supplying motor current to TMC2209 stepper drivers, providing superior torque-speed curves and lower current draw compared to 12V rails.

### Parallel-Jaw Rack & Pinion
A gripper mechanism where a central rotating spur pinion simultaneously drives two opposing toothed gear racks in opposite directions, keeping fingers parallel and centered on the grasping axis.

### Standby Hold Current
A TMC2209 firmware feature that automatically reduces motor coil current (e.g. down to 30% of run current) whenever an axis is stationary, preventing PLA motor mounts from softening due to motor heat.

### Conversational Disambiguation
An interaction pattern where the vision-language model detects ambiguity in the user's voice command and prompts Desktop Assistant to ask clarifying questions before initiating motor movements.

### ONNX (Open Neural Network Exchange)
An open, standardized model format enabling trained neural networks (such as our PPO actor policy) to be exported from Google Colab (PyTorch) and executed on the host PC with `onnxruntime` at sub-5ms latency without heavy AI dependencies.

### Domain Randomization (DR)
A sim-to-real transfer technique in which physics parameters (friction, mass, sensor noise, actuator latency) are randomly perturbed across training episodes in MuJoCo, teaching the neural network policy to be invariant to real-world hardware discrepancies.

### Hierarchical Control
An architecture that partitions a complex manipulation task into two distinct layers: a neural network (RL) policy responsible for free-space 3D reaching to a pre-grasp pose, and a deterministic motion primitive responsible for vertical descent, pinch, and lifting.

### Pre-Grasp Waypoint
A spatial target pose positioned at a designated safety clearance (e.g., 50mm) directly above the target object's centroid, oriented with the correct tool yaw angle for grasping.

### Deterministic Grasp Primitive
A scripted, open-loop or sensor-guided sequence executed after reaching the pre-grasp waypoint that performs linear descent along the Z-axis, closes the parallel gripper to a calibrated pinch width, and lifts the payload vertically.

### Jerk-Limited S-Curve Profile
A 7-phase motion acceleration profile where acceleration ramps smoothly up and down rather than stepping instantaneously (infinite jerk), minimizing mechanical vibration, belt backlash, and motor resonance.

### Table Homography Matrix
A 3x3 projective transformation matrix $H$ calibrated against 4 known table reference points that maps 2D camera pixels $(u, v)$ from an overhead webcam directly into real-world $(X, Y)$ table coordinates in meters.

### Safety Pause on Undock
A firmware-level interlock where removing Desktop Assistant from its pogo charging cradle causes the arm to decelerate safely to a halt, while retaining untethered Wi-Fi voice and display interaction.

---

## Pet Companion & Expressive Motion Concepts

### Expressive Robotics
A robotic design paradigm (pioneered by Disney Research, Sony AIBO, and Anki Vector) where robot motion conveys intent, emotion, personality, and life, rather than merely optimizing for shortest-time or industrial straight-line efficiency.

### Inquisitive Head-Tilt (Canine Roll Bias)
An expressive kinematic primitive where the end-effector (the "dog head") tilts sideways along its roll axis ($\pm 12^\circ$ to $\pm 18^\circ$) while maintaining visual gaze on a target object, signaling curiosity, questioning, or heightened attention.

### Idling / Breathing Oscillation
Subtle, continuous low-frequency (0.2 Hz – 0.5 Hz) harmonic or Perlin-noise oscillations injected into joint setpoints during idle states, giving the mechanical arm the illusion of breathing and resting life, preventing it from appearing "powered off" or dead.

### Compliant Interaction (Soft Joint Yield)
Motor control behavior where joint stiffness is intentionally limited (via current limiting or impedance control) so that when a human touches, strokes, or pushes the robot's head/neck, it gently yields and responds to touch rather than rigidly fighting the user.

### Behavior Tree (BT)
A modular hierarchical execution model used in robotics and game AI that evaluates environmental conditions (from Gemini vision and audio) to transition cleanly between distinct pet states (e.g. `SLEEPING`, `ALERT_TRACKING`, `CURIOUS_SNIFFING`, `PLAYFUL_NUDGE`, `GRASP_FETCH`).

### Trajectory Generator (Motion Planner)
A mathematical algorithm—hosted either on the host PC (streaming at 50Hz) or in ESP32 firmware—that translates a static target point into a continuous time-series of positions, velocities, and accelerations adhering to velocity limits and S-curve jerk constraints.
