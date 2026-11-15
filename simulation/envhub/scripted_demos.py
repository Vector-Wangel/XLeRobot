"""Scripted demonstrations for the XLeRobot pick-cube environment, recorded as a LeRobot dataset.

usage (from the repository root, with LeRobot >= 0.7 and the XLeRobot plugins installed):

    python simulation/envhub/scripted_demos.py --root data/xlerobot_pick_cube --episodes 50

The demonstrator knows the cube's pose. It turns the right shoulder towards the cube, then uses the
plugin's 2-link IK (`xlerobot_model.SO101Robot.SO101Kinematics`) to approach from above, close the
gripper and lift. Only episodes where the cube ends up lifted are kept. Frames hold the
observation before each action and the action sent, named and in the units of the `xlerobot`
plugin, as `lerobot-record` writes them.
"""

import argparse
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FPS = 30
# Gripper-to-target offset of the IK point, and its height below the shoulder, in metres; found by
# searching grasps in this scene.
REACH_OFFSET = 0.055
GRASP_HEIGHT = -0.12


def load_env():
    if "xlerobot_envhub_env" in sys.modules:
        return sys.modules["xlerobot_envhub_env"]
    spec = importlib.util.spec_from_file_location("xlerobot_envhub_env", HERE / "env.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ScriptedGrasp:
    """Right-arm pick-up, as a list of actions in plugin units, planned from the world state."""

    def __init__(self, env_module, world):
        from xlerobot_model.SO101Robot import SO101Kinematics

        self.env = env_module
        self.world = world
        self.kin = SO101Kinematics()

    def _arm(self, pan: float, reach: float, height: float, grip: float) -> dict[str, float]:
        lift, elbow = self.kin.inverse_kinematics(reach, height)
        return {
            "right_arm_shoulder_pan": pan,
            "right_arm_shoulder_lift": lift,
            "right_arm_elbow_flex": elbow,
            "right_arm_wrist_flex": -lift - elbow + 90.0,  # gripper pointing down
            "right_arm_wrist_roll": 0.0,
            "right_arm_gripper": grip,
        }

    def plan(self, rng: np.random.Generator) -> list[np.ndarray]:
        data = self.world.data
        rot = data.body("chassis").xmat.reshape(3, 3)
        origin = data.body("chassis").xpos

        def robot_frame(body: str) -> np.ndarray:
            return rot.T @ (data.body(body).xpos - origin)

        # The model's "Rotation_Pitch" arm is the robot's right arm (see JOINT_MAP in env.py).
        shoulder = robot_frame("Rotation_Pitch")
        cube = robot_frame(self.env.CUBE_BODY)
        forward, left = cube[0] - shoulder[0], cube[1] - shoulder[1]
        pan = -math.degrees(math.atan2(left, forward))  # positive pan turns the arm to the right
        reach = math.hypot(forward, left) - REACH_OFFSET
        start = {m: self.world.position(m) for m in self.env.MOTORS}
        waypoints = [
            (self._arm(pan, reach, GRASP_HEIGHT + 0.10, 100.0), rng.uniform(1.3, 1.7)),
            (self._arm(pan, reach, GRASP_HEIGHT, 100.0), rng.uniform(0.9, 1.2)),
            (self._arm(pan, reach, GRASP_HEIGHT, 0.0), 0.8),
            (self._arm(pan, reach, GRASP_HEIGHT + 0.14, 0.0), rng.uniform(1.3, 1.7)),
            (self._arm(pan, reach, GRASP_HEIGHT + 0.14, 0.0), 0.5),
        ]
        actions, current = [], dict(start)
        for goal, seconds in waypoints:
            steps = max(1, round(seconds * FPS))
            for i in range(1, steps + 1):
                pose = dict(current)
                pose.update({k: current[k] + (goal[k] - current[k]) * i / steps for k in goal})
                actions.append(np.array([pose[m] for m in self.env.MOTORS] + [0.0, 0.0, 0.0], dtype=np.float32))
            current.update(goal)
        return actions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, required=True, help="dataset directory (must not exist)")
    parser.add_argument("--repo_id", default="local/xlerobot_pick_cube_scripted")
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--cameras", nargs="+", default=["head", "right_wrist"])
    parser.add_argument("--height", type=int, default=240)
    parser.add_argument("--width", type=int, default=320)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--dry_run", action="store_true", help="measure the success rate without recording")
    args = parser.parse_args()

    env_module = load_env()
    env = env_module.XLeRobotEnv(observation_height=args.height, observation_width=args.width, cameras=args.cameras)
    dataset = None
    if not args.dry_run:
        from lerobot.datasets.lerobot_dataset import LeRobotDataset
        from lerobot.utils.constants import ACTION, OBS_STR
        from lerobot.utils.feature_utils import build_dataset_frame, hw_to_dataset_features

        state = dict.fromkeys(env_module.STATE_NAMES, float)
        cameras = {c: (args.height, args.width, 3) for c in args.cameras}
        features = {**hw_to_dataset_features(state, ACTION), **hw_to_dataset_features({**state, **cameras}, OBS_STR)}
        dataset = LeRobotDataset.create(args.repo_id, FPS, features, root=args.root, robot_type="xlerobot", use_videos=True)

    rng = np.random.default_rng(args.seed)
    kept, tried = 0, 0
    while kept < args.episodes:
        obs, _ = env.reset(seed=int(rng.integers(1 << 31)))
        tried += 1
        plan = ScriptedGrasp(env_module, env.world).plan(rng)
        frames, success = [], False
        for action in plan:
            frames.append((obs, action))
            obs, _, success, _, info = env.step(action)
        if not success:
            print(f"episode {tried}: cube lifted {info['cube_lift'] * 100:.1f} cm, dropped")
            continue
        kept += 1
        if dataset is not None:
            for observation, action in frames:
                values = dict(zip(env_module.STATE_NAMES, observation["agent_pos"].tolist(), strict=True))
                robot_obs = {**values, **observation["pixels"]}
                robot_action = dict(zip(env_module.STATE_NAMES, action.tolist(), strict=True))
                dataset.add_frame({
                    **build_dataset_frame(dataset.features, robot_obs, prefix=OBS_STR),
                    **build_dataset_frame(dataset.features, robot_action, prefix=ACTION),
                    "task": env.task_description,
                })
            dataset.save_episode()
        print(f"episode {tried}: kept ({kept}/{args.episodes}), {len(frames)} frames")
    if dataset is not None:
        dataset.finalize()
    env.close()
    print(f"success rate of the script: {kept}/{tried}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
