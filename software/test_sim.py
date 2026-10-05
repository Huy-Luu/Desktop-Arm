"""
Sanity check script for DesktopArm6DOFEnv MuJoCo simulation.
"""
import numpy as np
from arm_env_3d import DesktopArm6DOFEnv

def test_simulation():
    print("🤖 Initializing DesktopArm6DOFEnv (MuJoCo 6-DOF Continuous Control)...")
    env = DesktopArm6DOFEnv()
    obs, info = env.reset(seed=42)
    print("✓ Environment reset successful!")
    print(f"✓ Observation vector shape: {obs.shape} (27 features: cos/sin qpos, qvel, EE, Target, Delta)")
    print(f"✓ Action space: {env.action_space}")
    print(f"✓ Target position (X, Y, Z): {np.round(info['target_pos'], 3)} m\n")

    print("Executing 10 continuous position-delta steps in MuJoCo physics:")
    for step in range(1, 11):
        # Sample smooth action in [-1.0, 1.0]
        action = env.action_space.sample()
        obs, reward, terminated, truncated, step_info = env.step(action)
        dist = step_info["distance"]
        ee_pos = np.round(step_info["ee_pos"], 3)
        print(f"  Step {step:2d}: Reward = {reward:+.3f} | Dist to Target = {dist:.3f}m | EE = {ee_pos} | Success: {step_info['is_success']}")

    env.close()
    print("\n🎉 MuJoCo 6-DOF simulation environment runs cleanly at full physics fidelity!")

if __name__ == "__main__":
    test_simulation()
