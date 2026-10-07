# 0001: PPO, Vectorized Simulation, Domain Randomization, and ONNX

The user is entering Phase 1 Reinforcement Learning as a beginner. We established the four architectural pillars of cloud training: vectorized environments for 16x parallel sample collection, PPO actor-critic dynamics with clipping to prevent catastrophic policy forgetting, domain randomization to bridge the physical reality gap across friction/mass/latency, and ONNX export for lightweight sub-5ms CPU deployment without PyTorch dependencies.

## Implications
- The zone of proximal development now centers on hands-on code execution: inspecting environment observations, testing parameter perturbations, and training in Google Colab.
- The user can move directly into running `software/train_arm_3d_6dof.ipynb` on Colab to train their first neural network policy and download `arm_policy.onnx`.
