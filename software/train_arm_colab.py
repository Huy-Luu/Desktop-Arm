"""
Desktop AI Robot Arm - Google Colab Training Starter Script
===========================================================
This script runs headless in Google Colab (with free T4 GPU).
It trains a Reinforcement Learning (PPO) policy to control a robot arm
in Google DeepMind's MuJoCo physics engine, then records an MP4 video of the result.

Colab Setup Instructions:
1. Open https://colab.research.google.com
2. Change runtime: Runtime > Change runtime type > T4 GPU
3. Run the installation cell:
   !pip install gymnasium[mujoco] stable-baselines3 shimmy imageio imageio-ffmpeg
"""

import os
import imageio
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

# Enable GPU-accelerated headless rendering in Colab
os.environ["MUJOCO_GL"] = "egl"

def main():
    print("=" * 60)
    print("1. Initializing MuJoCo Robot Arm Environment...")
    print("=" * 60)
    
    # Create the Reacher-v4 continuous control environment
    # In this task, a 2-DOF robotic arm must reach a random target sphere
    env = gym.make("Reacher-v4", render_mode="rgb_array")
    
    obs_dim = env.observation_space.shape
    action_dim = env.action_space.shape
    print(f"Observation dimension: {obs_dim} (Angles, velocities, target vector)")
    print(f"Action dimension:      {action_dim} (Motor torque controls)")
    
    print("\n" + "=" * 60)
    print("2. Setting up PPO Neural Network Policy...")
    print("=" * 60)
    
    model = PPO(
        policy="MlpPolicy",
        env=env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.0,
        verbose=1,
        tensorboard_log="./ppo_reacher_tensorboard/"
    )
    
    print("\n" + "=" * 60)
    print("3. Training Policy (100,000 steps ~ 2-3 mins on Colab GPU)...")
    print("=" * 60)
    
    model.learn(total_timesteps=100_000)
    
    # Save the trained model checkpoint
    model_filename = "robot_arm_ppo_model.zip"
    model.save(model_filename)
    print(f"\nModel saved successfully as: {model_filename}")
    
    print("\n" + "=" * 60)
    print("4. Evaluating Trained Policy...")
    print("=" * 60)
    
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"Evaluation over 10 episodes: Mean Reward = {mean_reward:.2f} +/- {std_reward:.2f}")
    
    print("\n" + "=" * 60)
    print("5. Rendering Evaluation Video to MP4...")
    print("=" * 60)
    
    frames = []
    obs, _ = env.reset()
    
    for step in range(300):
        # Deterministic inference using trained policy
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Render camera frame
        frame = env.render()
        frames.append(frame)
        
        if terminated or truncated:
            obs, _ = env.reset()
            
    video_filename = "robot_arm_reacher_demo.mp4"
    imageio.mimsave(video_filename, frames, fps=30)
    print(f"Video saved to: {video_filename}")
    print("Done! If running in Colab, display using: IPython.display.Video('robot_arm_reacher_demo.mp4')")

if __name__ == "__main__":
    main()
