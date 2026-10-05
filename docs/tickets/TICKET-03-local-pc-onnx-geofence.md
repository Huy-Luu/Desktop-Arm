# TICKET-03: Local PC ONNX Inference Engine with Workspace Geofencing

- **Status**: Blocked
- **Blocked By**: TICKET-02
- **Delivers**: Standalone Python runtime on host PC using `onnxruntime` enforcing virtual desk safety bounds and streaming joint angle packets.

## Acceptance Criteria
1. Loads `arm_policy.onnx` using `onnxruntime` with zero PyTorch dependency.
2. Inference latency $<5\text{ ms}$ per step on CPU.
3. Virtual 3D geofence prevents commanding end-effector below table surface ($Z < 0.02\text{ m}$) or into base pillar ($R < 0.08\text{ m}$).
