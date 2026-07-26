from typing import Dict

from components.control.base_control import BaseController
from components.control.pd_control_xlerobot import PDController

_CONTROLLERS = {
    "pd": PDController,
}


def make_controller(config: Dict) -> BaseController:
    """Build a controller component from a config dict, dispatching on ``config['name']``.

    Args:
        config (dict): Controller config with a ``name`` key.

    Returns:
        BaseController: The controller component.
    """
    params = dict(config)
    name = params.pop("name")
    if name not in _CONTROLLERS:
        raise ValueError(f"Unknown controller '{name}'. Available: {sorted(_CONTROLLERS)}")
    return _CONTROLLERS[name](**params)
