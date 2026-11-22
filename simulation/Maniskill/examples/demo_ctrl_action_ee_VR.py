import gymnasium as gym
import numpy as np
import sapien
import pygame
import time
import math
import asyncio
import threading
import cv2
from PIL import Image
import torch

# Add Rerun imports
try:
    import rerun as rr
    RERUN_AVAILABLE = True
except ImportError:
    RERUN_AVAILABLE = False
    print("Warning: Rerun not available. Install with: pip install rerun-sdk")

from mani_skill.envs.sapien_env import BaseEnv
from mani_skill.utils import gym_utils
from mani_skill.utils.wrappers import RecordEpisode

# Import vr_monitor instead of OculusReader
import sys
import os
sys.path.append(os.path.abspath("/home/vec/lerobot/mani_skill/examples"))
from mani_skill.examples.vr_monitor import VRMonitor

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
    """Robot UID(s) to use. Can be a comma separated list of UIDs or empty string to have no agents. If not given then defaults to the environments default robot"""

    sim_backend: Annotated[str, tyro.conf.arg(aliases=["-b"])] = "auto"
    """Which simulation backend to use. Can be 'auto', 'cpu', 'gpu'"""

    reward_mode: Optional[str] = None
    """Reward mode"""

    num_envs: Annotated[int, tyro.conf.arg(aliases=["-n"])] = 1
    """Number of environments to run."""

    control_mode: Annotated[Optional[str], tyro.conf.arg(aliases=["-c"])] = None
    """Control mode"""

    render_mode: str = "rgb_array"
    """Render mode - using rgb_array to get camera images"""

    shader: str = "default"
    """Change shader used for all cameras in the environment for rendering. Default is 'minimal' which is very fast. Can also be 'rt' for ray tracing and generating photo-realistic renders. Can also be 'rt-fast' for a faster but lower quality ray-traced renderer"""

    record_dir: Optional[str] = None
    """Directory to save recordings"""

    pause: Annotated[bool, tyro.conf.arg(aliases=["-p"])] = False
    """If using human render mode, auto pauses the simulation upon loading"""

    quiet: bool = False
    """Disable verbose output."""

    seed: Annotated[Optional[Union[int, List[int]]], tyro.conf.arg(aliases=["-s"])] = None
    """Seed(s) for random actions and simulator. Can be a single integer or a list of integers. Default is None (no seeds)"""

    show_cameras: bool = True
    """Whether to show camera feeds in Rerun"""

    debug_cameras: bool = False
    """Enable debug output for camera processing"""

    use_rerun: bool = True
    """Whether to use Rerun for camera visualization"""

def get_mapped_joints(robot):
    """
    Get the current joint positions from the robot and map them correctly to the target joints.
    
    The mapping is:
    - full_joints[0,2] → current_joints[0,1] (base x position and base rotation)
    - full_joints[3,6,9,11,13] → current_joints[2,3,4,5,6] (first arm joints)
    - full_joints[4,7,10,12,14] → current_joints[7,8,9,10,11] (second arm joints)
    
    Returns:
        np.ndarray: Mapped joint positions with shape matching the target_joints
    """
    if robot is None:
        return np.zeros(16)  # Default size for action
        
    # Get full joint positions
    full_joints = robot.get_qpos()
    
    # Convert tensor to numpy array if needed
    if hasattr(full_joints, 'numpy'):
        full_joints = full_joints.numpy()
    
    # Handle case where it's a 2D tensor/array
    if full_joints.ndim > 1:
        full_joints = full_joints.squeeze()
    
    # Create the mapped joints array with correct size
    mapped_joints = np.zeros(16)
    
    # Map the joints according to the specified mapping
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
        mapped_joints[12] = full_joints[15]
        mapped_joints[13] = full_joints[16]
    
    return mapped_joints

def inverse_kinematics(x, y, l1=0.1159, l2=0.1350):
    """
    Calculate inverse kinematics for a 2-link robotic arm, considering joint offsets
    
    Parameters:
        x: End effector x coordinate
        y: End effector y coordinate
        l1: Upper arm length (default 0.1159 m)
        l2: Lower arm length (default 0.1350 m)
        
    Returns:
        joint2, joint3: Joint angles in radians as defined in the URDF file
    """
    # Calculate joint2 and joint3 offsets in theta1 and theta2
    theta1_offset = -math.atan2(0.028, 0.11257)  # theta1 offset when joint2=0
    theta2_offset = -math.atan2(0.0052, 0.1349) + theta1_offset  # theta2 offset when joint3=0
    
    # Calculate distance from origin to target point
    r = math.sqrt(x**2 + y**2)
    r_max = l1 + l2  # Maximum reachable distance
    
    # If target point is beyond maximum workspace, scale it to the boundary
    if r > r_max:
        scale_factor = r_max / r
        x *= scale_factor
        y *= scale_factor
        r = r_max
    
    # If target point is less than minimum workspace (|l1-l2|), scale it
    r_min = abs(l1 - l2)
    if r < r_min and r > 0:
        scale_factor = r_min / r
        x *= scale_factor
        y *= scale_factor
        r = r_min
    
    # Use law of cosines to calculate theta2
    cos_theta2 = -(r**2 - l1**2 - l2**2) / (2 * l1 * l2)
    
    # Calculate theta2 (elbow angle)
    theta2 = math.pi - math.acos(cos_theta2)
    
    # Calculate theta1 (shoulder angle)
    beta = math.atan2(y, x)
    gamma = math.atan2(l2 * math.sin(theta2), l1 + l2 * math.cos(theta2))
    theta1 = beta + gamma
    
    # Convert theta1 and theta2 to joint2 and joint3 angles
    joint2 = theta1 - theta1_offset
    joint3 = theta2 - theta2_offset
    
    # Ensure angles are within URDF limits
    joint2 = max(-0.1, min(3.45, joint2))
    joint3 = max(-0.2, min(math.pi, joint3))
    
    return joint2, joint3

def convert_tensor_to_numpy_image(tensor_image):
    """Convert tensor image to numpy array for display"""
    # Handle PyTorch tensors
    if hasattr(tensor_image, 'cpu'):
        # Move tensor to CPU first if it's on GPU
        tensor_image = tensor_image.cpu()
    
    if hasattr(tensor_image, 'numpy'):
        image = tensor_image.numpy()
    else:
        image = tensor_image
    
    # Handle different image formats
    if image.dtype == np.float32 or image.dtype == np.float64:
        # Normalize to 0-255 range
        if image.max() <= 1.0:
            image = (image * 255).astype(np.uint8)
        else:
            image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    
    # Remove batch dimension if present
    if image.ndim == 4:
        image = image[0]  # Take first batch
    
    # Convert RGBA to RGB if needed
    if image.shape[-1] == 4:
        image = image[..., :3]
    
    return image

def main(args: Args):
    pygame.init()
    
    # Initialize Rerun if requested and available
    if args.use_rerun and args.show_cameras and RERUN_AVAILABLE:
        rr.init("mani_skill_vr_camera_demo")
        rr.spawn()
        print("Rerun initialized for camera visualization")
    elif args.use_rerun and not RERUN_AVAILABLE:
        print("Warning: Rerun requested but not available. Install with: pip install rerun-sdk")
    
    screen_width, screen_height = 600, 750
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Control Window - VR Controller Input (Cameras in Rerun)")
    font = pygame.font.SysFont(None, 24)
    
    # Initialize the VRMonitor for VR controller input
    vr_monitor = VRMonitor()
    
    # Start VR monitoring in a separate thread
    vr_thread = threading.Thread(target=lambda: asyncio.run(vr_monitor.start_monitoring()), daemon=True)
    vr_thread.start()
    
    # Wait a bit for VR monitor to initialize
    time.sleep(2)
    
    # Define scale factor for VR to robot mapping
    vr_scale_y = 1
    vr_scale_x = 0.5
    vr_scale_z = -0.6


    np.set_printoptions(suppress=True, precision=3)
    verbose = not args.quiet
    if isinstance(args.seed, int):
        args.seed = [args.seed]
    if args.seed is not None:
        np.random.seed(args.seed[0])
    parallel_in_single_scene = args.render_mode == "human"
    if args.render_mode == "human" and args.obs_mode in ["sensor_data", "rgb", "rgbd", "depth", "point_cloud"]:
        print("Disabling parallel single scene/GUI render as observation mode is a visual one. Change observation mode to state or state_dict to see a parallel env render")
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
    env: BaseEnv = gym.make(
        args.env_id,
        **env_kwargs
    )
    record_dir = args.record_dir
    if record_dir:
        record_dir = record_dir.format(env_id=args.env_id)
        env = RecordEpisode(env, record_dir, info_on_video=False, save_trajectory=False, max_steps_per_video=gym_utils.find_max_episode_steps_value(env))

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
    target_joints[3] = 0.303
    target_joints[4] = 0.556
    target_joints[8] = 0.303
    target_joints[9] = 0.556

    # Initialize end effector positions for both arms
    initial_ee_pos_arm1 = np.array([0.247, -0.023])  # Initial position for first arm
    initial_ee_pos_arm2 = np.array([0.247, -0.023])  # Initial position for second arm
    ee_pos_arm1 = initial_ee_pos_arm1.copy()
    ee_pos_arm2 = initial_ee_pos_arm2.copy()
    
    # Initialize pitch adjustments for end effector orientation
    initial_pitch_1 = 0.0  # Initial pitch adjustment for first arm
    initial_pitch_2 = 0.0  # Initial pitch adjustment for second arm
    pitch_1 = initial_pitch_1
    pitch_2 = initial_pitch_2
    pitch_step = 0.02  # Step size for pitch adjustment
    
    # Define tip length for vertical position compensation
    tip_length = 0.108  # Length from wrist to end effector tip
    
    # Define the step size for changing target joints and end effector positions
    joint_step = 0.01
    ee_step = 0.005  # Step size for end effector position control
    
    # Define the gain for the proportional controller as a list for each joint
    p_gain = np.ones_like(action)  # Default all gains to 1.0
    # Specific gains can be adjusted here
    p_gain[0] = 1.5    # Base forward/backward
    p_gain[1] = 0.8   # Base rotation - lower gain for smoother turning
    p_gain[2:7] = 1.0   # First arm joints
    p_gain[7:12] = 1.0  # Second arm joints
    p_gain[12:14] = 0.1  # Gripper joints
    p_gain[14:16] = 2  # Headset joints
    
    # Get initial joint positions if available
    current_joints = np.zeros_like(action)
    robot = None
    
    # Try to get the robot instance for direct access
    if hasattr(env.unwrapped, "agent"):
        robot = env.unwrapped.agent.robot
    elif hasattr(env.unwrapped, "agents") and len(env.unwrapped.agents) > 0:
        robot = env.unwrapped.agents[0]  # Get the first robot if multiple exist
    
    print("robot", robot)
    
    # Get the correctly mapped joints
    current_joints = get_mapped_joints(robot)
    
    # Ensure target_joints is a numpy array with the same shape as current_joints
    target_joints = np.zeros_like(current_joints)
    
    # Set initial joint positions based on inverse kinematics from initial end effector positions
    try:
        target_joints[3], target_joints[4] = inverse_kinematics(ee_pos_arm1[0], ee_pos_arm1[1])
        target_joints[8], target_joints[9] = inverse_kinematics(ee_pos_arm2[0], ee_pos_arm2[1])
    except Exception as e:
        print(f"Error calculating initial inverse kinematics: {e}")
    
    # Add step counter for warmup phase
    step_counter = 0
    warmup_steps = 50
    
    # Variables for VR control tracking
    last_gripper_state_left = False
    last_gripper_state_right = False
    
    # Variables for auto-reset functionality
    last_vr_activity_time = time.time()
    auto_reset_timeout = 30.0  # Reset after 30 seconds of no VR activity
    
    def reset_positions():
        """Reset all positions to initial values"""
        nonlocal ee_pos_arm1, ee_pos_arm2, pitch_1, pitch_2, target_joints
        nonlocal last_gripper_state_left, last_gripper_state_right
        
        # Reset end effector positions
        ee_pos_arm1 = initial_ee_pos_arm1.copy()
        ee_pos_arm2 = initial_ee_pos_arm2.copy()
        
        # Reset pitch adjustments
        pitch_1 = initial_pitch_1
        pitch_2 = initial_pitch_2
        
        # Reset target joints
        target_joints = np.zeros_like(target_joints)
        
        # Reset gripper states
        last_gripper_state_left = False
        last_gripper_state_right = False
        
        # Calculate initial joint positions based on inverse kinematics
        try:
            compensated_y1 = ee_pos_arm1[1] - tip_length * math.sin(pitch_1)
            target_joints[3], target_joints[4] = inverse_kinematics(ee_pos_arm1[0], compensated_y1)
            
            compensated_y2 = ee_pos_arm2[1] - tip_length * math.sin(pitch_2)
            target_joints[8], target_joints[9] = inverse_kinematics(ee_pos_arm2[0], compensated_y2)
            
            # Apply pitch adjustment to joint 5 and 10
            target_joints[5] = target_joints[3] - target_joints[4] + pitch_1
            target_joints[10] = target_joints[8] - target_joints[9] + pitch_2
        except Exception as e:
            print(f"Error calculating inverse kinematics during reset: {e}")
        
        print("All positions reset to initial values")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                env.close()
                
                # Stop VR monitoring
                if vr_monitor.is_running:
                    asyncio.run(vr_monitor.stop_monitoring())
                return
        
        # Get VR controller data from VRMonitor
        dual_goals = vr_monitor.get_latest_goal_nowait()
        left_goal = dual_goals.get("left") if dual_goals else None
        right_goal = dual_goals.get("right") if dual_goals else None
        headset_goal = dual_goals.get("headset") if dual_goals else None  # 添加头部数据
        
        # Check for VR activity and auto-reset
        current_time = time.time()
        vr_activity_detected = False
        
        # Update target joint positions based on VR controller positions - only after warmup
        if step_counter >= warmup_steps:
            # Process LEFT controller goal
            if left_goal is not None and left_goal.target_position is not None:
                vr_activity_detected = True
                pos = left_goal.target_position
                
                x_vr = (pos[0] + 0.1) * vr_scale_x
                y_vr = (pos[1] - 0.96) * vr_scale_y
                z_vr = (pos[2] + 0.4) * vr_scale_z
                
                # 计算水平距离在垂直平面
                r_distance = math.sqrt(x_vr**2 + z_vr**2)
                
                # 更新左臂末端执行器位置
                ee_pos_arm2[0] = r_distance
                ee_pos_arm2[1] = y_vr
                
                # 计算基于控制器方向的旋转角度
                if abs(x_vr) > 0.05 or abs(z_vr) > 0.05:  # 小死区
                    rotation_angle = math.atan2(x_vr, z_vr)
                    target_joints[7] = rotation_angle  # 缩放因子调整灵敏度

                if left_goal.wrist_flex_deg is not None:
                    pitch_2 = (left_goal.wrist_flex_deg + 60) * 0.02
                
                if left_goal.wrist_roll_deg is not None:
                    target_joints[11] = -(left_goal.wrist_roll_deg-90) * 0.02
                
                if left_goal.metadata.get('trigger', 0) > 0.5:
                    target_joints[13] = 0.1  # Open
                else:
                    target_joints[13] = 2.5
            
                thumb1 = left_goal.metadata.get('thumbstick', {})
                if thumb1:
                    thumb_x1 = thumb1.get('x', 0)
                    thumb_y1 = thumb1.get('y', 0)
                    if abs(thumb_x1) > 0.1 or abs(thumb_y1) > 0.1:  # Only print when thumbstick is significantly moved
                        print(f"Left thumbstick: x={thumb_x1:.2f}, y={thumb_y1:.2f}")
                        action[0] = -thumb_y1 * 0.1
                        # 更新base旋转角并限制在-2π到2π范围内
                        target_joints[1] -= thumb_x1 * 0.02
                        target_joints[1] = max(-2 * math.pi, min(2 * math.pi, target_joints[1]))
                    else:
                        action[0] = 0.0
                    
            
            # Process RIGHT controller goal
            if right_goal is not None and right_goal.target_position is not None:
                vr_activity_detected = True
                pos = right_goal.target_position           
                
                # 绝对位置控制：直接使用VR位置
                x_vr = (pos[0] - 0.1) * vr_scale_x
                y_vr = (pos[1] - 0.96) * vr_scale_y
                z_vr = (pos[2] + 0.4) * vr_scale_z
                 
                # 计算水平距离在垂直平面
                r_distance = math.sqrt(x_vr**2 + z_vr**2)
                
                # 更新右臂末端执行器位置
                ee_pos_arm1[0] = r_distance
                ee_pos_arm1[1] = y_vr
                
                # 计算基于控制器方向的旋转角度
                if abs(x_vr) > 0.05 or abs(z_vr) > 0.05:  # 小死区
                    rotation_angle = math.atan2(x_vr, z_vr)
                    target_joints[2] = rotation_angle # 缩放因子调整灵敏度
                
                if right_goal.wrist_flex_deg is not None:
                    pitch_1 = (right_goal.wrist_flex_deg + 60) * 0.02
                
                if right_goal.wrist_roll_deg is not None:
                    target_joints[6] = -(right_goal.wrist_roll_deg-90) * 0.02

                if right_goal.metadata.get('trigger', 0) > 0.5:
                    target_joints[12] = 0.1  # Open
                else:
                    target_joints[12] = 2.5

                thumb2 = right_goal.metadata.get('thumbstick', {})
                if thumb2:
                    thumb_x2 = thumb2.get('x', 0)
                    thumb_y2 = thumb2.get('y', 0)
                    if abs(thumb_x2) > 0.1 or abs(thumb_y2) > 0.1:  # Only print when thumbstick is significantly moved
                        print(f"Right thumbstick: x={thumb_x2:.2f}, y={thumb_y2:.2f}")
                        target_joints[14] = -thumb_x2 * 0.15
                        target_joints[15] = thumb_y2 * 0.15
                    else:
                        target_joints[14] = 0.0
                        target_joints[15] = 0.0

            
            # if headset_goal is not None:
            #     target_joints[14] = headset_goal.wrist_roll_deg * 0.01
            #     target_joints[15] = -headset_goal.wrist_flex_deg * 0.01
            
            # Calculate inverse kinematics for both arms
            try:
                # First arm
                compensated_y1 = ee_pos_arm1[1] + tip_length * math.sin(pitch_1)
                target_joints[3], target_joints[4] = inverse_kinematics(ee_pos_arm1[0], compensated_y1)
                # Apply pitch adjustment to joint 5 based on joints 3 and 4
                target_joints[5] = target_joints[3] - target_joints[4] + pitch_1
                
                # Second arm
                compensated_y2 = ee_pos_arm2[1] + tip_length * math.sin(pitch_2)
                target_joints[8], target_joints[9] = inverse_kinematics(ee_pos_arm2[0], compensated_y2)
                # Apply pitch adjustment to joint 10 based on joints 8 and 9
                target_joints[10] = target_joints[8] - target_joints[9] + pitch_2
            except Exception as e:
                print(f"Error calculating inverse kinematics: {e}")
        
        # Get current joint positions using our mapping function
        current_joints = get_mapped_joints(robot)
        
        # Simple P controller for arm joints
        if step_counter < warmup_steps:
            action = np.zeros_like(action)
        else:
            # Apply P control to turning (index 1) and arm joints (indices 2-11) and grippers (indices 12-13)
            # Base forward/backward (index 0) is set directly above if using thumbstick
            for i in range(1, len(action)):
                action[i] = p_gain[i] * (target_joints[i] - current_joints[i])
        
        # Clip actions to be within reasonable bound
        
        # Get camera images and send to Rerun if available
        if args.show_cameras and step_counter >= warmup_steps and args.use_rerun and RERUN_AVAILABLE:
            try:
                # Get sensor images
                sensor_images = env.unwrapped.get_sensor_images()
                if args.debug_cameras:
                    print(f"Available sensor images: {list(sensor_images.keys())}")
                
                for camera_name, camera_data in sensor_images.items():
                    if args.debug_cameras:
                        print(f"Processing camera {camera_name}: {list(camera_data.keys())}")
                    
                    for data_type, image_data in camera_data.items():
                        if data_type == "rgb" or data_type == "Color":
                            try:
                                if args.debug_cameras:
                                    print(f"Processing {camera_name}_{data_type}, shape: {image_data.shape}, dtype: {image_data.dtype}")
                                
                                # Convert tensor to numpy
                                image = convert_tensor_to_numpy_image(image_data)
                                
                                # Rotate hand camera images clockwise by 90 degrees
                                if "arm_camera" in camera_name:
                                    # Rotate image clockwise by 90 degrees
                                    image = np.rot90(image, k=3)
                                
                                # Log to Rerun
                                rr.log(f"cameras/{camera_name}_rgb", rr.Image(image))
                                
                                if args.debug_cameras:
                                    print(f"Successfully logged {camera_name}_rgb to Rerun")
                                    
                            except Exception as e:
                                print(f"Error processing {camera_name}_{data_type}: {e}")
                                continue
                        
                        # Handle depth data for head camera
                        elif data_type == "depth" and camera_name == "fetch_head":
                            try:
                                if args.debug_cameras:
                                    print(f"Processing {camera_name}_{data_type}, shape: {image_data.shape}, dtype: {image_data.dtype}")
                                
                                # Convert tensor to numpy
                                depth_image = convert_tensor_to_numpy_image(image_data)
                                
                                # Normalize depth to 0-255 range for visualization
                                if depth_image.max() > 0:
                                    # Normalize to 0-1 range, then scale to 0-255
                                    depth_normalized = (depth_image - depth_image.min()) / (depth_image.max() - depth_image.min())
                                    depth_visualized = (depth_normalized * 255).astype(np.uint8)
                                else:
                                    depth_visualized = np.zeros_like(depth_image, dtype=np.uint8)
                                
                                # Convert to RGB for display (repeat the same value for all channels)
                                if depth_visualized.ndim == 3 and depth_visualized.shape[2] == 1:
                                    depth_rgb = np.repeat(depth_visualized, 3, axis=2)
                                else:
                                    depth_rgb = depth_visualized
                                
                                # Log to Rerun
                                rr.log(f"cameras/{camera_name}_depth", rr.Image(depth_rgb))
                                
                                if args.debug_cameras:
                                    print(f"Successfully logged {camera_name}_depth to Rerun")
                                    
                            except Exception as e:
                                print(f"Error processing {camera_name}_{data_type}: {e}")
                                continue
                
                # Also get human render camera images
                try:
                    render_images = env.unwrapped.render_rgb_array()
                    if args.debug_cameras:
                        print(f"Render images type: {type(render_images)}")
                        if render_images is not None:
                            if isinstance(render_images, dict):
                                print(f"Render cameras: {list(render_images.keys())}")
                            else:
                                print(f"Single render image shape: {render_images.shape}")
                    
                    if render_images is not None:
                        if isinstance(render_images, dict):
                            for camera_name, image_data in render_images.items():
                                try:
                                    if args.debug_cameras:
                                        print(f"Processing render_{camera_name}, shape: {image_data.shape}, dtype: {image_data.dtype}")
                                    
                                    image = convert_tensor_to_numpy_image(image_data)
                                    
                                    # Rotate hand camera images clockwise by 90 degrees
                                    if "arm_camera" in camera_name:
                                        # Rotate image clockwise by 90 degrees
                                        image = np.rot90(image, k=3)
                                    
                                    # Log to Rerun
                                    rr.log(f"cameras/render_{camera_name}", rr.Image(image))
                                    
                                    if args.debug_cameras:
                                        print(f"Successfully logged render_{camera_name} to Rerun")
                                        
                                except Exception as e:
                                    print(f"Error processing render_{camera_name}: {e}")
                                    continue
                        else:
                            # Single image
                            try:
                                if args.debug_cameras:
                                    print(f"Processing render_main, shape: {render_images.shape}, dtype: {render_images.dtype}")
                                
                                image = convert_tensor_to_numpy_image(render_images)
                                
                                # Note: render_main is not a hand camera, so no rotation needed
                                
                                # Log to Rerun
                                rr.log("cameras/render_main", rr.Image(image))
                                
                                if args.debug_cameras:
                                    print(f"Successfully logged render_main to Rerun")
                                    
                            except Exception as e:
                                print(f"Error processing render_main: {e}")
                except Exception as e:
                    print(f"Error getting render images: {e}")
                        
            except Exception as e:
                print(f"Error getting camera images: {e}")
        
        screen.fill((0, 0, 0))
        
        # Display VR Control Status
        text = font.render("VR Control Status:", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        # Add warmup status to display
        if step_counter < warmup_steps:
            warmup_text = font.render(f"WARMUP: {step_counter}/{warmup_steps} steps", True, (255, 0, 0))
            screen.blit(warmup_text, (300, 10))
        
        y_pos = 40
        
        # Display VR Connection Status
        connection_text = font.render("VR Connection:", True, (255, 255, 255))
        screen.blit(connection_text, (10, y_pos))
        y_pos += 25
        
        left_status = "CONNECTED" if left_goal is not None else "DISCONNECTED"
        right_status = "CONNECTED" if right_goal is not None else "DISCONNECTED"
        
        left_status_color = (0, 255, 0) if left_goal is not None else (255, 0, 0)
        right_status_color = (0, 255, 0) if right_goal is not None else (255, 0, 0)
        
        left_status_text = font.render(f"Left Controller: {left_status}", True, left_status_color)
        screen.blit(left_status_text, (20, y_pos))
        y_pos += 25
        
        right_status_text = font.render(f"Right Controller: {right_status}", True, right_status_color)
        screen.blit(right_status_text, (20, y_pos))
        y_pos += 25
        
        # Add headset status
        headset_status = "CONNECTED" if headset_goal is not None else "DISCONNECTED"
        headset_status_color = (0, 255, 0) if headset_goal is not None else (255, 0, 0)
        headset_status_text = font.render(f"Headset: {headset_status}", True, headset_status_color)
        screen.blit(headset_status_text, (20, y_pos))
        y_pos += 35
        
        # Display VR Controller Data
        if left_goal is not None:
            # Left Controller Data
            left_title = font.render("LEFT CONTROLLER:", True, (255, 255, 0))
            screen.blit(left_title, (10, y_pos))
            y_pos += 25
            
            if left_goal.target_position is not None:
                pos = left_goal.target_position
                pos_text = font.render(f"Position: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]", True, (255, 255, 255))
                screen.blit(pos_text, (20, y_pos))
                y_pos += 25
            
            if left_goal.wrist_roll_deg is not None:
                roll_text = font.render(f"Wrist Roll: {left_goal.wrist_roll_deg:.1f}°", True, (255, 255, 255))
                screen.blit(roll_text, (20, y_pos))
                y_pos += 25
            
            if left_goal.wrist_flex_deg is not None:
                flex_text = font.render(f"Wrist Flex: {left_goal.wrist_flex_deg:.1f}°", True, (255, 255, 255))
                screen.blit(flex_text, (20, y_pos))
                y_pos += 25
            
            
            # Add trigger state display
            if hasattr(left_goal, 'metadata') and left_goal.metadata:
                trigger_value = left_goal.metadata.get('trigger', 0)
                trigger_active = trigger_value > 0.5
                trigger_text = font.render(f"Trigger: {trigger_value:.2f} ({'ACTIVE' if trigger_active else 'INACTIVE'})", True, (255, 255, 255))
                screen.blit(trigger_text, (20, y_pos))
                y_pos += 25
                
                # Add thumbstick display
                thumbstick_data = left_goal.metadata.get('thumbstick', {})
                if thumbstick_data:
                    thumb_x = thumbstick_data.get('x', 0)
                    thumb_y = thumbstick_data.get('y', 0)
                    thumbstick_text = font.render(f"Thumbstick: x={thumb_x:.2f}, y={thumb_y:.2f}", True, (255, 255, 255))
                    screen.blit(thumbstick_text, (20, y_pos))
                    y_pos += 25
            
            if left_goal.metadata:
                mode_text = font.render(f"Mode: {left_goal.mode}", True, (255, 255, 255))
                screen.blit(mode_text, (20, y_pos))
                y_pos += 25
                
                is_absolute = left_goal.metadata.get("relative_position", True) == False
                control_type = "ABSOLUTE" if is_absolute else "RELATIVE"
                control_text = font.render(f"Control: {control_type}", True, (255, 255, 255))
                screen.blit(control_text, (20, y_pos))
                y_pos += 35
        
        if right_goal is not None:
            # Right Controller Data
            right_title = font.render("RIGHT CONTROLLER:", True, (255, 255, 0))
            screen.blit(right_title, (10, y_pos))
            y_pos += 25
            
            if right_goal.target_position is not None:
                pos = right_goal.target_position
                pos_text = font.render(f"Position: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]", True, (255, 255, 255))
                screen.blit(pos_text, (20, y_pos))
                y_pos += 25
            
            if right_goal.wrist_roll_deg is not None:
                roll_text = font.render(f"Wrist Roll: {right_goal.wrist_roll_deg:.1f}°", True, (255, 255, 255))
                screen.blit(roll_text, (20, y_pos))
                y_pos += 25
            
            if right_goal.wrist_flex_deg is not None:
                flex_text = font.render(f"Wrist Flex: {right_goal.wrist_flex_deg:.1f}°", True, (255, 255, 255))
                screen.blit(flex_text, (20, y_pos))
                y_pos += 25
            
            
            # Add trigger state display for right controller
            if hasattr(right_goal, 'metadata') and right_goal.metadata:
                trigger_value = right_goal.metadata.get('trigger', 0)
                trigger_active = trigger_value > 0.5
                trigger_text = font.render(f"Trigger: {trigger_value:.2f} ({'ACTIVE' if trigger_active else 'INACTIVE'})", True, (255, 255, 255))
                screen.blit(trigger_text, (20, y_pos))
                y_pos += 25
                
                # Add thumbstick display for right controller
                thumbstick_data = right_goal.metadata.get('thumbstick', {})
                if thumbstick_data:
                    thumb_x = thumbstick_data.get('x', 0)
                    thumb_y = thumbstick_data.get('y', 0)
                    thumbstick_text = font.render(f"Thumbstick: x={thumb_x:.2f}, y={thumb_y:.2f}", True, (255, 255, 255))
                    screen.blit(thumbstick_text, (20, y_pos))
                    y_pos += 25
            
            if right_goal.metadata:
                mode_text = font.render(f"Mode: {right_goal.mode}", True, (255, 255, 255))
                screen.blit(mode_text, (20, y_pos))
                y_pos += 25
                
                is_absolute = right_goal.metadata.get("relative_position", True) == False
                control_type = "ABSOLUTE" if is_absolute else "RELATIVE"
                control_text = font.render(f"Control: {control_type}", True, (255, 255, 255))
                screen.blit(control_text, (20, y_pos))
                y_pos += 35
        
        # Display Headset Data
        if headset_goal is not None:
            # Headset Data
            headset_title = font.render("HEADSET:", True, (255, 255, 0))
            screen.blit(headset_title, (10, y_pos))
            y_pos += 25
            
            if headset_goal.target_position is not None:
                pos = headset_goal.target_position
                pos_text = font.render(f"Position: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]", True, (255, 255, 255))
                screen.blit(pos_text, (20, y_pos))
                y_pos += 25
            
            if headset_goal.wrist_roll_deg is not None:
                roll_text = font.render(f"Head Roll: {headset_goal.wrist_roll_deg:.1f}°", True, (255, 255, 255))
                screen.blit(roll_text, (20, y_pos))
                y_pos += 25
            
            if headset_goal.wrist_flex_deg is not None:
                pitch_text = font.render(f"Head Pitch: {headset_goal.wrist_flex_deg:.1f}°", True, (255, 255, 255))
                screen.blit(pitch_text, (20, y_pos))
                y_pos += 25
            
            if headset_goal.metadata:
                mode_text = font.render(f"Mode: {headset_goal.mode}", True, (255, 255, 255))
                screen.blit(mode_text, (20, y_pos))
                y_pos += 25
                
                is_absolute = headset_goal.metadata.get("relative_position", True) == False
                control_type = "ABSOLUTE" if is_absolute else "RELATIVE"
                control_text = font.render(f"Control: {control_type}", True, (255, 255, 255))
                screen.blit(control_text, (20, y_pos))
                y_pos += 35
        
        # Display Robot Status
        robot_title = font.render("ROBOT STATUS:", True, (255, 255, 0))
        screen.blit(robot_title, (10, y_pos))
        y_pos += 25
        
        # Display end effector positions
        ee1_text = font.render(
            f"Arm 1 End Effector: ({ee_pos_arm1[0]:.3f}, {ee_pos_arm1[1]:.3f})", 
            True, (255, 100, 100)
        )
        screen.blit(ee1_text, (20, y_pos))
        y_pos += 25
        
        ee2_text = font.render(
            f"Arm 2 End Effector: ({ee_pos_arm2[0]:.3f}, {ee_pos_arm2[1]:.3f})", 
            True, (255, 100, 100)
        )
        screen.blit(ee2_text, (20, y_pos))
        y_pos += 35
        
        # Display Gripper States
        gripper_title = font.render("GRIPPER STATES:", True, (255, 255, 0))
        screen.blit(gripper_title, (10, y_pos))
        y_pos += 25
        
        left_gripper_state = "CLOSED" if last_gripper_state_left else "OPEN"
        right_gripper_state = "CLOSED" if last_gripper_state_right else "OPEN"
        
        left_gripper_text = font.render(f"Left Gripper: {left_gripper_state}", True, (255, 255, 255))
        screen.blit(left_gripper_text, (20, y_pos))
        y_pos += 25
        
        right_gripper_text = font.render(f"Right Gripper: {right_gripper_state}", True, (255, 255, 255))
        screen.blit(right_gripper_text, (20, y_pos))
        y_pos += 35
        
        # Display Instructions
        instructions_title = font.render("INSTRUCTIONS:", True, (255, 255, 0))
        screen.blit(instructions_title, (10, y_pos))
        y_pos += 25
        
        instructions = [
            "• Move VR controllers to control robot arms",
            "• Pull trigger to close gripper (trigger > 0.5)",
            "• Release trigger to open gripper",
            "• Use thumbstick for base movement (x/y values)",
            "• Move headset to see rotation data (Roll/Pitch)",
            "• Grip both controllers to reset positions",
            f"• Auto-reset after {auto_reset_timeout}s of inactivity"
        ]
        
        for instruction in instructions:
            inst_text = font.render(instruction, True, (200, 200, 200))
            screen.blit(inst_text, (20, y_pos))
            y_pos += 20
        
        # Display VR Activity Status
        y_pos += 10
        activity_title = font.render("VR ACTIVITY STATUS:", True, (255, 255, 0))
        screen.blit(activity_title, (10, y_pos))
        y_pos += 25
        
        # Show activity status
        activity_status = "ACTIVE" if vr_activity_detected else "INACTIVE"
        activity_color = (0, 255, 0) if vr_activity_detected else (255, 0, 0)
        activity_text = font.render(f"Status: {activity_status}", True, activity_color)
        screen.blit(activity_text, (20, y_pos))
        y_pos += 25
        
        # Show time since last activity
        time_since_activity = current_time - last_vr_activity_time
        time_text = font.render(f"Time since activity: {time_since_activity:.1f}s", True, (255, 255, 255))
        screen.blit(time_text, (20, y_pos))
        y_pos += 25
        
        # Show auto-reset countdown
        if not vr_activity_detected:
            countdown = auto_reset_timeout - time_since_activity
            if countdown > 0:
                countdown_text = font.render(f"Auto-reset in: {countdown:.1f}s", True, (255, 165, 0))
                screen.blit(countdown_text, (20, y_pos))
                y_pos += 25
        
        # Add Rerun status display
        y_pos += 10
        if args.use_rerun and RERUN_AVAILABLE:
            rerun_status = font.render("Rerun: Active - Check Rerun viewer for cameras", True, (0, 255, 0))
            screen.blit(rerun_status, (10, y_pos))
        elif args.use_rerun and not RERUN_AVAILABLE:
            rerun_status = font.render("Rerun: Not available - Install with: pip install rerun-sdk", True, (255, 0, 0))
            screen.blit(rerun_status, (10, y_pos))
        
        pygame.display.flip()
        
        obs, reward, terminated, truncated, info = env.step(action)
        step_counter += 1
        
        if args.render_mode is not None:
            env.render()
        
        time.sleep(0.01)
        
        if args.render_mode is None or args.render_mode != "human":
            if (terminated | truncated).any():
                break
    
    pygame.quit()
    env.close()
    
    # Stop VR monitoring
    if vr_monitor.is_running:
        asyncio.run(vr_monitor.stop_monitoring())

    if record_dir:
        print(f"Saving video to {record_dir}")


if __name__ == "__main__":
    parsed_args = tyro.cli(Args)
    main(parsed_args)
