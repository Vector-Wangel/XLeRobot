from typing import Any

import genesis as gs

from components.scene.base_scene import BaseScene


class PlaneScene(BaseScene):
    """A ground-plane Genesis scene."""

    def add_world(self, scene: Any) -> None:
        scene.add_entity(gs.morphs.Plane())
