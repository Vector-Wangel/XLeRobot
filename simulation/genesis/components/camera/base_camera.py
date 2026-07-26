from typing import Any, Optional, Tuple

import numpy as np


def to_numpy(array: Any) -> np.ndarray:
    return array.cpu().numpy() if hasattr(array, "cpu") else np.asarray(array)


class BaseCamera:
    """A Genesis camera attached to a robot link."""

    # `res` is (width, height), matching Genesis' convention.
    use_depth: bool = False

    def __init__(self, res: Tuple[int, int] = (640, 480), fov: float = 60.0, mount: Optional[str] = None):
        self.res = tuple(res)
        self.fov = fov
        self.mount = mount
        self.camera: Any = None

    def add_to_scene(self, scene: Any, link: Any, offset_T: np.ndarray) -> Any:
        """Create the Genesis camera and attach it to a link.

        Args:
            scene (Any): Genesis scene.
            link (Any): Genesis rigid link to attach to.
            offset_T (np.ndarray): 4x4 camera-to-link offset.

        Returns:
            Any: The Genesis camera.
        """
        self.camera = scene.add_camera(res=self.res, fov=self.fov, GUI=False)
        self.camera.attach(link, offset_T)
        return self.camera

    def render(self) -> np.ndarray:
        """Render the camera view.

        Returns:
            np.ndarray: (H, W, 3) uint8 RGB frame.
        """
        self.camera.move_to_attach()
        rgb = self.camera.render(rgb=True, depth=self.use_depth)[0]
        return to_numpy(rgb)
