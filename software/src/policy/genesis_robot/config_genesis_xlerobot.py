from dataclasses import dataclass, field
from typing import Dict

from lerobot.robots.config import RobotConfig


@RobotConfig.register_subclass("genesis_xlerobot")
@dataclass
class GenesisXLeRobotConfig(RobotConfig):
    """Config for the Genesis-simulated XLeRobot."""

    # sim_config: components spec (scene/robot/cameras/control) for XLeRobotEnvironment.
    # state_units: 'degrees' or 'radians' for the arm/head `.pos` values.
    sim_config: Dict = field(default_factory=dict)
    state_units: str = "degrees"
