from typing import Dict

from components.scene.base_scene import BaseScene
from components.scene.plane_scene import PlaneScene

_SCENES = {
    "plane": PlaneScene,
}


def make_scene(config: Dict) -> BaseScene:
    """Build a scene component from a config dict, dispatching on ``config['name']``.

    Args:
        config (dict): Scene config with a ``name`` key.

    Returns:
        BaseScene: The scene component.
    """
    params = dict(config)
    name = params.pop("name")
    if name not in _SCENES:
        raise ValueError(f"Unknown scene '{name}'. Available: {sorted(_SCENES)}")
    return _SCENES[name](**params)
