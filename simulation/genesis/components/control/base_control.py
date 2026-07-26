from abc import ABC, abstractmethod
from typing import Any, Dict, Sequence

import numpy as np


class BaseController(ABC):
    """Base controller for a robot's joint groups."""

    REST_POSE: Dict[str, float] = {}

    @abstractmethod
    def apply(self, robot: Any) -> None:
        """Apply control gains to the robot's joint groups.

        Args:
            robot (Any): Built robot component.
        """

    def rest_position(self, joint_names: Sequence[str]) -> np.ndarray:
        """Rest-pose targets for the given joints.

        Args:
            joint_names (Sequence[str]): Joint names.

        Returns:
            np.ndarray: Target positions (radians).
        """
        return np.array([self.REST_POSE[name] for name in joint_names])
