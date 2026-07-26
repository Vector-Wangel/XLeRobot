from typing import Dict

from components.robot.base_robot import BaseRobot
from components.robot.xlerobot import XLeRobot

_ROBOTS = {
    "xlerobot": XLeRobot,
}


def make_robot(config: Dict) -> BaseRobot:
    """Build a robot component from a config dict, dispatching on ``config['name']``.

    Args:
        config (dict): Robot config with a ``name`` key.

    Returns:
        BaseRobot: The robot component.
    """
    params = dict(config)
    name = params.pop("name")
    if name not in _ROBOTS:
        raise ValueError(f"Unknown robot '{name}'. Available: {sorted(_ROBOTS)}")
    return _ROBOTS[name](**params)
