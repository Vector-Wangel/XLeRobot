# lerobot plugin packages

Each directory here is a small, independently pip-installable package: one
shared module with the SO101 kinematics helpers, and one plugin per robot
base or teleoperator. lerobot auto-imports any installed package whose name
starts with `lerobot_robot_`, `lerobot_teleoperator_`, etc.
(`register_third_party_plugins()` in `lerobot.utils.import_utils`), so
installing one of these makes its `--robot.type=...` /
`--teleop.type=...` available on any standard lerobot CLI
(`lerobot-teleoperate`, `lerobot-record`, ...).

Each package here is just a `pyproject.toml` plus a symlink back to the real
code under `../src/` — nothing was moved or renamed.

- `xlerobot_model/` — shared SO101 kinematics helpers, used by the robot,
  teleoperator, and example code.
- `lerobot_robot_xlerobot/` — the 3-omniwheel base (`--robot.type=xlerobot`).
- `lerobot_robot_xlerobot_2wheels/` — the 2-wheel differential drive base
  (`--robot.type=xlerobot_2wheels`).
- `lerobot_robot_xlerobot_mecanum/` — the mecanum-wheel base
  (`--robot.type=xlerobot_mecanum`).
- `lerobot_teleoperator_xlerobot_vr/` — the VR teleoperator
  (`--teleop.type=xlerobot_vr`).

## Install (editable, for development)

```bash
pip install -e software/plugins/xlerobot_model
pip install -e software/plugins/lerobot_robot_xlerobot
pip install -e software/plugins/lerobot_robot_xlerobot_2wheels
pip install -e software/plugins/lerobot_robot_xlerobot_mecanum
pip install -e software/plugins/lerobot_teleoperator_xlerobot_vr
```

## Verifying discovery

```bash
python -c "
from lerobot.utils.import_utils import register_third_party_plugins
register_third_party_plugins()
from lerobot.robots.config import RobotConfig
from lerobot.robots.utils import make_robot_from_config
for t in ['xlerobot', 'xlerobot_mecanum', 'xlerobot_2wheels']:
    print(t, '->', make_robot_from_config(RobotConfig.get_choice_class(t)(id='test')))
"
```

## Adding more

Follow the same pattern: a new directory here with a `pyproject.toml` and a
symlink to the corresponding folder under `../src/`.
