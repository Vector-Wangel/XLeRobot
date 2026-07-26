"""GenesisXLeRobot: a lerobot ``Robot`` backed by the Genesis simulation.

Mirrors the real ``XLerobot``'s feature dicts exactly (17 `*.pos`/`*.vel` keys +
`{cam}:(H,W,3)` images), so the same policy loop drives sim or real. It wraps the
sim `XLeRobotEnvironment` and owns the LeRobot-facing naming + units (deg<->rad).
"""

import sys
from functools import cached_property
from pathlib import Path
from typing import Any, Dict

import numpy as np

from lerobot.robots.robot import Robot

from .config_genesis_xlerobot import GenesisXLeRobotConfig

# simulation/genesis on path for the environment + component imports.
_SIM_ROOT = Path(__file__).resolve().parents[4] / "simulation" / "genesis"
sys.path.insert(0, str(_SIM_ROOT))

from environments.test_environment import XLeRobotEnvironment  # noqa: E402

# Software state key -> URDF joint, in the real XLerobot `_state_order`:
# [left arm 6, right arm 6, head 2] positions, then [base 3] velocities.
POSITION_KEYS = (
    "left_arm_shoulder_pan.pos", "left_arm_shoulder_lift.pos", "left_arm_elbow_flex.pos",
    "left_arm_wrist_flex.pos", "left_arm_wrist_roll.pos", "left_arm_gripper.pos",
    "right_arm_shoulder_pan.pos", "right_arm_shoulder_lift.pos", "right_arm_elbow_flex.pos",
    "right_arm_wrist_flex.pos", "right_arm_wrist_roll.pos", "right_arm_gripper.pos",
    "head_motor_1.pos", "head_motor_2.pos",
)
POSITION_URDF_JOINTS = (
    "Rotation_2", "Pitch_2", "Elbow_2", "Wrist_Pitch_2", "Wrist_Roll_2", "Jaw_2",
    "Rotation", "Pitch", "Elbow", "Wrist_Pitch", "Wrist_Roll", "Jaw",
    "head_pan_joint", "head_tilt_joint",
)
BASE_KEYS = ("x.vel", "y.vel", "theta.vel")
BASE_URDF_JOINTS = ("root_x_axis_joint", "root_y_axis_joint", "root_z_rotation_joint")
STATE_KEYS = POSITION_KEYS + BASE_KEYS


class GenesisXLeRobot(Robot):
    config_class = GenesisXLeRobotConfig
    name = "genesis_xlerobot"

    def __init__(self, config: GenesisXLeRobotConfig):
        super().__init__(config)
        self.config = config
        self.state_units = config.state_units
        self.env = None
        self._connected = False
        cameras = config.sim_config.get("cameras", {})
        self.camera_keys = list(cameras)
        # observation_features image shapes are (H, W, 3); camera res is (W, H).
        self.camera_shapes = {
            key: (cam["res"][1], cam["res"][0], 3) for key, cam in cameras.items()
        }

    @cached_property
    def _state_ft(self) -> Dict:
        return {key: float for key in STATE_KEYS}

    @property
    def observation_features(self) -> Dict:
        return {**self._state_ft, **self.camera_shapes}

    @property
    def action_features(self) -> Dict:
        return self._state_ft

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def is_calibrated(self) -> bool:
        return True

    def connect(self, calibrate: bool = True) -> None:
        self.env = XLeRobotEnvironment.from_config(self.config.sim_config).build()
        self._connected = True

    def calibrate(self) -> None:
        pass

    def configure(self) -> None:
        pass

    def get_observation(self) -> Dict[str, Any]:
        positions = self._from_radians(self.env.get_positions(POSITION_URDF_JOINTS))
        base = self.env.get_velocities(BASE_URDF_JOINTS)
        base_out = [float(base[0]), float(base[1]), float(np.rad2deg(base[2]))]

        observation = {key: float(value) for key, value in zip(POSITION_KEYS, positions)}
        observation.update({key: value for key, value in zip(BASE_KEYS, base_out)})
        observation.update(self.env.render())
        return observation

    def send_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        position_targets = self._to_radians([action[key] for key in POSITION_KEYS])
        base_velocity = [action["x.vel"], action["y.vel"], float(np.deg2rad(action["theta.vel"]))]
        self.env.control_positions(POSITION_URDF_JOINTS, position_targets)
        self.env.control_velocities(BASE_URDF_JOINTS, base_velocity)
        self.env.step()
        return action

    def disconnect(self) -> None:
        self._connected = False

    def _to_radians(self, values: Any) -> np.ndarray:
        return np.deg2rad(values) if self.state_units == "degrees" else np.asarray(values)

    def _from_radians(self, values_rad: Any) -> np.ndarray:
        return np.rad2deg(values_rad) if self.state_units == "degrees" else np.asarray(values_rad)
