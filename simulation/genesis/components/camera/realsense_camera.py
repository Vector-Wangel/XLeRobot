from typing import Optional, Tuple

from components.camera.base_camera import BaseCamera


class RealSenseCamera(BaseCamera):
    """Sim camera emulating an Intel RealSense (RGB, depth-capable)."""

    use_depth = True

    def __init__(self, res: Tuple[int, int] = (1280, 720), fov: float = 55.0, mount: Optional[str] = None):
        super().__init__(res=res, fov=fov, mount=mount)
