# ADR 0003: 24V Bus, PLA Thermal Mitigation, and Rack-and-Pinion Gripper

- **Status**: Accepted
- **Date**: 2026-10-04
- **Deciders**: User & AI Pair

## Context & Problem Statement
With stepper motors selected for the base and shoulder (ADR 0001, ADR 0002), specific decisions were required regarding power supply voltage, fabrication materials (3D printing filament), and end-effector mechanics for desktop item manipulation.

## Decision Drivers
1. **High Stepper Back-EMF Headroom**: Steppers require higher DC voltage at higher RPMs to overcome inductance; 24V provides dramatically superior torque curves compared to 12V.
2. **Fabrication Simplicity**: PLA is the most accessible, dimensionally accurate filament for beginners, but has a low glass transition temperature ($T_g \approx 55^\circ\text{C}-60^\circ\text{C}$).
3. **Versatile Grasping**: A parallel-jaw mechanism keeps finger faces planar, ideal for grasping cuboids, markers, and cylinders.

## Decision Outcome
1. **Power Supply**: **24V 5A DC Power Supply (120W)**:
   - Direct 24V feed to the TMC2209 stepper driver $V_{MOT}$ pins for cool, high-torque operation.
   - Base PCB incorporates a high-voltage switching buck converter (e.g. `TPS54302`, rated up to 28V input) to step 24V down to 5.0V @ 3A for Desktop Assistant charging and servo power.
2. **Fabrication & Thermal Strategy**: **Standard PLA / PLA+ with Active Thermal Design**:
   - The arm links and base will be 3D printed in PLA/PLA+ for ease of printing and rigid tolerances.
   - **Thermal Mitigation**:
     - Firmware sets TMC2209 run current to moderate levels (e.g. 500mA–650mA RMS) and drops to 30% hold current during stationary pauses.
     - The base CAD will integrate ducting and a quiet 4010 24V cooling fan blowing over the stepper motor cans and driver heatsinks.
3. **End-Effector**: **Symmetrical Rack-and-Pinion Parallel Gripper**:
   - Single metal-gear micro-servo (MG90S) turning a central spur pinion.
   - Drives two opposed gear racks with silicone/rubber friction pads, ensuring objects are gripped symmetrically along the arm's centerline.

## Consequences & Trade-offs
### Positive
- 24V operation eliminates motor stalling during rapid trajectory moves.
- PLA prints reliably without warping or requiring heated enclosures.
- Symmetrical parallel grasping simplifies MuJoCo grasp physics modeling and inverse kinematics grasp pose calculations.

### Negative / Challenges to Manage
- 24V requires careful PCB layout and component rating (capacitors must be rated for $\ge 35\text{V}$, TVS clamp $\approx 27\text{V}-30\text{V}$).
- Forgetting to tune motor current in firmware could cause PLA brackets to warp over extended run sessions.
