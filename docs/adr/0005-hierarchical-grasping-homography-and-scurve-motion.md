# ADR 0005: Hierarchical RL-Primitive Grasping, Fixed Overhead Homography, and S-Curve Motion Execution

- **Status**: Accepted
- **Date**: 2026-10-06
- **Deciders**: User & Antigravity Pair

## Context & Problem Statement
To bring the Desktop AI Robot Arm from pure 3D reaching in simulation to an end-to-end physical manipulation system, architectural decisions were needed for:
1. **Grasp Strategy**: How the system transitions from spatial reaching to securing physical desk objects.
2. **Perception Setup**: How the table workspace is viewed and calibrated to map camera pixels to physical robot coordinates.
3. **Motion Execution**: How motor control commands flow from the host PC's ONNX inference engine to the ESP32-S3 firmware.
4. **Dock Safety Interlock**: How the arm handles Desktop Assistant unseating during active movement.

## Considered Options
- **Grasping**:
  - *Option A (Chosen)*: Hierarchical Control (RL for 3D Reaching + Deterministic Grasp Primitive).
  - *Option B*: Full End-to-End RL (RL controls both 6 arm joints and finger contact physics simultaneously).
  - *Option C*: Numerical Inverse Kinematics (IK) without RL.
- **Vision Rig**:
  - *Option A (Chosen)*: Fixed Overhead Webcam with 4-Point Homography.
  - *Option B*: Desktop Assistant Head Camera with active 3D eye-to-base extrinsics.
  - *Option C*: Dual Camera (Overhead + Wrist-mounted eye-in-hand).
- **Motion Command Pipeline**:
  - *Option A (Chosen)*: Waypoint Streaming with ESP32 Jerk-Limited S-Curve Interpolation.
  - *Option B*: Direct High-Frequency Delta Streaming (40-50 Hz) directly driving step timers.
  - *Option C*: G-Code Parser on ESP32.
- **Dock Safety**:
  - *Option A (Chosen)*: Safety Pause on Undock with Wireless Voice Control.
  - *Option B*: Uninterrupted Independent Operation.
  - *Option C*: Strict Dock-Only Operation (motors cut power when undocked).

## Decision Outcome
1. **Hierarchical Manipulation Control**:
   - The Colab-trained PPO neural network policy is responsible for spatial reaching to a 3D pre-grasp waypoint located $50\text{ mm}$ directly above the target object with approach yaw orientation.
   - Once within tolerance ($<15\text{ mm}$), the system executes a deterministic motion primitive: straight-line vertical descent along $Z$, closing the rack-and-pinion parallel gripper via micro-servo PWM, and lifting $80\text{ mm}$ above the table.
   - *Rationale*: Sim-to-real transfer of contact-rich finger grasping in pure RL is notoriously unstable due to micro-friction and collision chatter. Decoupling spatial reach (handled by RL) from tactile pinch (handled by deterministic primitives) dramatically increases real-world success rates.
2. **Fixed Overhead Camera with 4-Point Homography**:
   - A single fixed webcam observes the desk from above.
   - A one-time 4-point ArUco / table corner homography matrix maps normalized camera coordinates $(u, v)$ directly into $(X, Y)$ table coordinates in meters.
   - *Rationale*: Avoids complex dynamic coordinate frame tracking when the Desktop Assistant head pans or tilts, providing invariant, rock-solid table coordinates.
3. **Waypoint Streaming with ESP32 Jerk-Limited S-Curves**:
   - The PC sends discrete joint angle waypoints over WebSockets.
   - The ESP32-S3 firmware plans and executes smooth jerk-limited (S-curve) acceleration profiles using hardware timers.
   - *Rationale*: Protects 3D-printed PLA teeth and GT2 belts from sharp accelerations, guarantees zero dropped steps, and avoids reliance on microsecond-level Wi-Fi packet latency.
4. **Safety Pause on Undock with Wireless Voice Control**:
   - If Desktop Assistant is lifted from the pogo dock during active arm motion, the arm decelerates to a safe stationary hold.
   - Once paused, Desktop Assistant continues to act as an untethered wireless microphone and emotional display over Wi-Fi, allowing the user to inspect the workspace and command resume or abort.

## Consequences & Trade-offs
### Positive
- High reliability for physical pick-and-place tasks; avoids brittle sim-to-real contact physics.
- Extremely stable vision mapping independent of head movement.
- Smooth, vibration-free motor motion protecting 3D printed mechanical components.
- Intuitive and safe user experience when interacting physically with Desktop Assistant.

### Negative / Challenges to Manage
- Gripper descent requires accurate table plane calibration so fingers do not collide with the table surface.
- S-curve trajectory generator on ESP32 requires dedicated timer math in FreeRTOS.
