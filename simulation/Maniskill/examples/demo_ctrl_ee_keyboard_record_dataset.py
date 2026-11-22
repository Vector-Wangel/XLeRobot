import gymnasium as gym
import numpy as np
import sapien
import pygame
import time
import math
import cv2
import json
import os
from pathlib import Path
from PIL import Image
import torch
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq
from typing import Dict, Any, List
import hashlib

from mani_skill.envs.sapien_env import BaseEnv
from mani_skill.utils import gym_utils
from mani_skill.utils.wrappers import RecordEpisode

import tyro
from dataclasses import dataclass
from typing import List, Optional, Annotated, Union

@dataclass
class Args:
    env_id: Annotated[str, tyro.conf.arg(aliases=["-e"])] = "PushCube-v1"
    """The environment ID of the task you want to simulate"""

    obs_mode: Annotated[str, tyro.conf.arg(aliases=["-o"])] = "sensor_data"
    """Observation mode - changed to sensor_data to get camera images"""

    robot_uids: Annotated[Optional[str], tyro.conf.arg(aliases=["-r"])] = None
    """Robot UID(s) to use"""

    sim_backend: Annotated[str, tyro.conf.arg(aliases=["-b"])] = "auto"
    """Which simulation backend to use"""

    reward_mode: Optional[str] = None
    """Reward mode"""

    num_envs: Annotated[int, tyro.conf.arg(aliases=["-n"])] = 1
    """Number of environments to run"""

    control_mode: Annotated[Optional[str], tyro.conf.arg(aliases=["-c"])] = None
    """Control mode"""

    render_mode: str = "rgb_array"
    """Render mode"""

    shader: str = "default"
    """Shader type"""

    pause: Annotated[bool, tyro.conf.arg(aliases=["-p"])] = False
    """Auto pause on load"""

    quiet: bool = False
    """Disable verbose output"""

    seed: Annotated[Optional[Union[int, List[int]]], tyro.conf.arg(aliases=["-s"])] = None
    """Random seed"""

    # Recording specific arguments
    dataset_name: str = "maniskill_teleoperation"
    """Name of the dataset"""

    output_dir: str = "./datasets"
    """Output directory for the dataset"""

    num_episodes: int = 5
    """Number of episodes to record"""

    episode_length: int = 1000
    """Maximum length of each episode in steps"""

    fps: int = 30
    """Recording FPS"""

    task_description: str = "Teleoperation demonstration"
    """Description of the task being performed"""

class LeRobotDatasetRecorder:
    """A lightweight recorder for LeRobot dataset v3 format"""
    
    def __init__(self, dataset_name: str, output_dir: str, fps: int = 30, task_description: str = ""):
        self.dataset_name = dataset_name
        self.output_dir = Path(output_dir)
        self.fps = fps
        self.task_description = task_description
        
        # Create dataset directory
        self.dataset_dir = self.output_dir / dataset_name
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize episode data storage
        self.current_episode_data = []
        self.episode_index = 0
        self.frame_index = 0
        
        # Dataset metadata
        self.dataset_info = {
            "codebase_version": "3.0",
            "robot_type": "maniskill_fetch",
            "fps": fps,
            "task": task_description,
            "created_at": datetime.now().isoformat(),
        }
        
        # Initialize features schema
        self.features = self._create_features_schema()
        
        print(f"Initialized LeRobot dataset recorder at: {self.dataset_dir}")
    
    def _create_features_schema(self) -> Dict[str, Any]:
        """Create the features schema for the dataset"""
        return {
            "observation.images.fetch_head": {
                "dtype": "image",
                "shape": [480, 640, 3],
                "names": ["height", "width", "channels"]
            },
            "observation.images.fetch_left_arm_camera": {
                "dtype": "image", 
                "shape": [480, 640, 3],
                "names": ["height", "width", "channels"]
            },
            "observation.images.fetch_right_arm_camera": {
                "dtype": "image",
                "shape": [480, 640, 3], 
                "names": ["height", "width", "channels"]
            },
            "observation.state": {
                "dtype": "float32",
                "shape": [16],  # Adjust based on your robot's state size
                "names": ["joint_" + str(i) for i in range(16)]
            },
            "action": {
                "dtype": "float32", 
                "shape": [16],  # Adjust based on your robot's action size
                "names": ["joint_" + str(i) for i in range(16)]
            },
            "episode_index": {
                "dtype": "int64",
                "shape": [1],
                "names": None
            },
            "frame_index": {
                "dtype": "int64", 
                "shape": [1],
                "names": None
            },
            "timestamp": {
                "dtype": "float64",
                "shape": [1], 
                "names": None
            },
            "task": {
                "dtype": "string",
                "shape": [1],
                "names": None
            }
        }
    
    def start_episode(self):
        """Start recording a new episode"""
        self.current_episode_data = []
        self.frame_index = 0
        print(f"Starting episode {self.episode_index}")
    
    def add_frame(self, observation: Dict[str, Any], action: np.ndarray, task: str = ""):
        """Add a frame to the current episode"""
        timestamp = time.time()
        
        # Process camera images
        camera_data = {}
        if 'sensor_images' in observation:
            for camera_name, camera_dict in observation['sensor_images'].items():
                if 'rgb' in camera_dict:
                    img = self._convert_tensor_to_numpy_image(camera_dict['rgb'])
                    # Save image to disk
                    img_filename = f"episode_{self.episode_index:06d}_frame_{self.frame_index:06d}_{camera_name}.png"
                    img_path = self.dataset_dir / "images" / img_filename
                    img_path.parent.mkdir(exist_ok=True)
                    Image.fromarray(img).save(img_path)
                    camera_data[f"observation.images.{camera_name}"] = str(img_path.relative_to(self.dataset_dir))
        
        # Create frame data
        frame_data = {
            "episode_index": self.episode_index,
            "frame_index": self.frame_index,
            "timestamp": timestamp,
            "task": task or self.task_description,
            "observation.state": observation.get('state', np.zeros(16, dtype=np.float32)),
            "action": action.astype(np.float32),
            **camera_data
        }
        
        self.current_episode_data.append(frame_data)
        self.frame_index += 1
    
    def end_episode(self):
        """End the current episode and save to parquet"""
        if not self.current_episode_data:
            print("No data in current episode, skipping...")
            return
        
        # Convert to pandas/pyarrow format
        episode_dict = {}
        for key in self.current_episode_data[0].keys():
            if key.startswith("observation.images."):
                # Image paths are strings
                episode_dict[key] = [frame[key] for frame in self.current_episode_data]
            else:
                # Numeric data - keep as list of arrays for PyArrow
                values_list = [frame[key] for frame in self.current_episode_data]
                episode_dict[key] = values_list
        
        # Create PyArrow table
        arrays = []
        names = []
        for key, values in episode_dict.items():
            names.append(key)
            if isinstance(values, list):  # String data (image paths) or list of arrays
                if values and isinstance(values[0], str):
                    # String data
                    arrays.append(pa.array(values))
                else:
                    # List of arrays - PyArrow can handle this directly
                    arrays.append(pa.array(values))
        
        table = pa.table(arrays, names=names)
        
        # Save episode to parquet file
        episode_file = self.dataset_dir / f"episode_{self.episode_index:06d}.parquet"
        pq.write_table(table, episode_file)
        
        print(f"Saved episode {self.episode_index} with {len(self.current_episode_data)} frames")
        self.episode_index += 1
    
    def finalize_dataset(self):
        """Finalize the dataset by saving metadata"""
        # Save dataset info
        info_dict = {
            **self.dataset_info,
            "total_episodes": self.episode_index,
            "total_frames": sum(len(ep) for ep in [self.current_episode_data]) if hasattr(self, 'current_episode_data') else 0,
            "features": self.features
        }
        
        with open(self.dataset_dir / "meta.json", "w") as f:
            json.dump(info_dict, f, indent=2)
        
        # Create episode statistics
        episodes_info = []
        for ep_idx in range(self.episode_index):
            episode_file = self.dataset_dir / f"episode_{ep_idx:06d}.parquet"
            if episode_file.exists():
                table = pq.read_table(episode_file)
                episodes_info.append({
                    "episode_index": ep_idx,
                    "num_frames": len(table),
                    "file_path": str(episode_file.relative_to(self.dataset_dir))
                })
        
        episodes_table = pa.table({
            "episode_index": [ep["episode_index"] for ep in episodes_info],
            "num_frames": [ep["num_frames"] for ep in episodes_info], 
            "file_path": [ep["file_path"] for ep in episodes_info]
        })
        
        pq.write_table(episodes_table, self.dataset_dir / "episodes.parquet")
        
        print(f"Dataset finalized with {self.episode_index} episodes")
    
    def _convert_tensor_to_numpy_image(self, tensor_image):
        """Convert tensor image to numpy array for saving"""
        if hasattr(tensor_image, 'cpu'):
            tensor_image = tensor_image.cpu()
        
        if hasattr(tensor_image, 'numpy'):
            image = tensor_image.numpy()
        else:
            image = tensor_image
        
        if image.dtype == np.float32 or image.dtype == np.float64:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        else:
            image = image.astype(np.uint8)
        
        if image.ndim == 4:
            image = image[0]
        
        if image.shape[-1] == 4:
            image = image[..., :3]
        
        return image

def get_mapped_joints(robot):
    """Get the current joint positions from the robot and map them correctly"""
    if robot is None:
        return np.zeros(16)
        
    full_joints = robot.get_qpos()
    
    if hasattr(full_joints, 'numpy'):
        full_joints = full_joints.numpy()
    
    if full_joints.ndim > 1:
        full_joints = full_joints.squeeze()
    
    mapped_joints = np.zeros(16)
    
    if len(full_joints) >= 15:
        # Base joints: [0,2] → [0,1]
        mapped_joints[0] = full_joints[0]  # Base X position
        mapped_joints[1] = full_joints[2]  # Base rotation
        
        # First arm: [3,6,9,11,13] → [2,3,4,5,6]
        mapped_joints[2] = full_joints[3]
        mapped_joints[3] = full_joints[6]
        mapped_joints[4] = full_joints[9]
        mapped_joints[5] = full_joints[11]
        mapped_joints[6] = full_joints[13]
        
        # Second arm: [4,7,10,12,14] → [7,8,9,10,11]
        mapped_joints[7] = full_joints[4]
        mapped_joints[8] = full_joints[7]
        mapped_joints[9] = full_joints[10]
        mapped_joints[10] = full_joints[12]
        mapped_joints[11] = full_joints[14]
        if len(full_joints) > 15:
            mapped_joints[12] = full_joints[15]
        if len(full_joints) > 16:
            mapped_joints[13] = full_joints[16]
        if len(full_joints) > 5:
            mapped_joints[14] = full_joints[5]
        if len(full_joints) > 8:
            mapped_joints[15] = full_joints[8]
    
    return mapped_joints

def inverse_kinematics(x, y, l1=0.1159, l2=0.1350):
    """Calculate inverse kinematics for a 2-link robotic arm"""
    theta1_offset = math.atan2(0.028, 0.11257)
    theta2_offset = math.atan2(0.0052, 0.1349) + theta1_offset
    
    r = math.sqrt(x**2 + y**2)
    r_max = l1 + l2
    
    if r > r_max:
        scale_factor = r_max / r
        x *= scale_factor
        y *= scale_factor
        r = r_max
    
    r_min = abs(l1 - l2)
    if r < r_min and r > 0:
        scale_factor = r_min / r
        x *= scale_factor
        y *= scale_factor
        r = r_min
    
    cos_theta2 = -(r**2 - l1**2 - l2**2) / (2 * l1 * l2)
    theta2 = math.pi - math.acos(cos_theta2)
    
    beta = math.atan2(y, x)
    gamma = math.atan2(l2 * math.sin(theta2), l1 + l2 * math.cos(theta2))
    theta1 = beta + gamma
    
    joint2 = theta1 + theta1_offset
    joint3 = theta2 + theta2_offset
    
    joint2 = max(-0.1, min(3.45, joint2))
    joint3 = max(-0.2, min(math.pi, joint3))
    
    return joint2, joint3

def main(args: Args):
    pygame.init()
    
    # Initialize dataset recorder
    recorder = LeRobotDatasetRecorder(
        dataset_name=args.dataset_name,
        output_dir=args.output_dir,
        fps=args.fps,
        task_description=args.task_description
    )
    
    # Set up pygame display
    control_panel_width = 600
    screen_width = control_panel_width + 20
    screen_height = 750
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("LeRobot Dataset Recorder - Use keys to move")
    font = pygame.font.SysFont(None, 24)
    
    np.set_printoptions(suppress=True, precision=3)
    verbose = not args.quiet
    if isinstance(args.seed, int):
        args.seed = [args.seed]
    if args.seed is not None:
        np.random.seed(args.seed[0])
    
    parallel_in_single_scene = args.render_mode == "human"
    if args.render_mode == "human" and args.obs_mode in ["sensor_data", "rgb", "rgbd", "depth", "point_cloud"]:
        print("Disabling parallel single scene/GUI render as observation mode is a visual one")
        parallel_in_single_scene = False
    if args.render_mode == "human" and args.num_envs == 1:
        parallel_in_single_scene = False
    
    env_kwargs = dict(
        obs_mode=args.obs_mode,
        reward_mode=args.reward_mode,
        control_mode=args.control_mode,
        render_mode=args.render_mode,
        sensor_configs=dict(shader_pack=args.shader),
        human_render_camera_configs=dict(shader_pack=args.shader),
        viewer_camera_configs=dict(shader_pack=args.shader),
        num_envs=args.num_envs,
        sim_backend=args.sim_backend,
        enable_shadow=True,
        parallel_in_single_scene=parallel_in_single_scene,
    )
    
    if args.robot_uids is not None:
        env_kwargs["robot_uids"] = tuple(args.robot_uids.split(","))
        if len(env_kwargs["robot_uids"]) == 1:
            env_kwargs["robot_uids"] = env_kwargs["robot_uids"][0]
    
    env: BaseEnv = gym.make(args.env_id, **env_kwargs)

    if verbose:
        print("Observation space", env.observation_space)
        print("Action space", env.action_space)
        if env.unwrapped.agent is not None:
            print("Control mode", env.unwrapped.control_mode)
        print("Reward mode", env.unwrapped.reward_mode)

    obs, _ = env.reset(seed=args.seed, options=dict(reconfigure=True))
    if args.seed is not None and env.action_space is not None:
        env.action_space.seed(args.seed[0])
    if args.render_mode is not None:
        viewer = env.render()
        if isinstance(viewer, sapien.utils.Viewer):
            viewer.paused = args.pause
        env.render()
    
    action = env.action_space.sample() if env.action_space is not None else None
    action = np.zeros_like(action)
    
    # Initialize target joint positions with zeros
    target_joints = np.zeros_like(action)
    target_joints[6] = 1.57 
    target_joints[11] = 1.57 

    # Initialize end effector positions for both arms
    initial_ee_pos_arm1 = np.array([0.247, -0.023])
    initial_ee_pos_arm2 = np.array([0.247, -0.023])
    ee_pos_arm1 = initial_ee_pos_arm1.copy()
    ee_pos_arm2 = initial_ee_pos_arm2.copy()
    
    # Initialize pitch adjustments for end effector orientation
    initial_pitch_1 = 0.0
    initial_pitch_2 = 0.0
    pitch_1 = initial_pitch_1
    pitch_2 = initial_pitch_2
    pitch_step = 0.02
    
    # Define tip length for vertical position compensation
    tip_length = 0.108
    
    # Define step sizes
    joint_step = 0.01
    ee_step = 0.005
    
    # Define the gain for the proportional controller
    p_gain = np.ones_like(action)
    p_gain[0] = 2     # Base forward/backward
    p_gain[1] = 0.5   # Base rotation
    p_gain[2:7] = 1.0   # First arm joints
    p_gain[7:12] = 1.0  # Second arm joints
    p_gain[12:14] = 0.05  # Gripper joints
    if len(p_gain) > 14:
        p_gain[14:16] = 2  # Head motor joints
    
    # Get robot instance
    robot = None
    if hasattr(env.unwrapped, "agent"):
        robot = env.unwrapped.agent.robot
    elif hasattr(env.unwrapped, "agents") and len(env.unwrapped.agents) > 0:
        robot = env.unwrapped.agents[0]
    
    print("robot", robot)
    
    # Get initial joint positions
    current_joints = get_mapped_joints(robot)
    target_joints = np.zeros_like(current_joints)
    target_joints[6] = 1.57 
    target_joints[11] = 1.57 
    
    # Set initial joint positions based on inverse kinematics
    try:
        target_joints[3], target_joints[4] = inverse_kinematics(ee_pos_arm1[0], ee_pos_arm1[1])
        target_joints[8], target_joints[9] = inverse_kinematics(ee_pos_arm2[0], ee_pos_arm2[1])
    except Exception as e:
        print(f"Error calculating initial inverse kinematics: {e}")
    
    # Recording state
    recording = False
    current_episode = 0
    step_counter = 0
    warmup_steps = 50
    episode_step_counter = 0
    
    print("="*50)
    print("LeRobot Dataset Recorder Ready!")
    print("Controls:")
    print("SPACE: Start/Stop recording")
    print("R: Start new episode (while recording)")
    print("ESC: Finish recording and save dataset")
    print("="*50)
    
    clock = pygame.time.Clock()
    
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Toggle recording
                        if not recording:
                            recording = True
                            recorder.start_episode()
                            episode_step_counter = 0
                            print(f"Started recording episode {current_episode}")
                        else:
                            recording = False
                            recorder.end_episode()
                            current_episode += 1
                            print(f"Stopped recording. Episodes recorded: {current_episode}")
                    
                    elif event.key == pygame.K_r and recording:
                        # Start new episode while recording
                        recorder.end_episode()
                        current_episode += 1
                        recorder.start_episode()
                        episode_step_counter = 0
                        print(f"Started new episode {current_episode}")
                    
                    elif event.key == pygame.K_ESCAPE:
                        # Finish recording and save dataset
                        if recording:
                            recorder.end_episode()
                            current_episode += 1
                        recorder.finalize_dataset()
                        print("Dataset saved successfully!")
                        pygame.quit()
                        env.close()
                        return
                    
                    elif event.key == pygame.K_x:
                        # Reset all positions
                        ee_pos_arm1 = initial_ee_pos_arm1.copy()
                        ee_pos_arm2 = initial_ee_pos_arm2.copy()
                        pitch_1 = initial_pitch_1
                        pitch_2 = initial_pitch_2
                        target_joints = np.zeros_like(target_joints)
                        
                        try:
                            compensated_y1 = ee_pos_arm1[1] - tip_length * math.sin(pitch_1)
                            target_joints[3], target_joints[4] = inverse_kinematics(ee_pos_arm1[0], compensated_y1)
                            
                            compensated_y2 = ee_pos_arm2[1] - tip_length * math.sin(pitch_2)
                            target_joints[8], target_joints[9] = inverse_kinematics(ee_pos_arm2[0], compensated_y2)
                            
                            target_joints[5] = target_joints[3] - target_joints[4] + pitch_1
                            target_joints[10] = target_joints[8] - target_joints[9] + pitch_2
                        except Exception as e:
                            print(f"Error calculating inverse kinematics during reset: {e}")
                        
                        print("All positions reset to initial values")
            
            keys = pygame.key.get_pressed()
            
            # Update target joint positions based on key presses - only after warmup
            if step_counter >= warmup_steps:
                # Base forward/backward - direct control
                if keys[pygame.K_w]:
                    action[0] = 0.1  # Forward
                elif keys[pygame.K_s]:
                    action[0] = -0.1  # Backward
                else:
                    action[0] = 0.0  # Stop forward/backward movement
                    
                # Base turning - using target_joints and P control
                if keys[pygame.K_a]:
                    target_joints[1] += joint_step*2  # Turn left
                elif keys[pygame.K_d]:
                    target_joints[1] -= joint_step*2  # Turn right
                
                # Arm control - using end effector positions and inverse kinematics
                # First arm end effector control
                if keys[pygame.K_8]:  # Move end effector up
                    ee_pos_arm1[1] += ee_step
                if keys[pygame.K_u]:  # Move end effector down
                    ee_pos_arm1[1] -= ee_step
                if keys[pygame.K_9]:  # Move end effector forward
                    ee_pos_arm1[0] += ee_step
                if keys[pygame.K_i]:  # Move end effector backward
                    ee_pos_arm1[0] -= ee_step
                    
                # Calculate inverse kinematics for first arm
                compensated_y = ee_pos_arm1[1] + tip_length * math.sin(pitch_1)
                target_joints[3], target_joints[4] = inverse_kinematics(ee_pos_arm1[0], compensated_y)

                # Direct joint control for remaining joints of first arm
                if keys[pygame.K_7]:
                    target_joints[2] += joint_step
                if keys[pygame.K_y]:
                    target_joints[2] -= joint_step
                    
                # Pitch control for first arm
                if keys[pygame.K_0]:
                    pitch_1 += pitch_step
                if keys[pygame.K_o]:
                    pitch_1 -= pitch_step
                    
                # Apply pitch adjustment to joint 5 based on joints 3 and 4
                target_joints[5] = target_joints[3] - target_joints[4] + pitch_1
                
                # Wrist control for first arm
                if keys[pygame.K_MINUS]:
                    target_joints[6] += joint_step*3
                if keys[pygame.K_p]:
                    target_joints[6] -= joint_step*3
                
                # Second arm end effector control
                if keys[pygame.K_j]:  # Move end effector up
                    ee_pos_arm2[1] += ee_step
                if keys[pygame.K_m]:  # Move end effector down
                    ee_pos_arm2[1] -= ee_step
                if keys[pygame.K_k]:  # Move end effector forward
                    ee_pos_arm2[0] += ee_step
                if keys[pygame.K_COMMA]:  # Move end effector backward
                    ee_pos_arm2[0] -= ee_step
                    
                compensated_y = ee_pos_arm2[1] + tip_length * math.sin(pitch_2)
                target_joints[8], target_joints[9] = inverse_kinematics(ee_pos_arm2[0], compensated_y)
                
                # Direct joint control for remaining joints of second arm
                if keys[pygame.K_h]:
                    target_joints[7] += joint_step
                if keys[pygame.K_n]:
                    target_joints[7] -= joint_step
                    
                # Pitch control for second arm
                if keys[pygame.K_l]:
                    pitch_2 += pitch_step
                if keys[pygame.K_PERIOD]:
                    pitch_2 -= pitch_step
                    
                # Apply pitch adjustment to joint 10 based on joints 8 and 9
                target_joints[10] = target_joints[8] - target_joints[9] + pitch_2
                
                # Wrist control for second arm
                if keys[pygame.K_SEMICOLON]:
                    target_joints[11] += joint_step*3
                if keys[pygame.K_SLASH]:
                    target_joints[11] -= joint_step*3
                
                # Gripper control - toggle between open and closed
                if keys[pygame.K_v]:
                    if target_joints[12] < 0.4:
                        target_joints[12] = 2.5  # Open
                    else:
                        target_joints[12] = 0.1  # Close
                    pygame.time.delay(200)
                    
                if keys[pygame.K_b]:
                    if target_joints[13] < 0.4:
                        target_joints[13] = 2.5  # Open
                    else:
                        target_joints[13] = 0.1  # Close
                    pygame.time.delay(200)
                
                # Head motor control - set target positions
                if len(target_joints) > 14:
                    if keys[pygame.K_r]:
                        target_joints[14] += joint_step*2
                    if keys[pygame.K_t]:
                        target_joints[14] -= joint_step*2
                    if keys[pygame.K_f]:
                        target_joints[15] += joint_step*2
                    if keys[pygame.K_g]:
                        target_joints[15] -= joint_step*2
            
            # Get current joint positions using our mapping function
            current_joints = get_mapped_joints(robot)
            
            # Simple P controller for arm joints
            if step_counter < warmup_steps:
                action = np.zeros_like(action)
            else:
                # Apply P control to turning and arm joints
                for i in range(1, len(action)):
                    if i < len(target_joints) and i < len(current_joints):
                        action[i] = p_gain[i] * (target_joints[i] - current_joints[i])
            
            # Step the environment
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Record data if recording is active
            if recording and step_counter >= warmup_steps:
                # Get sensor images
                sensor_images = {}
                try:
                    sensor_images = env.unwrapped.get_sensor_images()
                except:
                    pass
                
                # Create observation dict for recorder
                observation_dict = {
                    'sensor_images': sensor_images,
                    'state': current_joints
                }
                
                # Add frame to recorder
                recorder.add_frame(
                    observation=observation_dict,
                    action=action,
                    task=args.task_description
                )
                
                episode_step_counter += 1
                
                # Auto-end episode if it reaches max length
                if episode_step_counter >= args.episode_length:
                    recorder.end_episode()
                    current_episode += 1
                    if current_episode < args.num_episodes:
                        recorder.start_episode()
                        episode_step_counter = 0
                        print(f"Auto-started new episode {current_episode}")
                    else:
                        recording = False
                        print(f"Reached maximum episodes ({args.num_episodes}). Recording stopped.")
            
            step_counter += 1
            
            # Render environment
            if args.render_mode is not None:
                env.render()
            
            # Update pygame display
            screen.fill((0, 0, 0))
            
            y_pos = 10
            
            # Recording status
            status_color = (0, 255, 0) if recording else (255, 0, 0)
            status_text = "RECORDING" if recording else "NOT RECORDING"
            status_surface = font.render(f"Status: {status_text}", True, status_color)
            screen.blit(status_surface, (10, y_pos))
            y_pos += 30
            
            # Episode info
            episode_surface = font.render(f"Episodes recorded: {current_episode}", True, (255, 255, 255))
            screen.blit(episode_surface, (10, y_pos))
            y_pos += 25
            
            if recording:
                frame_surface = font.render(f"Episode frames: {episode_step_counter}", True, (255, 255, 255))
                screen.blit(frame_surface, (10, y_pos))
                y_pos += 25
            
            # Add warmup status
            if step_counter < warmup_steps:
                warmup_text = font.render(f"WARMUP: {step_counter}/{warmup_steps} steps", True, (255, 0, 0))
                screen.blit(warmup_text, (10, y_pos))
                y_pos += 30
            
            # Control instructions
            y_pos += 10
            instructions = [
                "SPACE: Start/Stop recording",
                "R: New episode (while recording)", 
                "ESC: Finish and save dataset",
                "X: Reset positions",
                "",
                "Robot Controls:",
                "W/S: Base forward/back",
                "A/D: Base rotation",
                "8/U, 9/I: Arm1 EE Y/X",
                "J/M, K/,: Arm2 EE Y/X", 
                "V/B: Toggle grippers",
                "0/O, L/.: Pitch control"
            ]
            
            for instruction in instructions:
                if instruction:  # Skip empty lines
                    inst_surface = font.render(instruction, True, (200, 200, 200))
                    screen.blit(inst_surface, (10, y_pos))
                y_pos += 20
            
            pygame.display.flip()
            clock.tick(args.fps)
            
            if args.render_mode is None or args.render_mode != "human":
                if (terminated | truncated).any():
                    break
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        # Clean up
        if recording:
            recorder.end_episode()
        recorder.finalize_dataset()
        pygame.quit()
        env.close()
        print("Recording session finished and dataset saved!")

if __name__ == "__main__":
    parsed_args = tyro.cli(Args)
    main(parsed_args)