# 🦾 Desktop AI Robot Arm

An educational, 6-DOF (Degree of Freedom) desktop robotic manipulator integrated with the **Desktop Assistant** companion robot, serving as a hands-on learning laboratory for mastering **Robotic AI, Google MuJoCo Simulation, Reinforcement Learning, Embedded Firmware, KiCad PCB, and FreeCAD CAD**.

---

## 📌 Start Here

If you are returning to this project or starting a new session, open the dedicated beginner guide:
👉 **[📖 Beginner Guide & Master Roadmap](docs/BEGINNER_GUIDE_AND_ROADMAP.md)**

This guide explains:
1. **Why we train in simulation first** (Safety, Speed, and Instant Iteration).
2. **Key concepts demystified** (*Homography, Synthetic Test Harness, Domain Randomization, ONNX*).
3. **The 4-Phase Master Roadmap** from virtual simulation to physical desk manipulation.
4. **Current ticket status & next steps**.

---

## 🏛️ Project Directory Structure

```text
deskto-AI-arm/
├── README.md                      # Project root overview (this file)
├── MISSION.md                     # Why this project exists & definition of success
├── GLOSSARY.md                    # Ubiquitous robotics & AI domain dictionary
├── NOTES.md                       # Architectural decisions & hardware preferences
├── RESOURCES.md                   # High-trust documentation and community links
│
├── docs/
│   ├── BEGINNER_GUIDE_AND_ROADMAP.md # Comprehensive guide and master roadmap
│   ├── SYSTEM_DESIGN_DOCUMENT.md     # Authoritative Master System Design Document
│   ├── SPEC-0001-desktop-ai-arm.md   # Complete system architecture specification
│   ├── adr/                          # Architectural Decision Records (ADRs 0001–0005)
│   └── tickets/                      # Tracer-bullet tickets (TICKET-01 to TICKET-12)
│
├── software/
│   ├── models/
│   │   └── desktop_arm_6dof.xml      # Google DeepMind MuJoCo 6-DOF arm physics model
│   ├── arm_env_3d.py                 # Gymnasium continuous-control environment
│   ├── test_sim.py                   # Sanity test verifying 6-DOF physics simulation
│   ├── train_arm_3d_6dof.ipynb       # Google Colab GPU training notebook (PPO)
│   └── gemini_vision_planner.py      # Google Gemini 2.0 Flash spatial perception
│
├── hardware/                         # FreeCAD 3D models & KiCad base controller schematics
├── firmware/                         # ESP32-S3 FreeRTOS motor control & StallGuard4 homing
└── reference/                        # Quick-reference cheatsheets & fundamentals
```

---

## 🚦 Current Status & Next Step

- **TICKET-01 (Simulation Verification)**: ✅ **COMPLETED**. MuJoCo 6-DOF environment verified with [test_sim.py](file:///mnt/g/projects/deskto-AI-arm/software/test_sim.py).
- **TICKET-02 (Colab PPO Training & ONNX Export)**: ✅ **COMPLETED**. Vectorized notebook with Domain Randomization and ONNX actor export ready in [software/train_arm_3d_6dof.ipynb](file:///mnt/g/projects/deskto-AI-arm/software/train_arm_3d_6dof.ipynb). See [Lesson 0001](file:///mnt/g/projects/deskto-AI-arm/lessons/0001-colab-ppo-and-domain-randomization.html) and [test_ticket02.py](file:///mnt/g/projects/deskto-AI-arm/software/test_ticket02.py).
- **TICKET-03 (Local PC ONNX Inference & Workspace Geofence)**: 🎯 **CURRENT NEXT STEP**. Deploy `arm_policy.onnx` locally on CPU with 3D table safety boundaries.

To resume at any time in a new chat, simply tell the assistant:
> *"I'm ready to continue. Let's work on TICKET-03 (Local PC ONNX Inference and Workspace Geofencing)."*
