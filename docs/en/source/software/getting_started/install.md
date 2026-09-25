### Install LeRobot 🤗

To install LeRobot, follow the [official Installation Guide](https://huggingface.co/docs/lerobot/installation)

```{note}
It's recommended to use `pip install -e .` for a more convenient file transfer.
```

Configure the motors for [SO101 arms](https://huggingface.co/docs/lerobot/so101#configure-the-motors) and [other motors](https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble.html#configure-motors) if you haven't done so.


## Install XLeRobot's plugins

XLeRobot ships as a set of LeRobot plugins: a shared module with the SO101
kinematics helpers, plus one plugin per robot base and teleoperator.

Clone this repo, then install the shared module and the plugin(s) you need:

```bash
git clone https://github.com/Vector-Wangel/XLeRobot.git
cd XLeRobot

pip install -e software/plugins/xlerobot_model
pip install -e software/plugins/lerobot_robot_xlerobot          # 3-omniwheel base
pip install -e software/plugins/lerobot_robot_xlerobot_2wheels  # 2-wheel differential drive
pip install -e software/plugins/lerobot_robot_xlerobot_mecanum  # mecanum-wheel base
pip install -e software/plugins/lerobot_teleoperator_xlerobot_vr  # VR teleop
```

```{note}
If you want to build based on RaspberryPi, uncomment `xlerobot_host` and
`xlerobot_client` in the plugin's `__init__.py` under `software/src/robots/`.
```

`--robot.type=xlerobot` / `xlerobot_2wheels` / `xlerobot_mecanum` and
`--teleop.type=xlerobot_vr` now work on any standard LeRobot CLI command
(`lerobot-teleoperate`, `lerobot-record`, ...).
