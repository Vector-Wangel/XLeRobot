from typing import Any, List

import numpy as np

from components.control.base_control import BaseController


class PDController(BaseController):
    """Per-group PD gains and the ManiSkill rest keyframe for XLeRobot."""

    # PD gains from the ManiSkill agent: (stiffness -> kp, damping -> kv, force -> +/- range).
    ARM_KP, ARM_KV, ARM_FORCE = 2e4, 1e2, 250.0
    GRIPPER_KP, GRIPPER_KV, GRIPPER_FORCE = 50.0, 1e2, 2.8
    HEAD_KP, HEAD_KV, HEAD_FORCE = 1e4, 1e2, 200.0
    BASE_KP, BASE_KV, BASE_FORCE = 1e4, 1e2, 200.0

    # Rest keyframe (radians) decoded from the ManiSkill `rest` Keyframe qpos.
    REST_POSE = {
        "Rotation": 0.0, "Pitch": 3.14, "Elbow": 3.14, "Wrist_Pitch": 0.0, "Wrist_Roll": 1.57,
        "Rotation_2": 0.0, "Pitch_2": 3.14, "Elbow_2": 3.14, "Wrist_Pitch_2": 0.0, "Wrist_Roll_2": 1.57,
        "Jaw": 0.0, "Jaw_2": 0.0,
        "head_pan_joint": 0.0, "head_tilt_joint": 0.0,
    }

    def apply(self, robot: Any) -> None:
        entity = robot.entity
        arm_joints = robot.RIGHT_ARM_JOINTS + robot.LEFT_ARM_JOINTS
        self._set_group(entity, robot.dof_indices(arm_joints), self.ARM_KP, self.ARM_KV, self.ARM_FORCE)
        self._set_group(entity, robot.dof_indices(robot.GRIPPER_JOINTS), self.GRIPPER_KP, self.GRIPPER_KV, self.GRIPPER_FORCE)
        self._set_group(entity, robot.dof_indices(robot.HEAD_JOINTS), self.HEAD_KP, self.HEAD_KV, self.HEAD_FORCE)
        self._set_group(entity, robot.dof_indices(robot.BASE_JOINTS), self.BASE_KP, self.BASE_KV, self.BASE_FORCE)

    @staticmethod
    def _set_group(entity: Any, idx: List[int], kp: float, kv: float, force: float) -> None:
        count = len(idx)
        entity.set_dofs_kp(np.full(count, kp), idx)
        entity.set_dofs_kv(np.full(count, kv), idx)
        entity.set_dofs_force_range(np.full(count, -force), np.full(count, force), idx)
