from typing import Optional, Tuple

from components.camera.base_camera import BaseCamera


class OpenCVCamera(BaseCamera):
    """Sim camera emulating a USB/OpenCV webcam (RGB only)."""

    use_depth = False

    def __init__(self, res: Tuple[int, int] = (640, 480), fov: float = 60.0, mount: Optional[str] = None):
        super().__init__(res=res, fov=fov, mount=mount)
