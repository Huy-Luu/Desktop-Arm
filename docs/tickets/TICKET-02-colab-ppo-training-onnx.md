# TICKET-02: Colab PPO RL Training with Domain Randomization & ONNX Export

- **Status**: Ready
- **Blocked By**: TICKET-01
- **Delivers**: Google Colab training notebook (`software/train_arm_3d_6dof.ipynb`) running continuous-control PPO with randomized friction/mass/latency and exporting `arm_policy.onnx`.

## Acceptance Criteria
1. Vectorized parallel environments running at >2,000 FPS on Colab T4 GPU.
2. Domain randomization applied: joint damping/friction ($\pm 20\%$), link mass ($\pm 15\%$), latency ($10-30\text{ ms}$).
3. Policy converges to $>85\%$ target reaching success rate within 300k steps.
4. Export actor network to `software/models/arm_policy.onnx`.
