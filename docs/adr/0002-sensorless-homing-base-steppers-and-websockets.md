# ADR 0002: Sensorless Homing, Base-Mounted Belt Drive, and WebSocket Architecture

- **Status**: Accepted
- **Date**: 2026-10-04
- **Deciders**: User & AI Pair

## Context & Problem Statement
With the decision to use a hybrid stepper-servo architecture (ADR 0001), critical secondary architectural challenges arose:
1. Stepper motors require homing on startup.
2. NEMA 14/17 stepper motors have significant mass (~200g-300g each); mounting them on upper moving links would create massive cantilever torque and joint deflection.
3. Desktop Assistant must communicate when undocked.
4. Fast desktop manipulators risk knocking over desktop items or damaging 3D printed teeth if jammed.

## Decision Drivers
- Minimal exposed cabling for an elegant desktop aesthetic.
- Low moving mass and inertia to allow snappy, responsive movements.
- Unified local networking protocol accessible from PC, Assistant, and Base MCU.
- Proactive collision prevention and hardware protection.

## Decision Outcome
1. **Homing Mechanism — StallGuard4 Sensorless Homing**:
   - Zero physical limit switches or external wires along the arm links.
   - The arm performs a gentle homing sweep at reduced motor current (e.g., 200mA); when it contacts built-in mechanical hard stops, back-EMF spikes. The TMC2209 driver signals the MCU on the `DIAG` pin to zero the axis coordinate.
2. **Mechanical Layout — Base-Mounted Belt Drive**:
   - Both the Base Yaw motor and Shoulder/Elbow pitch motors remain concentrated inside or immediately adjacent to the stationary base enclosure.
   - 2GT timing belts (closed-loop or open belts with tensioners) route torque up to the shoulder and elbow pivot pulleys.
3. **Communication Protocol — Local Wi-Fi with WebSockets**:
   - The host PC acts as the WebSocket server / broker.
   - Both the Desktop Assistant and Arm Base MCU connect to the local home Wi-Fi network and maintain full-duplex JSON WebSocket streams with the PC.
   - When docked, the pogo pins can optionally negotiate a direct UART mirror, but the unified protocol remains JSON-over-WebSocket.
4. **Collision & Safety System — Dual Layer (Hardware Load + Software Geofencing)**:
   - **Layer 1 (Software Geofence)**: All MuJoCo and IK trajectory generators enforce strict virtual $(X, Y, Z)$ spatial boundaries, preventing the end-effector from driving into the table surface or base enclosure.
   - **Layer 2 (Hardware StallGuard Auto-Cut)**: If an external physical obstacle (e.g. human hand or cup) resists movement, the TMC2209 driver registers high stall load, triggers an immediate emergency deceleration, and sends an alert event to Desktop Assistant.

## Consequences & Trade-offs
### Positive
- Extremely clean mechanical aesthetic with zero dangling limit switch wires.
- Low arm inertia enables high acceleration with smaller motors.
- Standard WebSocket protocol simplifies PC client debugging (inspectable via Chrome DevTools or Python).
- Double-redundant collision protection.

### Negative / Challenges to Manage
- **StallGuard Tuning**: Requires precise tuning of the `SGTHRS` register in firmware; too sensitive causes false stops, while too insensitive risks motor step loss or mechanical strain before detecting a stall.
- **Belt Tensioning CAD**: The mechanical CAD must incorporate adjustable belt tensioning idlers to prevent tooth skipping.
