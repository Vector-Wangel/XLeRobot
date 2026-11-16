"""EnvHub environment: XLeRobot picking a cube from a table, simulated with MuJoCo.

The robot is the 0.3.0 three-omniwheel XLeRobot from ``simulation/mujoco/xlerobot.xml``. Its state,
actions and cameras use the names and units of the ``xlerobot`` LeRobot plugin with
``use_degrees=True``:

- arm and head joints in degrees, grippers 0-100 (``<motor>.pos``);
- base velocities in the robot frame, ``x.vel`` and ``y.vel`` in m/s and ``theta.vel`` in deg/s;
- cameras ``head``, ``left_wrist`` and ``right_wrist``.

A policy or dataset that uses these names works with ``--robot.type=sim`` on this environment and
``--robot.type=xlerobot --robot.use_degrees=true`` on the real robot. The joint conversions follow
the kinematics in ``software/src/model/SO101Robot.py``; check them against a calibrated robot
before relying on sim-to-real transfer (see README.md).

Arms and head are position controlled. The base is driven at the commanded body velocity: wheels
and floor contact are not simulated, as in ``simulation/mujoco/xlerobot_mujoco.py``.
"""

import atexit
import weakref
from collections.abc import Mapping, Sequence
from functools import partial
from pathlib import Path
from typing import Any

import gymnasium as gym
import mujoco
import numpy as np
from gymnasium import spaces

# Where this environment is published on the Hub.
REPO_ID = "VectorW/xlerobot-pick-cube-mujoco"
# Not resolved: in the Hugging Face cache, repository files are symlinks into blobs/ named by hash.
HERE = Path(__file__).absolute().parent
SCENE_FILE = "scene.xml"
ROBOT_FILE = "xlerobot.xml"
TASK = "xlerobot_pick_cube"
INSTRUCTION = "Pick up the red cube from the table."

# Plugin motor -> (MuJoCo joint, sign, offset in degrees): value = sign * degrees(q) + offset.
# shoulder_lift and elbow_flex follow SO101Kinematics.inverse_kinematics. The MJCF names its arms
# as seen from in front of the robot: its "_R" arm is on the robot's left, so it is the left arm.
JOINT_MAP: dict[str, tuple[str, int, float]] = {}
for side, suffix in (("left", "R"), ("right", "L")):
    JOINT_MAP |= {
        f"{side}_arm_shoulder_pan": (f"Rotation_{suffix}", 1, 0.0),
        f"{side}_arm_shoulder_lift": (f"Pitch_{suffix}", -1, 90.0),
        f"{side}_arm_elbow_flex": (f"Elbow_{suffix}", 1, -90.0),
        f"{side}_arm_wrist_flex": (f"Wrist_Pitch_{suffix}", 1, 0.0),
        f"{side}_arm_wrist_roll": (f"Wrist_Roll_{suffix}", 1, 0.0),
    }
JOINT_MAP |= {"head_motor_1": ("head_pan_joint", 1, 0.0), "head_motor_2": ("head_tilt_joint", 1, 0.0)}
# Plugin gripper -> MuJoCo jaw joint; 0 is closed and 100 fully open, in radians of the jaw.
GRIPPER_MAP = {"left_arm_gripper": "Jaw_R", "right_arm_gripper": "Jaw_L"}
GRIPPER_RANGE = (0.0, 1.6)
BASE = ("x.vel", "y.vel", "theta.vel")

# The plugin's observation and action order (XLerobot._state_ft).
MOTORS = [
    *(f"left_arm_{j}" for j in ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper")),
    *(f"right_arm_{j}" for j in ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper")),
    "head_motor_1",
    "head_motor_2",
]
STATE_NAMES = [f"{motor}.pos" for motor in MOTORS] + list(BASE)
# Arms reaching forward over the table edge with the grippers pointing down and half open, head
# looking down at the table. All zeros is the calibration pose: upper arms up, forearms forward.
HOME = {
    **{f"{side}_arm_shoulder_pan": 0.0 for side in ("left", "right")},
    **{f"{side}_arm_shoulder_lift": 35.0 for side in ("left", "right")},
    **{f"{side}_arm_elbow_flex": 0.0 for side in ("left", "right")},
    **{f"{side}_arm_wrist_flex": 40.0 for side in ("left", "right")},
    **{f"{side}_arm_wrist_roll": 0.0 for side in ("left", "right")},
    **{f"{side}_arm_gripper": 50.0 for side in ("left", "right")},
    "head_motor_1": 0.0,
    "head_motor_2": 35.0,
}

LEROBOT_SIM = {
    "fps": 30,
    "control_mode": "position",
    "semantics": "xlerobot-joint-degrees-v1",
    "state_names": STATE_NAMES,
    "action_names": STATE_NAMES,
    "robot_type": "xlerobot",
}

# Camera name -> (body, offset from the body origin, viewing direction, image up), in the robot frame
# (x forward, y left, z up) with every joint at zero: arms stretched forward, grippers pointing
# forward with the moving jaw on top, head level. The cameras then move with their body.
CAMERAS = {
    "head": ("head_tilt_link", (0.06, 0.0, 0.0), (1.0, 0.0, -0.27), (0.0, 0.0, 1.0)),
    # Under the fixed jaw, looking along the fingers. Fixed_Jaw_2 belongs to the robot's left arm.
    "left_wrist": ("Fixed_Jaw_2", (-0.02, 0.0, -0.05), (1.0, 0.0, 0.2), (0.0, 0.0, 1.0)),
    "right_wrist": ("Fixed_Jaw", (-0.02, 0.0, -0.05), (1.0, 0.0, 0.2), (0.0, 0.0, 1.0)),
}
CUBE_BODY = "red_cube"
LIFT_SUCCESS = 0.05  # metres above the cube's resting height


def repo_root() -> Path:
    """Directory holding the scene: this file's, or a snapshot of the Hub repository.

    LeRobot's in-process loader downloads ``env.py`` alone, into ``snapshots/<commit>/`` of the Hub
    cache; fetch the rest of that same commit. A checkout of XLeRobot or of the Hub repository needs
    nothing.
    """
    if (HERE / SCENE_FILE).is_file():
        return HERE
    from huggingface_hub import snapshot_download

    revision = HERE.name if HERE.parent.name == "snapshots" else None
    return Path(snapshot_download(REPO_ID, revision=revision))


def robot_dir(root: Path) -> Path:
    """Directory holding ``xlerobot.xml`` and its meshes: the Hub repository's copy, else XLeRobot's."""
    for candidate in (root / "xlerobot", root.parent / "mujoco"):
        if (candidate / ROBOT_FILE).is_file():
            return candidate
    raise FileNotFoundError(f"No {ROBOT_FILE} in {root / 'xlerobot'} or {root.parent / 'mujoco'}")


def _look_quat(direction: Sequence[float], up: Sequence[float]) -> np.ndarray:
    """Quaternion of a MuJoCo camera (looking along -z, y up) that looks along `direction`."""
    z = -np.asarray(direction, dtype=np.float64)
    z /= np.linalg.norm(z)
    x = np.cross(np.asarray(up, dtype=np.float64), z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    quat = np.zeros(4)
    mujoco.mju_mat2Quat(quat, np.column_stack([x, y, z]).ravel())
    return quat


def build_model(scene: Path, robot: Path) -> mujoco.MjModel:
    """Compile the scene with the robot, head actuators and the plugin's three cameras."""
    spec = mujoco.MjSpec.from_file(str(scene))
    robot_spec = mujoco.MjSpec.from_file(str(robot / ROBOT_FILE))
    # Contact groups: robot parts (contype 2, conaffinity 0) touch the table and objects
    # (conaffinity 3) but neither each other nor the floor, whose contype 1 they do not accept.
    # The model's arm meshes overlap the cart body once the arms bend down.
    for geom in robot_spec.geoms:
        if geom.contype or geom.conaffinity:
            geom.contype, geom.conaffinity = 2, 0
    spec.attach(robot_spec, frame=spec.worldbody.add_frame(name="robot_mount"), prefix="")
    for joint in ("head_pan_joint", "head_tilt_joint"):
        spec.add_actuator(
            name=joint, target=joint, trntype=mujoco.mjtTrn.mjTRN_JOINT,
            gaintype=mujoco.mjtGain.mjGAIN_FIXED, biastype=mujoco.mjtBias.mjBIAS_AFFINE,
            gainprm=[20.0] + [0.0] * 9, biasprm=[0.0, -20.0, -2.0] + [0.0] * 7,
            ctrlrange=spec.joint(joint).range, ctrllimited=True,
        )
    # A visible head: the model's head links carry no geometry.
    spec.body("head_tilt_link").add_geom(
        type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.03, 0.06, 0.03], rgba=[0.15, 0.15, 0.15, 1],
        contype=0, conaffinity=0,
    )
    for jaw in GRIPPER_MAP.values():
        spec.joint(jaw).range = GRIPPER_RANGE
        spec.actuator(jaw).ctrlrange = GRIPPER_RANGE
        # The light jaw has no rotor inertia in the model: give it some, as the servo has.
        spec.joint(jaw).armature = 0.05
    model = spec.compile()

    # Cameras are placed in the robot frame with every joint at zero, then expressed in their body frame.
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    robot_rot = data.body("chassis").xmat.reshape(3, 3)
    for name, (body_name, pos, direction, up) in CAMERAS.items():
        body = data.body(body_name)
        body_rot = body.xmat.reshape(3, 3)
        world_pos = body.xpos + robot_rot @ np.asarray(pos)
        world_dir = robot_rot @ np.asarray(direction)
        world_up = robot_rot @ np.asarray(up)
        cam_world = np.zeros(9)
        mujoco.mju_quat2Mat(cam_world, _look_quat(world_dir, world_up))
        local = body_rot.T @ cam_world.reshape(3, 3)
        quat = np.zeros(4)
        mujoco.mju_mat2Quat(quat, local.ravel())
        spec.body(body_name).add_camera(
            name=name, pos=body_rot.T @ (world_pos - body.xpos), quat=quat, fovy=70.0 if name == "head" else 80.0
        )
    model = spec.compile()
    # Track the commanded base velocity closely: the base is a velocity-controlled planar joint.
    for actuator in ("slider_actuator_x", "slider_actuator_y", "hinge_actuator_z"):
        index = model.actuator(actuator).id
        model.actuator_gainprm[index, 0] = 400.0
        model.actuator_biasprm[index, 2] = -400.0
    return model


def _set_joint_targets(model, data, values: Mapping[str, float], qpos: bool = False) -> None:
    """Write plugin-unit targets to the actuators (and, with `qpos`, to the joints)."""
    for motor, value in values.items():
        if motor in GRIPPER_MAP:
            joint = GRIPPER_MAP[motor]
            lo, hi = GRIPPER_RANGE
            q = lo + np.clip(value, 0.0, 100.0) / 100.0 * (hi - lo)
        else:
            joint, sign, offset = JOINT_MAP[motor]
            q = np.deg2rad(sign * (value - offset))
            q = float(np.clip(q, *model.joint(joint).range))
        data.ctrl[model.actuator(joint).id] = q
        if qpos:
            data.qpos[model.joint(joint).qposadr[0]] = q


class XLeRobotWorld:
    """Compiled model and physics of one XLeRobot scene, read and driven in the plugin's units."""

    def __init__(self, fps: int, height: int, width: int, scene: Path | None = None):
        root = repo_root()
        self.model = build_model(scene or root / SCENE_FILE, robot_dir(root))
        self.substeps = max(1, round(1 / (fps * self.model.opt.timestep)))
        self.model.opt.timestep = 1 / (fps * self.substeps)
        self.data = mujoco.MjData(self.model)
        self.height, self.width = height, width
        self._renderer: mujoco.Renderer | None = None
        self.base_joints = [self.model.joint(n).qposadr[0] for n in ("slide_joint_x", "slide_joint_y", "hinge_joint_z")]
        self.base_dofs = [self.model.joint(n).dofadr[0] for n in ("slide_joint_x", "slide_joint_y", "hinge_joint_z")]
        self.base_actuators = [self.model.actuator(n).id for n in ("slider_actuator_x", "slider_actuator_y", "hinge_actuator_z")]
        self.cube = self.model.body(CUBE_BODY).id
        self.cube_qadr = self.model.joint(self.model.body_jntadr[self.cube]).qposadr[0]
        self.cube_rest_z = 0.0
        self.base_command = np.zeros(3)

    # Joints, in plugin units.
    def position(self, motor: str) -> float:
        if motor in GRIPPER_MAP:
            lo, hi = GRIPPER_RANGE
            q = self.data.qpos[self.model.joint(GRIPPER_MAP[motor]).qposadr[0]]
            return float((q - lo) / (hi - lo) * 100.0)
        joint, sign, offset = JOINT_MAP[motor]
        return float(sign * np.rad2deg(self.data.qpos[self.model.joint(joint).qposadr[0]]) + offset)

    def set_position_target(self, motor: str, value: float) -> None:
        _set_joint_targets(self.model, self.data, {motor: value})

    # Base, in the robot frame: x forward and y left in m/s, theta counter-clockwise in deg/s. The
    # two slide joints move along the chassis axes at qpos = 0; the hinge after them turns the robot,
    # so robot-frame velocities are the slide velocities turned by the hinge angle.
    def set_base_velocity(self, x: float, y: float, theta: float) -> None:
        self.base_command = np.array([x, y, theta], dtype=np.float64)

    def _turn(self) -> tuple[float, float]:
        yaw = float(self.data.qpos[self.base_joints[2]])
        return np.cos(yaw), np.sin(yaw)

    def base_velocity(self) -> np.ndarray:
        vx, vy, wz = self.data.qvel[self.base_dofs]
        c, s = self._turn()
        return np.array([c * vx + s * vy, -s * vx + c * vy, np.rad2deg(wz)])

    def _apply_base_command(self) -> None:
        x, y, theta = self.base_command
        c, s = self._turn()
        self.data.ctrl[self.base_actuators[0]] = c * x - s * y
        self.data.ctrl[self.base_actuators[1]] = s * x + c * y
        self.data.ctrl[self.base_actuators[2]] = np.deg2rad(theta)

    def advance(self, seconds: float | None = None) -> None:
        """Step the physics one control period, or about `seconds`, holding the current commands."""
        steps = self.substeps if seconds is None else max(0, round(seconds / self.model.opt.timestep))
        for _ in range(steps):
            self._apply_base_command()
            mujoco.mj_step(self.model, self.data)

    def state(self) -> np.ndarray:
        return np.array([self.position(m) for m in MOTORS] + list(self.base_velocity()), dtype=np.float32)

    def apply_action(self, action: np.ndarray) -> None:
        for motor, value in zip(MOTORS, action[: len(MOTORS)], strict=True):
            self.set_position_target(motor, float(value))
        self.set_base_velocity(*map(float, action[len(MOTORS):]))

    def reset(self, rng: np.random.Generator, joint_noise: float, cube_xy_noise: float) -> None:
        mujoco.mj_resetData(self.model, self.data)
        values = {m: v + rng.uniform(-joint_noise, joint_noise) for m, v in HOME.items()}
        _set_joint_targets(self.model, self.data, values, qpos=True)
        a = self.cube_qadr
        self.data.qpos[a : a + 2] += rng.uniform(-cube_xy_noise, cube_xy_noise, 2)
        self.base_command = np.zeros(3)
        mujoco.mj_forward(self.model, self.data)
        self.advance(0.3)  # let the cube settle
        self.cube_rest_z = float(self.data.xpos[self.cube, 2])

    def cube_lift(self) -> float:
        return float(self.data.xpos[self.cube, 2] - self.cube_rest_z)

    def render(self, camera: str) -> np.ndarray:
        if self._renderer is None:
            self._renderer = mujoco.Renderer(self.model, self.height, self.width)
            # Close the GL context before interpreter shutdown tears down the GL bindings.
            ref = weakref.ref(self)
            atexit.register(lambda: (world := ref()) is not None and world.close())
        self._renderer.update_scene(self.data, camera=camera)
        return self._renderer.render().copy()

    def close(self) -> None:
        if self._renderer is not None:
            self._renderer.close()
            self._renderer = None


class XLeRobotEnv(gym.Env):
    """XLeRobot in a MuJoCo scene, with the ``xlerobot`` plugin's state, action and camera names."""

    metadata = {"render_modes": ["rgb_array"], "render_fps": 30}

    def __init__(
        self,
        fps: int = 30,
        episode_length: int = 900,
        observation_height: int = 480,
        observation_width: int = 640,
        cameras: Sequence[str] = tuple(CAMERAS),
        instruction: str = INSTRUCTION,
        joint_noise: float = 2.0,
        cube_xy_noise: float = 0.03,
        scene: str | Path | None = None,
    ):
        super().__init__()
        self.task = TASK
        self.fps = fps
        self._max_episode_steps = episode_length
        self._steps = 0
        self.height, self.width = observation_height, observation_width
        self.cameras = tuple(cameras)
        unknown = set(self.cameras) - set(CAMERAS)
        if unknown:
            raise ValueError(f"Unknown cameras {sorted(unknown)}; expected some of {list(CAMERAS)}")
        self.instruction = instruction
        self.joint_noise, self.cube_xy_noise = joint_noise, cube_xy_noise
        self.scene = Path(scene) if scene else None
        self._world: XLeRobotWorld | None = None
        image = spaces.Box(0, 255, (self.height, self.width, 3), np.uint8)
        self.observation_space = spaces.Dict(
            {
                "agent_pos": spaces.Box(-1e3, 1e3, (len(STATE_NAMES),), np.float32),
                "pixels": spaces.Dict(dict.fromkeys(self.cameras, image)),
            }
        )
        self.action_space = spaces.Box(-1e3, 1e3, (len(STATE_NAMES),), np.float32)

    @property
    def task_description(self) -> str:
        return self.instruction

    @property
    def world(self) -> XLeRobotWorld:
        """The physics, built on first use so async workers each own their GL context."""
        if self._world is None:
            self._world = XLeRobotWorld(self.fps, self.height, self.width, self.scene)
        return self._world

    def _obs(self) -> dict[str, Any]:
        return {
            "agent_pos": self.world.state(),
            "pixels": {camera: self.world.render(camera) for camera in self.cameras},
        }

    def reset(self, seed: int | None = None, **kwargs) -> tuple[dict[str, Any], dict[str, Any]]:
        super().reset(seed=seed)
        self.world.reset(self.np_random, self.joint_noise, self.cube_xy_noise)
        self._steps = 0
        return self._obs(), {"is_success": False}

    def step(self, action: np.ndarray) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        action = np.asarray(action, dtype=np.float64)
        if action.shape != self.action_space.shape:
            raise ValueError(f"Expected an action of shape {self.action_space.shape}, got {action.shape}")
        self.world.apply_action(action)
        self.world.advance()
        self._steps += 1
        lift = self.world.cube_lift()
        success = lift >= LIFT_SUCCESS
        truncated = self._steps >= self._max_episode_steps
        reward = float(np.clip(lift / LIFT_SUCCESS, 0.0, 1.0))
        return self._obs(), reward, success, truncated, {"is_success": success, "cube_lift": lift}

    def render(self, camera: str | None = None) -> np.ndarray:
        return self.world.render(camera or self.cameras[0])

    def close(self) -> None:
        if self._world is not None:
            self._world.close()
            self._world = None


def make_env(n_envs: int = 1, use_async_envs: bool = False, **kwargs: Any) -> dict[str, dict[int, Any]]:
    """EnvHub entry point: ``{"xlerobot_pick_cube": {0: vector_env}}``; ``kwargs`` override ``XLeRobotEnv``'s."""
    factory = partial(XLeRobotEnv, **kwargs)
    vector_cls = gym.vector.AsyncVectorEnv if use_async_envs else gym.vector.SyncVectorEnv
    return {TASK: {0: vector_cls([factory] * n_envs)}}
