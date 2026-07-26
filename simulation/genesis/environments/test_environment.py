"""Composes the sim components (scene + robot + cameras + control) into a ready
XLeRobot environment, driven by a sim config dict.

The environment is a thin physics wrapper (positions in radians, base velocities,
rendered frames). LeRobot-facing naming/units live in the GenesisXLeRobot adapter
under software/src/policy/.

Run as a smoke test (regression of the load/control/camera phases):
    python simulation/genesis/environments/test_environment.py --headless
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # simulation/genesis on path

from typing import Any, Dict, List, Sequence

import numpy as np

from components.camera.factory import make_camera
from components.control.factory import make_controller
from components.robot.factory import make_robot
from components.scene.factory import make_scene
from components.scene.base_scene import step_until_viewer_closed

DEFAULT_SIM_CONFIG = {
    "scene": {"name": "plane", "dt": 0.01, "show_viewer": False},
    "robot": {"name": "xlerobot"},
    "cameras": {
        "head": {"type": "realsense", "mount": "head", "res": (640, 480), "fov": 60.0},
        "right_wrist": {"type": "opencv", "mount": "right_wrist", "res": (640, 480), "fov": 60.0},
        "left_wrist": {"type": "opencv", "mount": "left_wrist", "res": (640, 480), "fov": 60.0},
    },
    "control": {"name": "pd"},
}


def _to_numpy(array):
    return array.cpu().numpy() if hasattr(array, "cpu") else np.asarray(array)


class XLeRobotEnvironment:
    """A composed Genesis scene: robot on a plane with mounted cameras and PD control."""

    def __init__(self, scene_component: Any, robot: Any, cameras: Dict[str, Any], controller: Any):
        self.scene_component = scene_component
        self.robot = robot
        self.cameras = cameras
        self.controller = controller
        self.scene = None
        self._dof_cache = {}
        # Position-controlled joints (arms + grippers + head) vs velocity-controlled base.
        self.position_joints = (
            robot.RIGHT_ARM_JOINTS + robot.LEFT_ARM_JOINTS + robot.GRIPPER_JOINTS + robot.HEAD_JOINTS
        )
        self.base_joints = robot.BASE_JOINTS

    @classmethod
    def from_config(cls, config: Dict) -> "XLeRobotEnvironment":
        scene_component = make_scene(config["scene"])
        robot = make_robot(config["robot"])
        cameras = {key: make_camera(cam) for key, cam in config["cameras"].items()}
        controller = make_controller(config["control"])
        return cls(scene_component, robot, cameras, controller)

    def build(self) -> "XLeRobotEnvironment":
        scene = self.scene_component.create()
        self.robot.add_to_scene(scene)
        for camera in self.cameras.values():
            link_name, offset = self.robot.camera_mount(camera.mount)
            camera.add_to_scene(scene, self.robot.link(link_name), offset)
        scene.build()
        self.scene = scene
        self.controller.apply(self.robot)
        self.reset()
        return self

    def _dofs(self, joint_names: Sequence[str]) -> List[int]:
        key = tuple(joint_names)
        if key not in self._dof_cache:
            self._dof_cache[key] = self.robot.dof_indices(joint_names)
        return self._dof_cache[key]

    def reset(self) -> None:
        rest = self.controller.rest_position(self.position_joints)
        self.robot.entity.set_dofs_position(rest, self._dofs(self.position_joints), zero_velocity=True)

    def get_positions(self, joint_names: Sequence[str]) -> np.ndarray:
        return _to_numpy(self.robot.entity.get_dofs_position(self._dofs(joint_names))).reshape(-1)

    def get_velocities(self, joint_names: Sequence[str]) -> np.ndarray:
        return _to_numpy(self.robot.entity.get_dofs_velocity(self._dofs(joint_names))).reshape(-1)

    def control_positions(self, joint_names: Sequence[str], targets: np.ndarray) -> None:
        self.robot.entity.control_dofs_position(np.asarray(targets), self._dofs(joint_names))

    def control_velocities(self, joint_names: Sequence[str], velocities: np.ndarray) -> None:
        self.robot.entity.control_dofs_velocity(np.asarray(velocities), self._dofs(joint_names))

    def render(self) -> Dict[str, np.ndarray]:
        return {key: camera.render() for key, camera in self.cameras.items()}

    def step(self) -> None:
        self.scene.step()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--steps", type=int, default=200)
    args = parser.parse_args()

    config = {**DEFAULT_SIM_CONFIG, "scene": {**DEFAULT_SIM_CONFIG["scene"], "show_viewer": not args.headless}}
    env = XLeRobotEnvironment.from_config(config).build()

    print(f"n_dofs = {env.robot.entity.n_dofs} (expected 17)")
    rest = env.controller.rest_position(env.position_joints)
    for _ in range(args.steps):
        env.control_positions(env.position_joints, rest)
        env.control_velocities(env.base_joints, np.zeros(len(env.base_joints)))
        env.step()

    frames = env.render()
    for key, frame in frames.items():
        print(f"  camera {key}: shape={frame.shape} dtype={frame.dtype}")

    if not args.headless:
        def hold():
            env.control_positions(env.position_joints, rest)
            env.control_velocities(env.base_joints, np.zeros(len(env.base_joints)))
        step_until_viewer_closed(env.scene, on_step=hold)


if __name__ == "__main__":
    main()
