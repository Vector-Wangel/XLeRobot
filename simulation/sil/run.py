"""Run a LeRobot command line tool with the XLeRobot plugins on the simulation.

usage: python simulation/sil/run.py [--sil.height H --sil.width W --sil.seed N] <lerobot-command> [args...]

For example, roll a policy out through the real `xlerobot` plugin, with the simulation's cameras:

    python simulation/sil/run.py --sil.height 240 --sil.width 320 lerobot-rollout \\
      --strategy.type=base --policy.path=<checkpoint> \\
      --robot.type=xlerobot --robot.use_degrees=true --robot.id=sil \\
      --robot.cameras="{head: {type: xlerobot_sim, name: head, width: 320, height: 240, fps: 30}}" \\
      --task="Pick up the red cube from the table." --duration=10

The plugin's serial buses become `VirtualServoBus`es and cameras of type `xlerobot_sim` render the
simulation. Unless `--robot.calibration_dir` is given, a calibration matching the virtual encoders is
written to a temporary directory. The plugin's prompt to restore it is answered with ENTER. The
world starts with the environment's reset noise, drawn with `--sil.seed`. At exit the script prints
the highest the cube was lifted.
"""

import atexit
import builtins
import sys
import tempfile
from importlib.metadata import entry_points
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import virtual_bus  # noqa: E402


def main() -> None:
    args = sys.argv[1:]
    options = {"height": 480, "width": 640, "seed": 0}
    while args and args[0].startswith("--sil."):
        key, _, value = args.pop(0)[len("--sil."):].partition("=")
        options[key] = int(value or args.pop(0))
    if not args:
        sys.exit(__doc__)
    command, cli_args = args[0], args[1:]
    scripts = {ep.name: ep for ep in entry_points(group="console_scripts")}
    if command not in scripts:
        sys.exit(f"Unknown command {command!r}: install LeRobot, which provides it")

    virtual_bus.install()
    sim = virtual_bus.sim(options["height"], options["width"], options["seed"], randomize=True)
    if not any(a.startswith("--robot.calibration_dir") for a in cli_args):
        robot_id = next((a.split("=", 1)[1] for a in cli_args if a.startswith("--robot.id=")), None)
        calib_dir = Path(tempfile.mkdtemp(prefix="xlerobot_sil_"))
        virtual_bus.write_calibration_file(calib_dir / f"{robot_id}.json")
        cli_args.append(f"--robot.calibration_dir={calib_dir}")
    real_input = builtins.input

    def answer(prompt: str = "") -> str:
        if "calibration" in prompt:  # the plugin's "restore calibration from file?" prompt
            print(f"{prompt}[sil: ENTER]")
            return ""
        return real_input(prompt)

    builtins.input = answer
    # The highest lift: rollouts return the arm to its start pose, dropping the cube, before exiting.
    atexit.register(lambda: print(f"[sil] cube lifted at most {sim.max_lift * 100:.1f} cm"))

    sys.argv = [command, *cli_args]
    sys.exit(scripts[command].load()())


if __name__ == "__main__":
    main()
