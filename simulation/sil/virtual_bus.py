"""Run the XLeRobot LeRobot plugins against the MuJoCo simulation instead of serial servos.

`install()` makes every `SerialMotorsBus` (LeRobot >= 0.7) open a `VirtualServoBus` instead of a
serial port. The virtual bus keeps STS3215 registers and answers them from the EnvHub world in
`../envhub/env.py`, so the plugin's own code runs unchanged: handshake, calibration, operating
modes, PID registers, sync reads and writes. A servo honours a goal only in the matching operating
mode and with its torque on, so a plugin that configures its motors wrongly does not move.

Arm and head encoders put the calibrated middle of the range at tick 2047.5, the convention of the
calibration that `write_calibration_file()` writes. The three omniwheels follow the plugin's own
kinematics (`XLerobot._body_to_wheel_raw`). Cameras of type `xlerobot_sim` render the
simulation's cameras of the same name.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ENV_PY = Path(__file__).resolve().parents[1] / "envhub" / "env.py"
CENTER = 2047.5  # tick of the calibrated middle
TICKS_PER_DEG = 4095 / 360  # LeRobot's degree normalization: (raw - mid) * 360 / 4095
GRIPPER_RAW = (1600, 3200)  # gripper ticks for 0 (closed) and 100 (open)
# The omniwheel plugin's base geometry (XLerobot._body_to_wheel_raw).
WHEELS = ("base_left_wheel", "base_back_wheel", "base_right_wheel")
WHEEL_RADIUS, BASE_RADIUS = 0.05, 0.125
_ANGLES = np.radians(np.array([240, 0, 120]) - 90)
WHEEL_MATRIX = np.array([[np.cos(a), np.sin(a), BASE_RADIUS] for a in _ANGLES])
STEPS_PER_DEG = 4096.0 / 360.0  # XLerobot._degps_to_raw

_lock = threading.RLock()
_sim: _Sim | None = None


def load_env():
    """Import the EnvHub `env.py` as a module."""
    if "xlerobot_envhub_env" in sys.modules:
        return sys.modules["xlerobot_envhub_env"]
    spec = importlib.util.spec_from_file_location("xlerobot_envhub_env", ENV_PY)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class _Sim:
    """One world shared by both buses and the cameras, advanced to match the wall clock."""

    def __init__(self, height: int, width: int, seed: int, randomize: bool):
        self.env = load_env()
        self.world = self.env.XLeRobotWorld(30, height, width)
        # The environment's default reset noise, or none for repeatable checks.
        noise = (2.0, 0.03) if randomize else (0.0, 0.0)
        self.world.reset(np.random.default_rng(seed), *noise)
        self.last = time.perf_counter()
        self.carry = 0.0
        self.max_lift = 0.0

    def sync(self) -> None:
        now = time.perf_counter()
        elapsed = min(now - self.last, 0.1) + self.carry  # a stalled caller does not fast-forward
        self.last = now
        step = self.world.model.opt.timestep
        steps = int(elapsed / step)
        self.carry = elapsed - steps * step
        if steps:
            self.world.advance(steps * step)
            self.max_lift = max(self.max_lift, self.world.cube_lift())


def sim(height: int = 480, width: int = 640, seed: int = 0, randomize: bool = False) -> _Sim:
    """The shared simulation, created on first use; `randomize` applies the env's reset noise."""
    global _sim
    with _lock:
        if _sim is None:
            _sim = _Sim(height, width, seed, randomize)
        return _sim


def reset_sim() -> None:
    global _sim
    with _lock:
        if _sim is not None:
            _sim.world.close()
        _sim = None


def _model_number(model: str) -> int:
    import rustypot

    return int(rustypot.find_model(model)[0])


class VirtualServoBus:
    """The subset of `rustypot.Bus` that `SerialMotorsBus` uses, served by the simulation."""

    def __init__(self, port: str, motors: dict, definitions: dict):
        self.port = port
        self.names = {motor.id: name for name, motor in motors.items()}
        self.definitions = definitions
        self.registers: dict[int, dict[str, int]] = {}
        for name, motor in motors.items():
            self.registers[motor.id] = {
                "model_number": _model_number(motor.model),
                "firmware_major_version": 3,
                "firmware_minor_version": 10,
                "torque_enable": 0,
                "operating_mode": 0,
                "homing_offset": 0,
                "min_position_limit": 0,
                "max_position_limit": 4095,
            }
        self.sim = sim()
        self.env = self.sim.env
        self.writes: list[tuple[str, int, str, int]] = []  # (motor, id, register, value), for checks

    # Register file
    def _get(self, id_: int, name: str) -> int:
        regs = self.registers[id_]
        motor = self.names[id_]
        if name == "present_position" and self._is_joint(motor):
            return int(round(self._physical(motor) - regs["homing_offset"]))
        if name == "present_velocity" and motor in WHEELS:
            return self._wheel_raw(motor)
        return int(regs.get(name, 0))

    def _set(self, id_: int, name: str, value: int) -> None:
        motor = self.names[id_]
        self.registers[id_][name] = int(value)
        self.writes.append((motor, id_, name, int(value)))
        regs = self.registers[id_]
        if name == "torque_enable" and self._is_joint(motor):
            # Torque off: the joint stays where it is instead of tracking an old goal.
            self.sim.world.set_position_target(motor, self.sim.world.position(motor))
        if name == "goal_position" and self._is_joint(motor) and regs["torque_enable"] and regs["operating_mode"] == 0:
            raw = int(np.clip(value, regs["min_position_limit"], regs["max_position_limit"]))
            self.sim.world.set_position_target(motor, self._units(motor, raw + regs["homing_offset"]))
        if name in ("goal_velocity", "torque_enable", "operating_mode") and motor in WHEELS:
            self._drive_base()

    def _is_joint(self, motor: str) -> bool:
        return motor in self.env.JOINT_MAP or motor in self.env.GRIPPER_MAP

    def _physical(self, motor: str) -> float:
        value = self.sim.world.position(motor)
        if motor in self.env.GRIPPER_MAP:
            lo, hi = GRIPPER_RAW
            return lo + value / 100.0 * (hi - lo)
        return CENTER + value * TICKS_PER_DEG

    def _units(self, motor: str, physical: float) -> float:
        if motor in self.env.GRIPPER_MAP:
            lo, hi = GRIPPER_RAW
            return (physical - lo) / (hi - lo) * 100.0
        return (physical - CENTER) / TICKS_PER_DEG

    # Omniwheel base
    def _drive_base(self) -> None:
        if not all(w in self.names.values() for w in WHEELS):
            return
        ids = {name: id_ for id_, name in self.names.items()}
        degps = []
        for wheel in WHEELS:
            regs = self.registers[ids[wheel]]
            moving = regs["torque_enable"] and regs["operating_mode"] == 1
            degps.append(regs.get("goal_velocity", 0) / STEPS_PER_DEG if moving else 0.0)
        linear = np.radians(degps) * WHEEL_RADIUS
        x, y, theta_rad = np.linalg.solve(WHEEL_MATRIX, linear)
        self.sim.world.set_base_velocity(float(x), float(y), float(np.degrees(theta_rad)))

    def _wheel_raw(self, wheel: str) -> int:
        x, y, theta = self.sim.world.base_velocity()
        linear = WHEEL_MATRIX @ np.array([x, y, np.radians(theta)])
        degps = np.degrees(linear / WHEEL_RADIUS)[WHEELS.index(wheel)]
        return int(round(degps * STEPS_PER_DEG))

    # rustypot.Bus API
    def read_register_with_error(self, id_: int, name: str, retries: int = 0):
        with _lock:
            self.sim.sync()
            return self._get(id_, name), 0

    def write_register_with_error(self, id_: int, name: str, value: int, retries: int = 0) -> int:
        with _lock:
            self.sim.sync()
            self._set(id_, name, value)
            return 0

    def sync_read_register_with_error(self, ids, name: str, retries: int = 0):
        with _lock:
            self.sim.sync()
            return [(self._get(id_, name), 0) for id_ in ids]

    def sync_write_register(self, ids, name: str, values, retries: int = 0) -> None:
        with _lock:
            self.sim.sync()
            for id_, value in zip(ids, values, strict=True):
                self._set(id_, name, value)

    def set_torque(self, ids, enabled: bool, retries: int = 0) -> dict:
        with _lock:
            self.sim.sync()
            for id_ in ids:
                self._set(id_, "torque_enable", int(enabled))
            return {}

    def scan(self, definition) -> dict[int, int]:
        return {id_: regs["model_number"] for id_, regs in self.registers.items()}

    broadcast_scan = scan

    def close(self) -> None:
        pass

    def is_open(self) -> bool:
        return True


BUSES: list[VirtualServoBus] = []


def install() -> None:
    """Make every `SerialMotorsBus` open a `VirtualServoBus`, and register the sim camera."""
    from lerobot.motors.motors_bus import SerialMotorsBus

    def _open_bus(self):
        bus = VirtualServoBus(self.port, self.motors, self._definitions)
        BUSES.append(bus)
        return bus

    SerialMotorsBus._open_bus = _open_bus
    _register_camera()


def write_calibration_file(path: Path, motors: dict[str, int] | None = None) -> None:
    """Write the calibration that matches the virtual encoders, for every motor of a plugin."""
    env = load_env()
    names = list(motors) if motors else [*env.MOTORS, *WHEELS]
    calibration = {}
    for name in names:
        lo, hi = GRIPPER_RAW if name in env.GRIPPER_MAP else (0, 4095)
        calibration[name] = {"id": 0, "drive_mode": 0, "homing_offset": 0, "range_min": lo, "range_max": hi}
        if motors:
            calibration[name]["id"] = motors[name]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(calibration, indent=2))


def _register_camera() -> None:
    from lerobot.cameras.camera import Camera
    from lerobot.cameras.configs import CameraConfig

    if "xlerobot_sim" in CameraConfig.get_known_choices():
        return

    @CameraConfig.register_subclass("xlerobot_sim")
    @dataclass
    class XLeRobotSimCameraConfig(CameraConfig):
        """A camera of the simulation, by its name there: head, left_wrist or right_wrist."""

        name: str = "head"

    class XLeRobotSimCamera(Camera):
        def __init__(self, config: XLeRobotSimCameraConfig):
            super().__init__(config)
            self.config = config
            self._connected = False

        @property
        def is_connected(self) -> bool:
            return self._connected

        @staticmethod
        def find_cameras() -> list[dict]:
            return []

        def connect(self, warmup: bool = True) -> None:
            sim(self.config.height or 480, self.config.width or 640)
            self._connected = True

        def read(self, *args, **kwargs) -> np.ndarray:
            with _lock:
                s = sim()
                s.sync()
                return s.world.render(self.config.name)

        def async_read(self, *args, **kwargs) -> np.ndarray:
            return self.read()

        def read_latest(self, *args, **kwargs) -> np.ndarray:
            return self.read()

        def disconnect(self) -> None:
            self._connected = False

    # make_device_from_device_class finds the camera next to its config.
    module = sys.modules[__name__]
    XLeRobotSimCameraConfig.__module__ = module.__name__
    XLeRobotSimCamera.__module__ = module.__name__
    module.XLeRobotSimCameraConfig = XLeRobotSimCameraConfig
    module.XLeRobotSimCamera = XLeRobotSimCamera
