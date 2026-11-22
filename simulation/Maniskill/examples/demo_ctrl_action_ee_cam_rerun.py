import gymnasium as gym
import numpy as np
import sapien
import pygame
import time
import math
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

        mapped_joints[14] = full_joints[5]
        mapped_joints[15] = full_joints[8]
    
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
        rr.init("mani_skill_camera_demo")
        rr.spawn()
        print("Rerun initialized for camera visualization")
    elif args.use_rerun and not RERUN_AVAILABLE:
        print("Warning: Rerun requested but not available. Install with: pip install rerun-sdk")
    
    # Calculate screen size for control panel only (no camera display)
    control_panel_width = 600
    screen_width = control_panel_width + 20
    screen_height = 750  # Fixed height for control panel
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Control Window - Use keys to move (Cameras in Rerun)")
    font = pygame.font.SysFont(None, 24)
    
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
    target_joints[6] = 1.57  # Set joint 5 for first arm to 1.57
    target_joints[8] = 0.303
    target_joints[9] = 0.556
    target_joints[11] = 1.57  # Set joint 5 for second arm to 1.57

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
    p_gain[0] = 2     # Base forward/backward
    p_gain[1] = 0.5     # Base rotation - lower gain for smoother turning
    p_gain[2:7] = 1.0   # First arm joints
    p_gain[7:12] = 1.0  # Second arm joints
    p_gain[12:14] = 0.05  # Gripper joints
    p_gain[14:16] = 2  # Head motor joints
    
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
    target_joints[6] = 1.57 
    target_joints[11] = 1.57 
    
    # Set initial joint positions based on inverse kinematics from initial end effector positions
    try:
        target_joints[3], target_joints[4] = inverse_kinematics(ee_pos_arm1[0], ee_pos_arm1[1])
        target_joints[8], target_joints[9] = inverse_kinematics(ee_pos_arm2[0], ee_pos_arm2[1])
    except Exception as e:
        print(f"Error calculating initial inverse kinematics: {e}")
    
    # Add step counter for warmup phase
    step_counter = 0
    warmup_steps = 50
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                env.close()
                return
            elif event.type == pygame.KEYDOWN:
                # Reset all positions when 'x' is pressed (changed from 'r' since 'r' is now used for head control)
                if event.key == pygame.K_x:
                    # Reset end effector positions
                    ee_pos_arm1 = initial_ee_pos_arm1.copy()
                    ee_pos_arm2 = initial_ee_pos_arm2.copy()
                    
                    # Reset pitch adjustments
                    pitch_1 = initial_pitch_1
                    pitch_2 = initial_pitch_2
                    
                    # Reset target joints
                    target_joints = np.zeros_like(target_joints)
                    
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
            
            # # Handle base rotation wraparound - if rotation falls below -π, add 2π
            # if target_joints[1] < -math.pi*1.01:
            #     target_joints[1] += 2 * math.pi
            # # If rotation exceeds π, subtract 2π
            # elif target_joints[1] > math.pi*1.01:
            #     target_joints[1] -= 2 * math.pi
            
            # Arm control - using end effector positions and inverse kinematics
            # First arm end effector control
            if keys[pygame.K_8]:  # Move end effector up
                ee_pos_arm1[1] += ee_step
                ee_changed_arm1 = True
            if keys[pygame.K_u]:  # Move end effector down
                ee_pos_arm1[1] -= ee_step
                ee_changed_arm1 = True
            if keys[pygame.K_9]:  # Move end effector forward
                ee_pos_arm1[0] += ee_step
                ee_changed_arm1 = True
            if keys[pygame.K_i]:  # Move end effector backward
                ee_pos_arm1[0] -= ee_step
                ee_changed_arm1 = True
                
            # Calculate inverse kinematics for first arm if end effector position changed
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
                ee_changed_arm2 = True
            if keys[pygame.K_m]:  # Move end effector down
                ee_pos_arm2[1] -= ee_step
                ee_changed_arm2 = True
            if keys[pygame.K_k]:  # Move end effector forward
                ee_pos_arm2[0] += ee_step
                ee_changed_arm2 = True
            if keys[pygame.K_COMMA]:  # Move end effector backward
                ee_pos_arm2[0] -= ee_step
                ee_changed_arm2 = True
                
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
                # Toggle first gripper (index 12)
                if target_joints[12] < 0.4:  # If closed or partially closed
                    target_joints[12] = 2.5  # Open
                else:
                    target_joints[12] = 0.1  # Close
                # Add a small delay to prevent multiple toggles
                pygame.time.delay(200)
                
            if keys[pygame.K_b]:
                # Toggle second gripper (index 13)
                if target_joints[13] < 0.4:  # If closed or partially closed
                    target_joints[13] = 2.5  # Open
                else:
                    target_joints[13] = 0.1  # Close
                # Add a small delay to prevent multiple toggles
                pygame.time.delay(200)
            
            # Head motor control - set target positions
            if keys[pygame.K_r]:
                # Control first head motor (index 14) - increase target position
                target_joints[14] += joint_step*2
            if keys[pygame.K_t]:
                # Control first head motor (index 14) - decrease target position
                target_joints[14] -= joint_step*2
            if keys[pygame.K_f]:
                # Control second head motor (index 15) - increase target position
                target_joints[15] += joint_step*2
            if keys[pygame.K_g]:
                # Control second head motor (index 15) - decrease target position
                target_joints[15] -= joint_step*2
        
        # Get current joint positions using our mapping function
        current_joints = get_mapped_joints(robot)
        
        # # Handle base rotation wraparound for current joints too
        # if current_joints[1] < -math.pi:
        #     current_joints[1] += 2 * math.pi
        # elif current_joints[1] > math.pi:
        #     current_joints[1] -= 2 * math.pi
        
        # Simple P controller for arm joints only (not base)
        if step_counter < warmup_steps:
            action = np.zeros_like(action)
        else:
            # Apply P control to turning (index 1) and arm joints (indices 2-11) and grippers (indices 12-13)
            # Base forward/backward (index 0) is already set directly above
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
        
        # Draw control panel
        control_panel_x = 10
        text = font.render("Controls:", True, (255, 255, 255))
        screen.blit(text, (control_panel_x + 10, 10))
        
        # Add warmup status to display
        if step_counter < warmup_steps:
            warmup_text = font.render(f"WARMUP: {step_counter}/{warmup_steps} steps", True, (255, 0, 0))
            screen.blit(warmup_text, (control_panel_x + 300, 10))
        
        control_texts = [
            "W/S: joint[0] (+/-)",
            "A/D: joint[1] (+/-)",
            "Y/7: joint[2] (+/-)",
            "8/U: EE1 Y (+/-)",
            "9/I: EE1 X (+/-)",
            "0/P: joint[5] (+/-)",
            "-/[: joint[6] (+/-)",
            "H/N: joint[7] (+/-)",
            "J/M: EE2 Y (+/-)",
            "K/,: EE2 X (+/-)",
            "L/.: joint[10] (+/-)",
            ";/?: joint[11] (+/-)",
            "R/T: Head1 (+/-)",
            "F/G: Head2 (+/-)",
            "V/B: Toggle grippers",
            "X: Reset all positions"
        ]
        
        col_height = len(control_texts) // 2 + len(control_texts) % 2
        for i, txt in enumerate(control_texts):
            col = 0 if i < col_height else 1
            row = i if i < col_height else i - col_height
            ctrl_text = font.render(txt, True, (255, 255, 255))
            screen.blit(ctrl_text, (control_panel_x + 10 + col * 200, 40 + row * 25))
        
        # Display full joints (before mapping)
        y_pos = 40 + col_height * 30 + 10
        
        # Get full joint positions
        full_joints = robot.get_qpos() if robot is not None else np.zeros(17)
        
        # Convert tensor to numpy array if needed
        if hasattr(full_joints, 'numpy'):
            full_joints = full_joints.numpy()
        
        # Handle case where it's a 2D tensor/array
        if full_joints.ndim > 1:
            full_joints = full_joints.squeeze()
            
        # Display full joints in two rows
        full_joints_text1 = font.render(
            f"Full Joints (1-8): {np.round(full_joints[:8], 2)}", 
            True, (255, 150, 0)
        )
        screen.blit(full_joints_text1, (control_panel_x + 10, y_pos))
        y_pos += 25
        
        full_joints_text2 = font.render(
            f"Full Joints (9-17): {np.round(full_joints[8:], 2)}", 
            True, (255, 150, 0)
        )
        screen.blit(full_joints_text2, (control_panel_x + 10, y_pos))
        y_pos += 30
        
        # Display current joint positions in three logical groups
        # Group 1: Base control [0,1]
        base_joints = current_joints[0:2]
        base_text = font.render(
            f"Base [0,1]: {np.round(base_joints, 2)}", 
            True, (255, 255, 0)
        )
        screen.blit(base_text, (control_panel_x + 10, y_pos))
        
        # Group 2: First arm [2,3,4,5,6]
        y_pos += 25
        arm1_joints = current_joints[2:7]
        arm1_text = font.render(
            f"Arm 1 [2,3,4,5,6]: {np.round(arm1_joints, 2)}", 
            True, (255, 255, 0)
        )
        screen.blit(arm1_text, (control_panel_x + 10, y_pos))
        
        # Group 3: Second arm [7,8,9,10,11]
        y_pos += 25
        arm2_joints = current_joints[7:12]
        arm2_text = font.render(
            f"Arm 2 [7,8,9,10,11]: {np.round(arm2_joints, 2)}", 
            True, (255, 255, 0)
        )
        screen.blit(arm2_text, (control_panel_x + 10, y_pos))
        
        # Display target joint positions in three logical groups
        y_pos += 35
        
        # Group 1: Base control [0,1]
        base_targets = target_joints[0:2]
        base_target_text = font.render(
            f"Base Target [0,1]: {np.round(base_targets, 2)}", 
            True, (0, 255, 0)
        )
        screen.blit(base_target_text, (control_panel_x + 10, y_pos))
        
        # Group 2: First arm [2,3,4,5,6]
        y_pos += 25
        arm1_targets = target_joints[2:7]
        arm1_target_text = font.render(
            f"Arm 1 Target [2,3,4,5,6]: {np.round(arm1_targets, 2)}", 
            True, (0, 255, 0)
        )
        screen.blit(arm1_target_text, (control_panel_x + 10, y_pos))
        
        # Group 3: Second arm [7,8,9,10,11]
        y_pos += 25
        arm2_targets = target_joints[7:12]
        arm2_target_text = font.render(
            f"Arm 2 Target [7,8,9,10,11]: {np.round(arm2_targets, 2)}", 
            True, (0, 255, 0)
        )
        screen.blit(arm2_target_text, (control_panel_x + 10, y_pos))
        
        # Group 4: Grippers [12,13]
        y_pos += 25
        gripper_targets = target_joints[12:14]
        gripper_target_text = font.render(
            f"Grippers Target [12,13]: {np.round(gripper_targets, 2)}", 
            True, (0, 255, 0)
        )
        screen.blit(gripper_target_text, (control_panel_x + 10, y_pos))
        
        # Group 5: Head motors [14,15]
        y_pos += 25
        head_targets = target_joints[14:16]
        head_target_text = font.render(
            f"Head Motors Target [14,15]: {np.round(head_targets, 2)}", 
            True, (0, 255, 0)
        )
        screen.blit(head_target_text, (control_panel_x + 10, y_pos))
        
        # Display end effector positions
        y_pos += 35
        ee1_text = font.render(
            f"Arm 1 End Effector: ({ee_pos_arm1[0]:.3f}, {ee_pos_arm1[1]:.3f}) [Comp Y: {ee_pos_arm1[1] - tip_length * math.sin(pitch_1):.3f}]", 
            True, (255, 100, 100)
        )
        screen.blit(ee1_text, (control_panel_x + 10, y_pos))
        
        y_pos += 25
        ee2_text = font.render(
            f"Arm 2 End Effector: ({ee_pos_arm2[0]:.3f}, {ee_pos_arm2[1]:.3f}) [Comp Y: {ee_pos_arm2[1] - tip_length * math.sin(pitch_2):.3f}]", 
            True, (255, 100, 100)
        )
        screen.blit(ee2_text, (control_panel_x + 10, y_pos))
        
        # Display current action values (velocities) in three logical groups
        y_pos += 35
        
        # Group 1: Base control [0,1]
        base_actions = action[0:2]
        base_action_text = font.render(
            f"Base Velocity [0,1]: {np.round(base_actions, 2)}", 
            True, (255, 255, 255)
        )
        screen.blit(base_action_text, (control_panel_x + 10, y_pos))
        
        # Group 2: First arm [2,3,4,5,6]
        y_pos += 25
        arm1_actions = action[2:7]
        arm1_action_text = font.render(
            f"Arm 1 Velocity [2,3,4,5,6]: {np.round(arm1_actions, 2)}", 
            True, (255, 255, 255)
        )
        screen.blit(arm1_action_text, (control_panel_x + 10, y_pos))
        
        # Group 3: Second arm [7,8,9,10,11]
        y_pos += 25
        arm2_actions = action[7:12]
        arm2_action_text = font.render(
            f"Arm 2 Velocity [7,8,9,10,11]: {np.round(arm2_actions, 2)}", 
            True, (255, 255, 255)
        )
        screen.blit(arm2_action_text, (control_panel_x + 10, y_pos))
        
        # Group 4: Grippers [12,13]
        y_pos += 25
        gripper_actions = action[12:14]
        gripper_action_text = font.render(
            f"Grippers Velocity [12,13]: {np.round(gripper_actions, 2)}", 
            True, (255, 255, 255)
        )
        screen.blit(gripper_action_text, (control_panel_x + 10, y_pos))
        
        # Group 5: Head motors [12,13]
        y_pos += 25
        head_actions = action[14:16]
        head_action_text = font.render(
            f"Head Motors Velocity [14,15]: {np.round(head_actions, 2)}", 
            True, (255, 255, 255)
        )
        screen.blit(head_action_text, (control_panel_x + 10, y_pos))
        
        # Display pitch adjustments
        y_pos += 35
        pitch_text = font.render(
            f"Pitch Adjustments: Arm1={pitch_1:.3f} (O/0), Arm2={pitch_2:.3f} (./L)", 
            True, (255, 100, 255)
        )
        screen.blit(pitch_text, (control_panel_x + 10, y_pos))
        
        # Add Rerun status display
        if args.use_rerun and RERUN_AVAILABLE:
            rerun_status = font.render("Rerun: Active - Check Rerun viewer for cameras", True, (0, 255, 0))
            screen.blit(rerun_status, (control_panel_x + 10, y_pos + 25))
        elif args.use_rerun and not RERUN_AVAILABLE:
            rerun_status = font.render("Rerun: Not available - Install with: pip install rerun-sdk", True, (255, 0, 0))
            screen.blit(rerun_status, (control_panel_x + 10, y_pos + 25))
        
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

    if record_dir:
        print(f"Saving video to {record_dir}")


if __name__ == "__main__":
    parsed_args = tyro.cli(Args)
    main(parsed_args)
