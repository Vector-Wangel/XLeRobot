"""Run a trained LeRobot policy on XLeRobot — sim or real, chosen by config.

Builds a lerobot ``Robot`` from the run config (``genesis_xlerobot`` in sim, or a
real type via lerobot's factory), loads the policy, and runs the closed-loop
``get_observation -> policy -> send_action`` loop. The policy<->robot mapping
(which robot joints/cameras the policy uses) comes from the config, so a single-arm
policy drives the 17-DOF robot with the arms/head/base it doesn't control held.

    python software/src/policy/run_policy.py software/src/policy/configs/policy_act_pick_place.yaml
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

_SRC = Path(__file__).resolve().parents[1]  # software/src
sys.path.insert(0, str(_SRC))

import cv2
import numpy as np
import torch

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("run_policy")

from lerobot.configs.policies import PreTrainedConfig
from lerobot.policies.factory import get_policy_class

from policy.config_loader import load_run_config
from policy.genesis_robot.config_genesis_xlerobot import GenesisXLeRobotConfig
from policy.genesis_robot.genesis_xlerobot import GenesisXLeRobot


def build_robot(robot_config: Dict, show_viewer: bool = False) -> Any:
    params = {key: value for key, value in robot_config.items() if key != "type"}
    if robot_config["type"] == "genesis_xlerobot":
        if show_viewer:
            params.setdefault("sim_config", {}).setdefault("scene", {})["show_viewer"] = True
        return GenesisXLeRobot(GenesisXLeRobotConfig(**params))

    # Real robot: build via lerobot's registry + factory. Importing lerobot.robots
    # registers the built-in robot types; a custom bimanual xlerobot package must be
    # imported here too so its type resolves.
    import draccus

    import lerobot.robots  # noqa: F401  (registers built-in robot choice classes)
    from lerobot.robots.config import RobotConfig
    from lerobot.robots.utils import make_robot_from_config

    try:
        config = draccus.decode(RobotConfig, robot_config)
    except Exception as error:
        raise RuntimeError(
            f"Robot type '{robot_config['type']}' is not registered. Import its robot "
            f"package before running so its config subclass registers."
        ) from error
    return make_robot_from_config(config)


def load_policy(policy_config: Dict) -> Tuple[Any, str]:
    device = policy_config.get("device", "cuda")
    if device == "cuda" and not torch.cuda.is_available():
        logger.warning("CUDA not available; falling back to CPU")
        device = "cpu"
    pretrained = PreTrainedConfig.from_pretrained(policy_config["path"])
    policy = get_policy_class(pretrained.type).from_pretrained(policy_config["path"])
    policy.to(device)
    policy.eval()
    policy.reset()
    return policy, device


def build_policy_batch(observation: Dict, mapping: Dict, device: str) -> Dict[str, Any]:
    state = np.array([observation[key] for key in mapping["state_keys"]], dtype=np.float32)
    batch = {"observation.state": torch.from_numpy(state).unsqueeze(0).to(device)}
    height, width = mapping["image_hw"]
    for policy_key, robot_key in mapping["cameras"].items():
        frame = cv2.resize(observation[robot_key], (width, height))
        chw = np.transpose(frame, (2, 0, 1)).astype(np.float32) / 255.0
        batch[f"observation.images.{policy_key}"] = torch.from_numpy(chw).unsqueeze(0).to(device)
    return batch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="path to a policy run config YAML")
    parser.add_argument("--viewer", action="store_true", help="show the sim viewer")
    parser.add_argument("--steps", type=int, default=None, help="override duration_steps")
    args = parser.parse_args()

    config = load_run_config(args.config)
    mapping = config["mapping"]
    steps = args.steps if args.steps is not None else config.get("duration_steps", 400)

    robot = build_robot(config["robot"], show_viewer=args.viewer)
    policy, device = load_policy(config["policy"])
    robot.connect()

    observation = robot.get_observation()
    for step in range(steps):
        batch = build_policy_batch(observation, mapping, device)
        with torch.no_grad():
            action_values = policy.select_action(batch).squeeze(0).cpu().numpy()

        robot_action = {key: observation[key] for key in robot.action_features}
        for key, value in zip(mapping["action_keys"], action_values):
            robot_action[key] = float(value)
        robot.send_action(robot_action)
        observation = robot.get_observation()

        if step % 25 == 0:
            logger.info("step %4d  action=%s", step, np.array2string(action_values, precision=1))

    robot.disconnect()
    logger.info("rollout complete: %d steps, no shape/unit errors", steps)


if __name__ == "__main__":
    main()
