from typing import Dict

from components.camera.base_camera import BaseCamera
from components.camera.opencv_camera import OpenCVCamera
from components.camera.realsense_camera import RealSenseCamera

_CAMERAS = {
    "opencv": OpenCVCamera,
    "realsense": RealSenseCamera,
}


def make_camera(config: Dict) -> BaseCamera:
    """Build a camera component from a config dict, dispatching on ``config['type']``.

    Args:
        config (dict): Camera config with ``type``, ``res``, ``fov``, ``mount``.

    Returns:
        BaseCamera: The camera component.
    """
    params = dict(config)
    camera_type = params.pop("type")
    if camera_type not in _CAMERAS:
        raise ValueError(f"Unknown camera '{camera_type}'. Available: {sorted(_CAMERAS)}")
    return _CAMERAS[camera_type](**params)
