from pathlib import Path
from typing import Dict, Union

import yaml


def load_run_config(policy_config_path: Union[str, Path]) -> Dict:
    """Load a policy run config YAML and inline its referenced robot config.

    Args:
        policy_config_path (str | Path): Path to the policy run config YAML.

    Returns:
        dict: Run config with `policy`, `robot`, `task`, `duration_steps`, `mapping`.
    """
    # `robot_config` is resolved relative to the policy config file.
    policy_config_path = Path(policy_config_path)
    with open(policy_config_path) as file:
        config = yaml.safe_load(file)

    robot_ref = config.get("robot_config")
    if robot_ref is not None:
        robot_path = policy_config_path.parent / robot_ref
        with open(robot_path) as file:
            config["robot"] = yaml.safe_load(file)["robot"]
    return config
