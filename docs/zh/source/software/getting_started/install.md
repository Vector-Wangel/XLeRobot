### 安装LeRobot 🤗

要安装LeRobot，请按照[官方安装指南](https://huggingface.co/docs/lerobot/installation)

```{note}
建议使用`pip install -e .`以便更方便的文件传输。
```

如果您还没有配置[SO101手臂](https://huggingface.co/docs/lerobot/so101#configure-the-motors)和[其他电机](https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble.html#configure-motors)的电机，请进行配置。


## 安装XLeRobot插件

XLeRobot以一组LeRobot插件的形式提供：一个包含SO101运动学工具的共享模块，以及每种机器人底盘和遥操作方式各自对应的插件。

克隆本仓库，然后安装共享模块和您需要的插件：

```bash
git clone https://github.com/Vector-Wangel/XLeRobot.git
cd XLeRobot

pip install -e software/plugins/xlerobot_model
pip install -e software/plugins/lerobot_robot_xlerobot          # 三全向轮底盘
pip install -e software/plugins/lerobot_robot_xlerobot_2wheels  # 双轮差速驱动底盘
pip install -e software/plugins/lerobot_robot_xlerobot_mecanum  # 麦克纳姆轮底盘
pip install -e software/plugins/lerobot_teleoperator_xlerobot_vr  # VR遥操作
```

```{note}
如果您想基于树莓派构建，请在`software/src/robots/`下对应插件的`__init__.py`中取消注释`xlerobot_host`和`xlerobot_client`。
```

`--robot.type=xlerobot` / `xlerobot_2wheels` / `xlerobot_mecanum`
和`--teleop.type=xlerobot_vr`现在可以在任何标准的LeRobot命令行工具中使用
（`lerobot-teleoperate`、`lerobot-record`等）。
