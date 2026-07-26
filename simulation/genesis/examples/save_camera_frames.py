"""Render each mounted camera at the rest pose and save a PNG per view.

Run headless (with the system-GL preload; see software/src/policy/run_policy.sh):
    python simulation/genesis/examples/save_camera_frames.py --out /tmp/xle_frames
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import imageio.v3 as iio
import numpy as np

from environments.test_environment import DEFAULT_SIM_CONFIG, XLeRobotEnvironment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="camera_frames")
    parser.add_argument("--steps", type=int, default=200)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    env = XLeRobotEnvironment.from_config(DEFAULT_SIM_CONFIG).build()
    rest = env.controller.rest_position(env.position_joints)
    for _ in range(args.steps):
        env.control_positions(env.position_joints, rest)
        env.control_velocities(env.base_joints, np.zeros(len(env.base_joints)))
        env.step()

    for key, frame in env.render().items():
        path = out_dir / f"{key}.png"
        iio.imwrite(path, frame)
        print(f"saved {key}: shape={frame.shape} -> {path}")


if __name__ == "__main__":
    main()
