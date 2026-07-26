from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Union

import genesis as gs
import numpy as np


class BaseRobot:
    """A robot loaded from URDF into a Genesis scene."""

    # Subclasses set these class attributes.
    LINKS_TO_KEEP: Tuple[str, ...] = ()
    CAMERA_MOUNTS: Dict[str, str] = {}
    CAMERA_OFFSETS: Dict[str, np.ndarray] = {}

    def __init__(self, urdf_path: Union[str, Path]):
        self.urdf_path = Path(urdf_path)
        self.entity: Any = None

    def add_to_scene(self, scene: Any) -> Any:
        """Add the robot URDF to the scene.

        Args:
            scene (Any): Genesis scene.

        Returns:
            Any: The robot entity.
        """
        # fixed=True welds `root` to the world so the virtual base joints act as a planar base.
        self.entity = scene.add_entity(
            gs.morphs.URDF(
                file=str(self.urdf_path),
                fixed=True,
                merge_fixed_links=True,
                links_to_keep=self.LINKS_TO_KEEP,
            ),
        )
        return self.entity

    def dof_indices(self, joint_names: Sequence[str]) -> List[int]:
        """Resolve local DOF indices for the given joints, in order.

        Args:
            joint_names (Sequence[str]): Joint names.

        Returns:
            List[int]: Local DOF indices.
        """
        return [self.entity.get_joint(name).dofs_idx_local[0] for name in joint_names]

    def link(self, name: str) -> Any:
        """Return a rigid link by name.

        Args:
            name (str): Link name.

        Returns:
            Any: The rigid link.
        """
        return self.entity.get_link(name)

    def camera_mount(self, view: str) -> Tuple[str, np.ndarray]:
        """Mount link name and 4x4 offset for a camera view.

        Args:
            view (str): Camera view name.

        Returns:
            Tuple[str, np.ndarray]: Link name and offset matrix.
        """
        return self.CAMERA_MOUNTS[view], self.CAMERA_OFFSETS[view]
