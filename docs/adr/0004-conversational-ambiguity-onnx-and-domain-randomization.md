# ADR 0004: Conversational Disambiguation, ONNX Runtime Inference, and Domain Randomization

- **Status**: Accepted
- **Date**: 2026-10-04
- **Deciders**: User & AI Pair

## Context & Problem Statement
The high-level intelligence and motion control stack requires decisions across three distinct software layers:
1. **Perception Ambiguity**: How the system handles vague user instructions when multiple candidate targets are detected by the overhead camera.
2. **Model Deployment**: How the trained reinforcement learning policy is packaged and executed on the host PC.
3. **Reality Gap**: How the simulation-trained policy handles physical variances in real 3D-printed parts, belt elasticity, and motor latency.

## Decision Drivers
- Expressive, natural human-robot interaction leveraging Desktop Assistant's audio and visual capabilities.
- Minimal host runtime dependencies (avoiding heavy training frameworks like PyTorch or CUDA runtime on the host PC).
- Robust physical policy execution without manual micro-tuning on hardware.

## Decision Outcome
1. **Conversational Disambiguation via Desktop Assistant**:
   - When Gemini 2.0 Flash detects multiple objects matching the voice query (e.g., two pens or three colored cubes), it does not guess.
   - It emits a structured disambiguation prompt:
     ```json
     {
       "action": "disambiguate",
       "query": "I see a blue pen on the left and a black pen on the right. Which one would you like me to grab?",
       "candidates": [
         {"id": 1, "name": "blue pen", "bbox": [0.2, 0.4, 0.3, 0.5]},
         {"id": 2, "name": "black pen", "bbox": [0.6, 0.4, 0.7, 0.5]}
       ]
     }
     ```
   - Desktop Assistant's speaker plays this question and its circular LCD displays a questioning face expression.
2. **ONNX Policy Packaging & Inference**:
   - The PPO actor network trained in MuJoCo on Google Colab is exported to `.onnx` format (`actor_policy.onnx`).
   - The host PC executes the policy inside a lightweight, standalone Python or C++ runtime via `onnxruntime` (<5ms per inference step, zero PyTorch install required on host).
3. **Sim-to-Real Domain Randomization**:
   - Training episodes in MuJoCo on Google Colab undergo continuous physics randomization:
     - Joint friction & damping: $\pm 20\%$
     - Link masses and center-of-mass offsets: $\pm 15\%$
     - Command actuation latency: injected random delay of $10\text{ ms} - 30\text{ ms}$
     - Action noise: Gaussian perturbation $\mathcal{N}(0, 0.02)$ added to joint position deltas.
   - This prevents the policy from overfitting to perfect rigid-body simulator physics.

## Consequences & Trade-offs
### Positive
- Safe and delightful user experience: robot asks when uncertain instead of grabbing the wrong object.
- Host PC runs at minimal CPU/RAM utilization using `onnxruntime`.
- Robust real-world transfer: the arm policy handles minor belt elasticity and joint friction without failing.

### Negative / Challenges to Manage
- Disambiguation requires multi-turn conversational state tracking on the PC voice orchestrator.
- Domain randomization slightly extends Google Colab training time (e.g. from 200,000 steps to 400,000 steps to converge).
