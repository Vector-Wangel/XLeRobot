"""Check an XLeRobot plugin end to end on the simulation, without hardware.

usage: python simulation/sil/check_plugin.py [--robot xlerobot|xlerobot_2wheels|xlerobot_mecanum]

The plugin connects to `VirtualServoBus`es instead of serial ports. The checks read the virtual
servos' registers and the simulated robot, not only what the plugin reports:

1. connect: handshake, calibration restored to the servos, operating modes, torque, PID values;
2. observation: the plugin reads the simulated joints in degrees;
3. arms and head: position goals reach the simulated joints;
4. base (omniwheel robot only): body velocities move the simulated base, and are read back;
5. grasp (omniwheel robot only): a scripted pick-up through the plugin lifts the cube;
6. disconnect: torque off.
"""

import argparse
import builtins
import importlib.util
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import virtual_bus  # noqa: E402

FPS = 30
results: list[tuple[bool, str]] = []


def check(ok: bool, what: str) -> None:
    results.append((bool(ok), what))
    print(f"[{'PASS' if ok else 'FAIL'}] {what}")


def run(robot, steps: int, action: dict) -> None:
    """Send `action` at 30 fps for `steps` periods, letting the simulation follow the wall clock."""
    for _ in range(steps):
        start = time.perf_counter()
        robot.send_action(action)
        time.sleep(max(0.0, 1 / FPS - (time.perf_counter() - start)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", default="xlerobot", choices=["xlerobot", "xlerobot_2wheels", "xlerobot_mecanum"])
    args = parser.parse_args()

    import lerobot
    from lerobot.robots.config import RobotConfig
    from lerobot.robots.utils import make_robot_from_config
    from lerobot.utils.import_utils import register_third_party_plugins

    register_third_party_plugins()
    virtual_bus.install()
    env = virtual_bus.load_env()
    print(f"lerobot {lerobot.__version__}, robot {args.robot}")

    calib_dir = Path(tempfile.mkdtemp(prefix="xlerobot_sil_"))
    cfg_cls = RobotConfig.get_choice_class(args.robot)
    cfg = cfg_cls(id="sil", calibration_dir=calib_dir, use_degrees=True, cameras={})
    robot = make_robot_from_config(cfg)
    motors = {name: m.id for bus in (robot.bus1, robot.bus2) for name, m in bus.motors.items()}
    virtual_bus.write_calibration_file(calib_dir / "sil.json", motors)
    robot._load_calibration()

    # The plugin asks whether to restore the calibration file on connect: answer ENTER.
    real_input = builtins.input
    builtins.input = lambda prompt="": print(f"{prompt}[sil: ENTER]") or ""
    try:
        robot.connect()
    finally:
        builtins.input = real_input
    buses = {bus.port: bus for bus in virtual_bus.BUSES}
    world = virtual_bus.sim().world

    # 1. connect
    regs = {bus.names[i]: r for bus in buses.values() for i, r in bus.registers.items()}
    joints = [m for m in regs if m in env.JOINT_MAP or m in env.GRIPPER_MAP]
    wheels = [m for m in regs if m not in joints]
    check(all(regs[m]["operating_mode"] == 0 for m in joints), f"{len(joints)} arm/head servos in position mode (0)")
    check(wheels and all(regs[m]["operating_mode"] == 1 for m in wheels), f"{len(wheels)} wheel servos in velocity mode (1)")
    check(all(regs[m]["torque_enable"] == 1 for m in regs), "torque enabled on every servo")
    arm_motors = [m for m in joints if "_arm_" in m]
    check(all((regs[m]["p_coefficient"], regs[m]["i_coefficient"], regs[m]["d_coefficient"]) == (16, 0, 43) for m in arm_motors),
          "arm PID registers set to P=16 I=0 D=43")
    check(all(regs[m]["max_position_limit"] == robot.calibration[m].range_max for m in joints),
          "calibration restored to the servos (position limits)")
    check(robot.is_calibrated, "bus reports the servos calibrated")

    # 2. observation
    obs = robot.get_observation()
    errors = [abs(obs[f"{m}.pos"] - world.position(m)) for m in env.MOTORS if f"{m}.pos" in obs]
    check(max(errors) < 0.2, f"observation matches the simulated joints (max error {max(errors):.3f} deg)")

    # 3. arms and head: move every joint, then compare the simulation with the goals.
    target = {f"{m}.pos": obs[f"{m}.pos"] for m in env.MOTORS if f"{m}.pos" in obs}
    for side in ("left", "right"):
        target[f"{side}_arm_shoulder_pan.pos"] += 15 if side == "left" else -15
        target[f"{side}_arm_shoulder_lift.pos"] -= 20
        target[f"{side}_arm_elbow_flex.pos"] += 25
        target[f"{side}_arm_wrist_roll.pos"] += 30
        target[f"{side}_arm_gripper.pos"] = 90.0
    target["head_motor_1.pos"] += 20
    base = {k: 0.0 for k in robot.action_features if not k.endswith(".pos")}
    run(robot, 60, {**target, **base})
    sim_err = {k: abs(world.position(k[:-4]) - v) for k, v in target.items()}
    worst = max(sim_err, key=sim_err.get)
    check(sim_err[worst] < 3.0, f"{len(target)} position goals reached in simulation (worst {worst} off by {sim_err[worst]:.2f})")
    if sim_err[worst] >= 3.0:
        print("   goals vs simulation:", {k: (round(v, 1), round(world.position(k[:-4]), 1)) for k, v in target.items()})

    if args.robot == "xlerobot":
        # 4. base: back away from the table, then turn, through the plugin's wheel kinematics.
        world_base = world.data.qpos[world.base_joints].copy()
        run(robot, 60, {**target, "x.vel": -0.15, "y.vel": 0.0, "theta.vel": 0.0})
        obs = robot.get_observation()
        moved = world.data.qpos[world.base_joints] - world_base
        backward = -float(moved[0])  # slide x is the robot's forward axis while it has not turned
        check(0.22 < backward < 0.34, f"x.vel=-0.15 m/s for 2 s moves the base {backward:.3f} m back (expect about 0.3)")
        check(abs(obs["x.vel"] + 0.15) < 0.02, f"plugin reads x.vel={obs['x.vel']:.3f} back from the wheels")
        yaw0 = float(world.data.qpos[world.base_joints[2]])
        run(robot, 60, {**target, "x.vel": 0.0, "y.vel": 0.0, "theta.vel": 30.0})
        turned = np.degrees(float(world.data.qpos[world.base_joints[2]]) - yaw0)
        check(45 < turned < 70, f"theta.vel=30 deg/s for 2 s turns the base {turned:.1f} deg (expect about 60)")
        run(robot, 20, {**target, "x.vel": 0.0, "y.vel": 0.0, "theta.vel": 0.0})

        # 5. grasp: reset the world, then pick the cube up with the right arm through the plugin.
        kin_spec = importlib.util.spec_from_file_location("so101_kin", HERE.parents[1] / "software/src/model/SO101Robot.py")
        kin_module = importlib.util.module_from_spec(kin_spec)
        kin_spec.loader.exec_module(kin_module)
        kin = kin_module.SO101Kinematics()
        world.reset(np.random.default_rng(0), 0.0, 0.0)
        obs = robot.get_observation()
        hold = {f"{m}.pos": obs[f"{m}.pos"] for m in env.MOTORS}

        def arm(x, y, grip):
            j2, j3 = kin.inverse_kinematics(x, y)
            return {"right_arm_shoulder_pan.pos": 0.0, "right_arm_shoulder_lift.pos": j2, "right_arm_elbow_flex.pos": j3,
                    "right_arm_wrist_flex.pos": -j2 - j3 + 90, "right_arm_wrist_roll.pos": 0.0, "right_arm_gripper.pos": grip}

        current = {k: hold[k] for k in arm(0.17, 0.0, 100)}
        for goal, secs in ((arm(0.17, -0.02, 100), 1.5), (arm(0.17, -0.09, 100), 1.0),
                           (arm(0.17, -0.09, 0), 0.8), (arm(0.17, 0.03, 0), 1.5)):
            n = int(secs * FPS)
            for i in range(1, n + 1):
                step = {k: current[k] + (goal[k] - current[k]) * i / n for k in goal}
                run(robot, 1, {**hold, **step, **base})
            current = goal
        lift = world.cube_lift()
        check(lift > 0.05, f"scripted grasp through the plugin lifts the cube {lift * 100:.1f} cm")

    # 6. disconnect
    robot.disconnect()
    check(all(r["torque_enable"] == 0 for bus in buses.values() for r in bus.registers.values()), "torque disabled on disconnect")

    failed = [what for ok, what in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
