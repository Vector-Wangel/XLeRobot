from pathlib import Path
from typing import Union

import numpy as np

from components.robot.base_robot import BaseRobot

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets" / "xlerobot"
DEFAULT_URDF_PATH = ASSETS_DIR / "xlerobot.urdf"


class XLeRobot(BaseRobot):
    """The bimanual XLeRobot loaded from URDF into a Genesis scene."""

    # Actuated joints: 3 planar-base + 5 right arm + 5 left arm + 2 grippers + 2 head = 17 DOF.
    BASE_JOINTS = ("root_x_axis_joint", "root_y_axis_joint", "root_z_rotation_joint")
    RIGHT_ARM_JOINTS = ("Rotation", "Pitch", "Elbow", "Wrist_Pitch", "Wrist_Roll")
    LEFT_ARM_JOINTS = ("Rotation_2", "Pitch_2", "Elbow_2", "Wrist_Pitch_2", "Wrist_Roll_2")
    GRIPPER_JOINTS = ("Jaw", "Jaw_2")
    HEAD_JOINTS = ("head_pan_joint", "head_tilt_joint")
    ACTUATED_JOINTS = BASE_JOINTS + RIGHT_ARM_JOINTS + LEFT_ARM_JOINTS + GRIPPER_JOINTS + HEAD_JOINTS

    # Fixed links preserved through fixed-link merging: camera mounts + gripper tips.
    CAMERA_LINKS = ("head_camera_link", "Right_Arm_Camera", "Left_Arm_Camera")
    GRIPPER_TIP_LINKS = ("Fixed_Jaw_tip", "Moving_Jaw_tip", "Fixed_Jaw_tip_2", "Moving_Jaw_tip_2")
    LINKS_TO_KEEP = CAMERA_LINKS + GRIPPER_TIP_LINKS

    # View name -> mount link.
    CAMERA_MOUNTS = {
        "head": "head_camera_link",
        "right_wrist": "Right_Arm_Camera",
        "left_wrist": "Left_Arm_Camera",
    }

    # View name -> 4x4 camera-to-link mount offset. Genesis cameras look down local
    # -Z; these rotations aim each view forward + down at the workspace at the rest
    # pose and rotate with the link thereafter.
    CAMERA_OFFSETS = {
        "head": np.array([
            [0.0000, 0.5735, -0.8192, 0.0],
            [-1.0000, 0.0000, 0.0000, 0.0],
            [0.0000, 0.8192, 0.5735, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]),
        "right_wrist": np.array([
            [0.0000, 0.4472, -0.8944, 0.0],
            [0.0000, 0.8944, 0.4472, 0.0],
            [1.0000, 0.0000, 0.0000, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]),
        "left_wrist": np.array([
            [0.0000, 0.4472, -0.8944, 0.0],
            [0.0000, 0.8944, 0.4472, 0.0],
            [1.0000, 0.0000, 0.0000, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]),
    }

    def __init__(self, urdf_path: Union[str, Path] = DEFAULT_URDF_PATH):
        super().__init__(urdf_path)
