"""
Desktop 3D 6-DOF Robot Arm - Gymnasium Environment
===================================================
A self-contained, continuous-control reinforcement learning environment
simulating a desktop 6-DOF robotic arm using Google DeepMind's MuJoCo.

Features:
- 6 revolute joints (Base Yaw, Shoulder Pitch, Elbow Pitch, Forearm Roll, Wrist Pitch, Tool Roll)
- End-effector 3D tracking & reaching target sphere
- Smooth position delta control simulating digital smart servos (e.g., Feetech/Dynamixel)
- Headless EGL rendering support for Google Colab
"""

import os
import sys
import numpy as np
import gymnasium as gym
from gymnasium import spaces

# Automatically configure NVIDIA EGL ICD on Linux/Colab if missing
if sys.platform.startswith("linux"):
    nvidia_icd_path = "/usr/share/glvnd/egl_vendor.d/10_nvidia.json"
    if not os.path.exists(nvidia_icd_path):
        try:
            os.makedirs(os.path.dirname(nvidia_icd_path), exist_ok=True)
            with open(nvidia_icd_path, "w") as f:
                f.write('{\n  "file_format_version" : "1.0.0",\n  "ICD" : {\n    "library_path" : "libEGL_nvidia.so.0"\n  }\n}')
        except Exception:
            pass

# Enable GPU-accelerated headless rendering by default on Linux
if "MUJOCO_GL" not in os.environ:
    os.environ["MUJOCO_GL"] = "egl"
DESKTOP_ARM_6DOF_XML = """
<mujoco model="desktop_arm_6dof">
  <compiler angle="radian" coordinate="local" inertiafromgeom="true"/>
  <option timestep="0.005" gravity="0 0 -9.81" integrator="Euler"/>
  
  <default>
    <joint damping="0.8" armature="0.01"/>
    <geom contype="1" conaffinity="1" friction="0.8 0.1 0.1"/>
    <position kp="40" kv="5"/>
  </default>

  <asset>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0.1 0.1 0.2" width="512" height="512"/>
    <texture name="grid" type="2d" builtin="checker" rgb1="0.85 0.85 0.85" rgb2="0.65 0.65 0.65" width="512" height="512"/>
    <material name="grid_mat" texture="grid" texrepeat="5 5" reflectance="0.1"/>
    <material name="arm_mat" rgba="0.15 0.45 0.85 1.0" specular="0.4" shininess="0.3"/>
    <material name="joint_mat" rgba="0.95 0.55 0.1 1.0" specular="0.5" shininess="0.4"/>
    <material name="flange_mat" rgba="0.25 0.25 0.28 1.0" specular="0.2"/>
    <material name="target_mat" rgba="0.95 0.15 0.15 0.85" specular="0.6" shininess="0.6"/>
    <material name="table_mat" rgba="0.9 0.9 0.92 1.0" specular="0.2"/>
    <material name="ee_mat" rgba="0.1 0.85 0.3 1.0" specular="0.5"/>
  </asset>

  <worldbody>
    <light pos="0.2 -0.3 1.5" dir="-0.2 0.3 -1.0" diffuse="0.85 0.85 0.85" specular="0.3 0.3 0.3"/>
    <light pos="-0.5 0.5 1.2" dir="0.5 -0.5 -1.0" diffuse="0.4 0.4 0.4"/>

    <geom name="floor" type="plane" size="1.2 1.2 0.05" material="grid_mat"/>

    <body name="table" pos="0 0 0.15">
      <geom name="table_top" type="box" size="0.35 0.35 0.015" material="table_mat"/>
      <geom name="table_leg1" type="cylinder" size="0.02 0.07" pos="0.3 0.3 -0.075" material="flange_mat"/>
      <geom name="table_leg2" type="cylinder" size="0.02 0.07" pos="-0.3 0.3 -0.075" material="flange_mat"/>
      <geom name="table_leg3" type="cylinder" size="0.02 0.07" pos="0.3 -0.3 -0.075" material="flange_mat"/>
      <geom name="table_leg4" type="cylinder" size="0.02 0.07" pos="-0.3 -0.3 -0.075" material="flange_mat"/>
    </body>

    <body name="target" pos="0.15 0.10 0.32" mocap="true">
      <geom name="target_geom" type="sphere" size="0.025" material="target_mat" contype="0" conaffinity="0"/>
      <site name="target_site" pos="0 0 0" size="0.008" rgba="1 1 1 0.9"/>
    </body>

    <body name="arm_base" pos="0 0 0.165">
      <geom name="base_plate" type="cylinder" size="0.065 0.015" material="flange_mat"/>
      <geom name="base_pillar" type="cylinder" size="0.045 0.03" pos="0 0 0.03" material="arm_mat"/>

      <body name="link1" pos="0 0 0.06">
        <joint name="joint1_base_yaw" type="hinge" axis="0 0 1" range="-3.1416 3.1416"/>
        <geom name="j1_cylinder" type="cylinder" size="0.04 0.025" material="joint_mat"/>

        <body name="link2" pos="0 0 0.04">
          <joint name="joint2_shoulder_pitch" type="hinge" axis="0 1 0" range="-1.5708 1.5708"/>
          <geom name="j2_hub" type="cylinder" size="0.03 0.025" fromto="0 -0.025 0 0 0.025 0" material="joint_mat"/>
          <geom name="upper_arm" type="capsule" fromto="0 0 0 0 0 0.14" size="0.022" material="arm_mat"/>

          <body name="link3" pos="0 0 0.14">
            <joint name="joint3_elbow_pitch" type="hinge" axis="0 1 0" range="-2.0944 2.0944"/>
            <geom name="j3_hub" type="cylinder" size="0.026 0.022" fromto="0 -0.022 0 0 0.022 0" material="joint_mat"/>
            <geom name="forearm" type="capsule" fromto="0 0 0 0 0 0.12" size="0.018" material="arm_mat"/>

            <body name="link4" pos="0 0 0.12">
              <joint name="joint4_wrist_roll" type="hinge" axis="0 0 1" range="-3.1416 3.1416"/>
              <geom name="j4_swivel" type="cylinder" size="0.018 0.015" pos="0 0 0.015" material="joint_mat"/>

              <body name="link5" pos="0 0 0.03">
                <joint name="joint5_wrist_pitch" type="hinge" axis="0 1 0" range="-1.5708 1.5708"/>
                <geom name="j5_hub" type="sphere" size="0.018" material="joint_mat"/>
                <geom name="wrist_link" type="capsule" fromto="0 0 0 0 0 0.035" size="0.014" material="arm_mat"/>

                <body name="link6_flange" pos="0 0 0.035">
                  <joint name="joint6_tool_roll" type="hinge" axis="0 0 1" range="-3.1416 3.1416"/>
                  <geom name="tool_disc" type="cylinder" size="0.02 0.008" pos="0 0 0.008" material="flange_mat"/>

                  <geom name="gripper_base" type="box" size="0.025 0.008 0.006" pos="0 0 0.018" material="flange_mat"/>
                  <geom name="finger_left" type="box" size="0.004 0.008 0.018" pos="-0.016 0 0.032" material="joint_mat"/>
                  <geom name="finger_right" type="box" size="0.004 0.008 0.018" pos="0.016 0 0.032" material="joint_mat"/>

                  <site name="ee_site" pos="0 0 0.045" size="0.008" rgba="0.1 0.9 0.3 0.9"/>
                </body>
              </body>
            </body>
          </body>
        </body>
      </body>
    </body>

    <camera name="cam_isometric" pos="0.55 -0.55 0.65" xyaxes="0.707 0.707 0 -0.408 0.408 0.816"/>
    <camera name="cam_front" pos="0 -0.65 0.45" xyaxes="1 0 0 0 0.45 0.893"/>
    <camera name="cam_overhead" pos="0 0 0.9" xyaxes="1 0 0 0 1 0"/>
  </worldbody>

  <actuator>
    <position name="act_j1" joint="joint1_base_yaw" kp="50" ctrlrange="-3.1416 3.1416"/>
    <position name="act_j2" joint="joint2_shoulder_pitch" kp="60" ctrlrange="-1.5708 1.5708"/>
    <position name="act_j3" joint="joint3_elbow_pitch" kp="50" ctrlrange="-2.0944 2.0944"/>
    <position name="act_j4" joint="joint4_wrist_roll" kp="30" ctrlrange="-3.1416 3.1416"/>
    <position name="act_j5" joint="joint5_wrist_pitch" kp="25" ctrlrange="-1.5708 1.5708"/>
    <position name="act_j6" joint="joint6_tool_roll" kp="20" ctrlrange="-3.1416 3.1416"/>
  </actuator>
</mujoco>
"""

class DesktopArm6DOFEnv(gym.Env):
    """
    Continuous control 3D 6-DOF Desktop Robot Arm Environment.
    
    Action Space:
        Box(-1.0, 1.0, shape=(6,))
        Continuous control commands representing delta position updates to the 6 servo actuators.
        
    Observation Space:
        Box(-inf, inf, shape=(27,))
        - cos(qpos[0..5]): 6 values
        - sin(qpos[0..5]): 6 values
        - qvel[0..5]:      6 values (joint velocities)
        - ee_pos:          3 values (current end-effector X, Y, Z)
        - target_pos:      3 values (target X, Y, Z)
        - delta_pos:       3 values (target_pos - ee_pos)
    """
    metadata = {"render_modes": ["rgb_array"], "render_fps": 40}

    def __init__(self, xml_path=None, render_mode=None, max_episode_steps=150, camera_name="cam_isometric", domain_randomization=False):
        super().__init__()
        
        # Enable GPU-accelerated headless rendering if running in Colab/Linux
        if "MUJOCO_GL" not in os.environ:
            os.environ["MUJOCO_GL"] = "egl"
            
        import mujoco
        self.mujoco = mujoco

        # Load MuJoCo model
        if xml_path and os.path.exists(xml_path):
            with open(xml_path, "r") as f:
                xml_string = f.read()
        else:
            xml_string = DESKTOP_ARM_6DOF_XML.strip()

        self.model = mujoco.MjModel.from_xml_string(xml_string)
        self.data = mujoco.MjData(self.model)

        self.render_mode = render_mode
        self.camera_name = camera_name
        self.max_episode_steps = max_episode_steps
        self.domain_randomization = domain_randomization
        self.step_count = 0
        self.frame_skip = 5  # 5 * 0.005s = 0.025s per step (40 Hz control frequency)
        self.action_scale = 0.05  # Maximum radian delta per control step

        # Nominal physics properties for Domain Randomization
        self.default_dof_damping = self.model.dof_damping.copy()
        self.default_body_mass = self.model.body_mass.copy()
        self.default_geom_friction = self.model.geom_friction.copy()
        self.prev_action = np.zeros(6, dtype=np.float32)

        # Extract IDs
        self.ee_site_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_SITE, "ee_site")
        self.target_mocap_id = 0  # First mocap body in the model is 'target'

        # Joint control limits
        self.ctrl_min = self.model.actuator_ctrlrange[:, 0]
        self.ctrl_max = self.model.actuator_ctrlrange[:, 1]

        # Action and Observation Spaces
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(6,), dtype=np.float32
        )

        # 12 (cos/sin angles) + 6 (velocities) + 3 (ee_pos) + 3 (target_pos) + 3 (diff) = 27
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(27,), dtype=np.float32
        )

        self.renderer = None
        self.target_pos = np.array([0.15, 0.10, 0.32], dtype=np.float32)

    def _get_obs(self):
        qpos = self.data.qpos[:6].copy()
        qvel = self.data.qvel[:6].copy()
        ee_pos = self.data.site_xpos[self.ee_site_id].copy()
        delta_pos = self.target_pos - ee_pos

        obs = np.concatenate([
            np.cos(qpos),
            np.sin(qpos),
            qvel,
            ee_pos,
            self.target_pos,
            delta_pos
        ]).astype(np.float32)
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.step_count = 0
        self.prev_action = np.zeros(6, dtype=np.float32)

        # Reset MuJoCo physics state
        self.mujoco.mj_resetData(self.model, self.data)

        # Domain Randomization (Sim-to-Real): perturb physics if active
        if self.domain_randomization:
            # 1. Joint damping perturbation: +/- 20%
            damping_noise = self.np_random.uniform(0.8, 1.2, size=len(self.default_dof_damping))
            self.model.dof_damping[:] = self.default_dof_damping * damping_noise
            
            # 2. Link mass perturbation: +/- 15%
            mass_noise = self.np_random.uniform(0.85, 1.15, size=len(self.default_body_mass))
            self.model.body_mass[:] = self.default_body_mass * mass_noise
            
            # 3. Geom friction perturbation: +/- 20%
            friction_noise = self.np_random.uniform(0.8, 1.2, size=len(self.default_geom_friction))
            self.model.geom_friction[:, 0] = self.default_geom_friction[:, 0] * friction_noise
        else:
            self.model.dof_damping[:] = self.default_dof_damping
            self.model.body_mass[:] = self.default_body_mass
            self.model.geom_friction[:] = self.default_geom_friction

        # Initialize to a natural home pose (slight bend in shoulder and elbow)
        home_qpos = np.array([0.0, 0.35, 0.55, 0.0, 0.2, 0.0])
        noise = self.np_random.uniform(-0.05, 0.05, size=6)
        self.data.qpos[:6] = home_qpos + noise
        self.data.qvel[:6] = 0.0
        self.data.ctrl[:6] = self.data.qpos[:6]

        # Sample a randomized 3D target position within reachable workspace
        # Cylindrical coordinates: radius r, angle theta, height z
        r = self.np_random.uniform(0.12, 0.28)
        theta = self.np_random.uniform(-np.pi * 0.75, np.pi * 0.75)
        z = self.np_random.uniform(0.20, 0.38)

        self.target_pos = np.array([
            r * np.cos(theta),
            r * np.sin(theta),
            z
        ], dtype=np.float32)

        # Set target mocap position in MuJoCo
        self.data.mocap_pos[self.target_mocap_id] = self.target_pos

        # Step forward kinematics
        self.mujoco.mj_forward(self.model, self.data)

        obs = self._get_obs()
        info = {"target_pos": self.target_pos.copy()}
        return obs, info

    def step(self, action):
        self.step_count += 1
        action = np.clip(action, -1.0, 1.0)

        # Domain Randomization: Command latency & action noise
        if self.domain_randomization:
            alpha = float(self.np_random.uniform(0.6, 0.9))
            filtered_action = (1.0 - alpha) * self.prev_action + alpha * action
            noise = self.np_random.normal(0.0, 0.02, size=6).astype(np.float32)
            applied_action = np.clip(filtered_action + noise, -1.0, 1.0)
            self.prev_action = action.copy()
        else:
            applied_action = action

        # Update position setpoints incrementally for smooth trajectory
        target_ctrl = self.data.ctrl[:6] + (applied_action * self.action_scale)
        self.data.ctrl[:6] = np.clip(target_ctrl, self.ctrl_min, self.ctrl_max)

        # Run MuJoCo physics simulation
        for _ in range(self.frame_skip):
            self.mujoco.mj_step(self.model, self.data)

        ee_pos = self.data.site_xpos[self.ee_site_id]
        dist = np.linalg.norm(ee_pos - self.target_pos)

        # Continuous reward function
        reward_dist = -dist
        reward_action = -0.005 * np.sum(np.square(action))
        reward_bonus = 0.0

        is_success = dist < 0.03  # Within 3 cm tolerance
        if is_success:
            reward_bonus = 2.0
        elif dist < 0.06:
            reward_bonus = 0.5

        reward = float(reward_dist + reward_action + reward_bonus)

        # Terminate or truncate
        terminated = False
        truncated = self.step_count >= self.max_episode_steps

        obs = self._get_obs()
        info = {
            "distance": float(dist),
            "is_success": is_success,
            "ee_pos": ee_pos.copy(),
            "target_pos": self.target_pos.copy()
        }

        return obs, reward, terminated, truncated, info

    def render(self):
        if self.render_mode != "rgb_array":
            return None
        if self.renderer is None:
            try:
                self.renderer = self.mujoco.Renderer(self.model, height=480, width=640)
            except Exception as e:
                # Fallback to software CPU renderer if EGL context fails
                try:
                    os.environ["MUJOCO_GL"] = "osmesa"
                    self.renderer = self.mujoco.Renderer(self.model, height=480, width=640)
                except Exception:
                    raise RuntimeError(f"MuJoCo rendering failed: {e}. Check GPU and EGL configuration.")

        self.renderer.update_scene(self.data, camera=self.camera_name)
        return self.renderer.render()

    def close(self):
        if self.renderer is not None:
            self.renderer.close()
            self.renderer = None
