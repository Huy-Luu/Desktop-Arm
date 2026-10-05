# TICKET-01: MuJoCo 6-DOF Simulation Verification & End-to-End IK Baseline

- **Status**: Completed / Verified
- **Blocked By**: None
- **Delivers**: Runnable Python simulation verifying joint axes, forward/inverse kinematics, observation vectors, and 3D reaching targets.

## Details
1. Verify `software/arm_env_3d.py` in MuJoCo 3.x.
2. Ensure 27-dimensional observation space (cos/sin joint angles, angular velocity, end-effector position, target position, delta).
3. Validate continuous position-delta control in $[-1.0, 1.0]$.
4. Test with `software/test_sim.py`.
