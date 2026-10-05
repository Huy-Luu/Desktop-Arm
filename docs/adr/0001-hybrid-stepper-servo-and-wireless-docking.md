# ADR 0001: Hybrid Stepper-Servo Actuation & Wireless Docking Architecture

- **Status**: Accepted
- **Date**: 2026-10-04
- **Deciders**: User & AI Pair

## Context & Problem Statement
The desktop robot arm requires high precision, sufficient torque for vertical shoulder/elbow cantilever loads, low acoustic noise for a desktop environment, and seamless integration with the mobile Desktop Assistant.

## Decision Drivers
1. **Desktop Acoustic Noise & Precision**: Standard RC servos jitter and whine under load; steppers with silent drivers offer quiet, rock-solid holding torque.
2. **Payload & Cantilever Inertia**: Steppers at the wrist would make the arm excessively top-heavy, whereas micro-servos at the wrist keep the end-effector lightweight.
3. **Untethered Assistant Mobility**: The user wants Desktop Assistant to operate wirelessly on battery when picked up from the arm.

## Considered Options
- **Option 1**: Pure Smart Serial Bus Servos (Feetech/Dynamixel) across all 6 joints.
- **Option 2**: Hybrid: NEMA 14/17 Steppers (with TMC2209 silent drivers & GT2 belts) for Base/Shoulder/Elbow + Micro-Servos for Forearm/Wrist/Gripper. (Chosen)
- **Option 3**: Pure standard RC PWM servos (MG996R / MG90S).

## Decision Outcome
**Chosen Option**: **Option 2 (Hybrid Stepper + Micro-Servo)**:
1. **Base Yaw, Shoulder Pitch, Elbow Pitch**: Driven by NEMA 14 / 17 stepper motors through GT2 timing belt reduction. Silent operation and sensorless homing provided by Trinamic TMC2209 drivers.
2. **Forearm Roll, Wrist Pitch, Gripper**: Driven by lightweight metal-gear micro-servos (e.g. MG90S or SCS0009) to minimize end-effector mass.
3. **Power Architecture**: 12V 5A main supply provides direct motor power to TMC2209 drivers and steps down via Buck converter to 5V 3A for servo rails and Desktop Assistant pogo dock charging.
4. **Docking & Wireless Strategy**:
   - Pogo pins provide battery charging (5V) and dock presence detection.
   - Audio and control messaging utilize local Wi-Fi / WebSockets / ESP-NOW, enabling seamless operation both when docked and when handheld.

## Consequences & Trade-offs
### Positive
- Exceptional positional rigidity and zero jitter when holding stationary positions.
- Silent desktop operation via TMC2209 StealthChop2.
- Low end-effector inertia allows rapid wrist orientation.
- Desktop Assistant can be picked up off the dock without interrupting active voice commands.

### Negative / Challenges to Manage
- **Homing Requirement**: Steppers do not possess absolute encoders on power-up; a homing routine (StallGuard sensorless or optical endstops) is required on boot.
- **Circuit Complexity**: Base PCB must route high-current stepper traces, heat dissipation for TMC2209 drivers, and multiple power domains (12V, 5V, 3.3V).
