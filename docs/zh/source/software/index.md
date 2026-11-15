<!-- THIS IS ALL GENERATED DOCUMENTATION via generate_robot_docs.py. DO NOT MODIFY THIS FILE DIRECTLY. -->

# 软件

这里我们将展示如何在lerobot框架下运行XLeRobot。

```{xl-flow}
lanes:
  - label: 模仿学习
    note: 社区贡献的 VLA 教程
    items:
      - {icon: gamepad, title: 采集演示, text: 遥操作录制数据集。, chips: [主臂, VR], link: "doc:software/getting_started/VLA_ACT"}
      - {icon: brain, title: 训练策略, text: 在你的数据集上微调。, chips: [ACT, SmolVLA, π0.5], link: "doc:software/getting_started/VLA_smol"}
      - {icon: robot, title: 部署, text: 在 XLeRobot 上运行策略。, link: "doc:software/getting_started/VLA_ACT"}
  - label: 强化学习
    note: 完整的 XLeRobot RL 代码即将发布
    items:
      - {icon: cube, title: 仿真, text: ManiSkill 环境。, link: "doc:simulation/index"}
      - {icon: arrows-rotate, title: RL 训练, text: 可先在单个 SO101 手臂上尝试。, chips: [lerobot-sim2real, HIL-SERL], link: "doc:software/getting_started/RL"}
      - {icon: robot, title: Sim2real, text: 部署到真实机器人。, link: "doc:software/getting_started/RL"}
  - label: LLM 智能体
    note: 基于 RoboCrew
    items:
      - {icon: microphone, title: 下指令, text: 语音或文字命令。, link: "doc:software/getting_started/LLM_agent"}
      - {icon: eye, title: 观察与决策, text: 智能体借助相机视觉。, link: "doc:software/getting_started/LLM_agent"}
      - {icon: robot, title: 执行, text: 移动底盘、操作物体。, link: "doc:software/getting_started/LLM_agent"}
```

### [安装LeRobot 并移动XLeRobot文件](getting_started/install.md)

### 快速指南

```{note}
如果您之前没有使用过lerobot SO101手臂，建议先测试单臂设置遥操作并先熟悉一段时间。
```

1. **选择控制方法**: 关节控制(示例0)用于基本电机测试，末端执行器控制用于遥操作(示例1 & 6)
2. **高级功能**: 尝试双臂控制(示例2)或基于视觉的控制(示例3)进行更复杂的任务
3. **完整系统**: 使用键盘(示例4)、Xbox控制器(示例5)或Switch Joycon(示例7)进行完整的XLeRobot遥操作

所有示例脚本都位于[`software/examples/`](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/examples)目录中，在正确设置和校准后可以直接运行。某些示例需要额外校准以确保性能。

```{note}
对于XLeRobot的基础版本，您不需要树莓派。只需使用您的笔记本电脑，如果您想使用完整系统，可以将其放在宜家推车中。
```

### [SO100/SO101手臂示例](getting_started/SO101.md)

### [XLeRobot遥操作](getting_started/XLeRobot_teleop.md)

### [自主LLM Agent](getting_started/LLM_agent.md)

```{note}
下面的VLA教程来自社区的不同团队。非常感谢他们的努力！
```

### [VLA (1) ACT](getting_started/VLA_ACT.md)

### [VLA (2) SmolVLA and more](getting_started/VLA_smol.md)

### [VLA (3) pi0.5](getting_started/VLA_pi05.md)

### [强化学习(RL)](getting_started/RL.md)

### [树莓派设置](getting_started/raspberry_pi_setup.md)


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