from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Tuple

import genesis as gs


class BaseScene(ABC):
    """A Genesis scene with a viewer and fixed timestep."""

    def __init__(
        self,
        dt: float = 0.01,
        show_viewer: bool = True,
        camera_pos: Tuple[float, float, float] = (0.0, -2.5, 1.8),
        camera_lookat: Tuple[float, float, float] = (0.0, 0.0, 0.5),
        camera_fov: float = 40,
    ):
        self.dt = dt
        self.show_viewer = show_viewer
        self.camera_pos = camera_pos
        self.camera_lookat = camera_lookat
        self.camera_fov = camera_fov
        self.scene: Any = None

    def create(self) -> Any:
        """Create the scene and its world entities.

        Returns:
            Any: The unbuilt Genesis scene.
        """
        if not gs._initialized:  # gs.init may only be called once per process
            gs.init(backend=gs.gpu)
        self.scene = gs.Scene(
            viewer_options=gs.options.ViewerOptions(
                camera_pos=self.camera_pos,
                camera_lookat=self.camera_lookat,
                camera_fov=self.camera_fov,
            ),
            sim_options=gs.options.SimOptions(dt=self.dt),
            show_viewer=self.show_viewer,
        )
        self.add_world(self.scene)
        return self.scene

    @abstractmethod
    def add_world(self, scene: Any) -> None:
        """Add the world entities (ground, props) to the scene.

        Args:
            scene (Any): Genesis scene.
        """


def step_until_viewer_closed(scene: Any, on_step: Optional[Callable[[], None]] = None) -> None:
    """Step the scene until the viewer window closes.

    Args:
        scene (Any): Built Genesis scene.
        on_step (Optional[Callable[[], None]]): Called before each step. Defaults to None.
    """
    try:
        while scene.viewer.is_alive():
            if on_step is not None:
                on_step()
            scene.step()
    except gs.GenesisException:
        # The window can close between the liveness check and the step.
        pass
