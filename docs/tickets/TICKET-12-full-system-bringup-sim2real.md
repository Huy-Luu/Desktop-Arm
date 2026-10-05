# TICKET-12: Full Physical System Bringup & Sim-to-Real Deployment

- **Status**: Blocked
- **Blocked By**: TICKET-05, TICKET-08, TICKET-09, TICKET-10, TICKET-11
- **Delivers**: Integrated physical robot arm connected to base dock with Desktop Assistant seated, demonstrating complete end-to-end voice-commanded pick-and-place with visual feedback.

## Acceptance Criteria
1. Desktop Assistant docks smoothly onto the base, detects dock presence, and charges battery.
2. User speaks: *"Pick up the green marker"*.
3. Desktop Assistant streams voice to PC; Gemini vision planner identifies 3D target coordinates.
4. ONNX policy / kinematics streamer sends joint trajectory to Arm Base MCU.
5. Arm executes motion silently, grasps marker with rack-and-pinion gripper, and Desktop Assistant displays celebratory face animation on LCD.
