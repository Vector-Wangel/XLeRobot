<!-- THIS IS ALL GENERATED DOCUMENTATION via generate_robot_docs.py. DO NOT MODIFY THIS FILE DIRECTLY. -->

# Software

Here we will show how to run XLeRobot under the lerobot framework.

```{xl-flow}
lanes:
  - label: Imitation learning
    note: VLA tutorials from the community
    items:
      - {icon: gamepad, title: Record demos, text: Teleoperate to collect a dataset., chips: [Leader arm, VR], link: "doc:software/getting_started/VLA_ACT"}
      - {icon: brain, title: Train a policy, text: Fine-tune on your dataset., chips: [ACT, SmolVLA, π0.5], link: "doc:software/getting_started/VLA_smol"}
      - {icon: robot, title: Deploy, text: Run the policy on XLeRobot., link: "doc:software/getting_started/VLA_ACT"}
  - label: Reinforcement learning
    note: Full XLeRobot RL code is coming soon
    items:
      - {icon: cube, title: Simulate, text: ManiSkill environments., link: "doc:simulation/index"}
      - {icon: arrows-rotate, title: Train with RL, text: Try on a single SO101 arm first., chips: [lerobot-sim2real, HIL-SERL], link: "doc:software/getting_started/RL"}
      - {icon: robot, title: Sim2real, text: Deploy to the real robot., link: "doc:software/getting_started/RL"}
  - label: LLM agent
    note: Built on RoboCrew
    items:
      - {icon: microphone, title: Ask, text: Voice or text commands., link: "doc:software/getting_started/LLM_agent"}
      - {icon: eye, title: See and decide, text: The agent uses camera vision., link: "doc:software/getting_started/LLM_agent"}
      - {icon: robot, title: Act, text: Move the base and manipulate objects., link: "doc:software/getting_started/LLM_agent"}
```

### [Install LeRobot and Move XLeRobot files](getting_started/install.md)

### Quick Guide

```{note}
If you haven't played with lerobot SO101 Arm before, it's recommended to test single arm setup teleop and play with it for a while first.
```

1. **Choose Control Method**: Joint control (example 0) for basic motor testing, end-effector control for teleop (example 1 & 6)
2. **Advanced Features**: Try dual-arm control (example 2) or vision-based control (example 3) for more complex tasks
3. **Full System**: Use keyboard (example 4), Xbox controller (example 5), or Switch Joycon (example 7) for complete XLeRobot teleop

All example scripts are located in the [`software/examples/`](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/examples) directory and can be run directly after proper setup and calibration. Some examples needs additional calibration to ensure performance.

```{note}
For basic version of XLeRobot, you don't need a RaspberryPi. Just use your laptop and put it in the IKEA cart if you want to use the full system.
```

### [SO100/SO101 Arm Examples](getting_started/SO101.md)

### [XLeRobot Teleop](getting_started/XLeRobot_teleop.md)

### [Autonomous LLM Agent](getting_started/LLM_agent.md)

```{note}
The VLA tutorials below came from different teams in the community. Thanks a lot for their efforts!
```

### [VLA (1) ACT](getting_started/VLA_ACT.md)

### [VLA (2) SmolVLA and more](getting_started/VLA_smol.md)

### [VLA (3) pi0.5](getting_started/VLA_pi05.md)

### [Reinforcenment Learning (RL)](getting_started/RL.md)

### [Raspberri Pi Setup](getting_started/raspberry_pi_setup.md)


```{toctree}
getting_started/install
getting_started/SO101
getting_started/XLeRobot_teleop
getting_started/LLM_agent
getting_started/VLA_ACT
getting_started/VLA_smol
getting_started/VLA_pi05
getting_started/RL
getting_started/raspberry_pi_setup.md
```
