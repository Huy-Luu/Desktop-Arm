# TICKET-07: Stepper Driver Stage (3x TMC2209) & Micro-Servo Bus KiCad Schematic

- **Status**: Blocked
- **Blocked By**: TICKET-06
- **Delivers**: Motor drive section of Base Controller PCB, integrating 3x TMC2209 stepper driver sockets with UART address tuning, StallGuard DIAG lines, and 3x PWM micro-servo headers.

## Acceptance Criteria
1. 3x TMC2209 step/dir driver sockets with $100\mu\text{F}$ 35V low-ESR bulk electrolytic capacitors on $V_{MOT}$.
2. Shared single-wire UART line for software current tuning and StallGuard threshold configuration.
3. Dedicated `DIAG` pins routed to MCU external interrupt GPIOs for sensorless homing and collision cut-off.
4. 3x 3-pin standard 2.54mm headers (5V, GND, PWM) for wrist pitch, wrist roll, and gripper servos.
