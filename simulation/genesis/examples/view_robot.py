"""Load XLeRobot in Genesis and open the viewer, holding the rest pose.

Run (needs a display):
    DISPLAY=:1 python simulation/genesis/examples/view_robot.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from components.scene.base_scene import step_until_viewer_closed
from environments.test_environment import DEFAULT_SIM_CONFIG, XLeRobotEnvironment


def main():
    config = {**DEFAULT_SIM_CONFIG, "scene": {**DEFAULT_SIM_CONFIG["scene"], "show_viewer": True}}
    env = XLeRobotEnvironment.from_config(config).build()
    rest = env.controller.rest_position(env.position_joints)

    def hold():
        env.control_positions(env.position_joints, rest)
        env.control_velocities(env.base_joints, np.zeros(len(env.base_joints)))

    step_until_viewer_closed(env.scene, on_step=hold)


if __name__ == "__main__":
    main()
