<!-- THIS IS ALL GENERATED DOCUMENTATION via generate_robot_docs.py. DO NOT MODIFY THIS FILE DIRECTLY. -->

# Software

## Install LeRobot 🤗

To install LeRobot, follow the [official Installation Guide](https://huggingface.co/docs/lerobot/installation)

```{note}
It's recommended to use `pip install -e .` for a more convenient file transfer.
```

Configure the motors for [SO101 arms](https://huggingface.co/docs/lerobot/so101#configure-the-motors) and [other motors](https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble.html#configure-motors) if you haven't done so.


## Move XLeRobot files 

Open the installed lerobot folder and:

Move my analytical IK solver for SO101 robot to the /model folder
![image](https://github.com/user-attachments/assets/87248f48-b118-470d-8e57-2b7111f054ed)

Move xlerobot robot folder the /robots folder.
![image](https://github.com/user-attachments/assets/335d571a-a14d-4466-b439-8384517f607b)

```{note}
If you want to build based on RaspberryPi, uncomment xlerobot_host and xlerobot_client in __init__.py.
```
Move all the example codes to /example folder.
![image](https://github.com/user-attachments/assets/f6e89ff4-7361-408a-83c6-d320bb23da98)

## Quick Guide

```{note}
If you haven't played with lerobot SO101 Arm before, it's recommended to test single arm setup teleop and play with it for a while first.
```

1. **Choose Control Method**: Joint control (example 0) for basic motor testing, end-effector control for teleop (example 1 & 6)
2. **Advanced Features**: Try dual-arm control (example 2) or vision-based control (example 3) for more complex tasks
3. **Full System**: Use keyboard (example 4), Xbox controller (example 5), or Switch Joycon (example 7) for complete XLeRobot teleop

All example scripts are located in the [`software/examples/`](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/examples) directory and can be run directly after proper setup and calibration. Some examples needs additional calibration to ensure performance.

```{note}
For basic version of XLeRobot, you don't need a RaspberryPi. Just use your laptop and put it in the IKEA cart if you want to use the full system.
```

## SO100/SO101 Arm Examples

### Keyboard Joint Control

The most basic control method using direct joint angle manipulation. Run `0_so100_keyboard_joint_control.py` for manual control of individual joint positions using keyboard inputs. This provides direct access to each joint's movement without inverse kinematics calculations.

### Keyboard End-Effector Control

Advanced control using inverse kinematics to move the end-effector in Cartesian space. Run `1_so100_keyboard_ee_control.py` for intuitive control where keyboard inputs control the end-effector position (X, Y coordinates) rather than individual joints.

<video width="100%" controls>
  <source src="../_static/videos/Real_demos/keyboard_teleop.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Dual-Arm Keyboard Control

Simultaneous control of two SO100 arms connected via different serial ports (/dev/ttyACM0 and /dev/ttyACM1). Run `2_dual_so100_keyboard_ee_control.py` for coordinated dual-arm manipulation with separate keyboard mappings for each arm.

### Vision-based Object Following

YOLO-powered object detection and tracking system. Run `3_so100_yolo_ee_control.py` to enable the robot to automatically follow detected objects (such as bottles) using computer vision. This demo requires no training and combines real-time object detection with end-effector control. 

You can check [Ultralytics official website](https://docs.ultralytics.com/models/) to try all kinds of different Vision-related models and applications in an extremely easy way.

<video width="100%" controls>
  <source src="../_static/videos/Real_demos/yolo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## XLeRobot Teleop

### FAQ

- If you are using Ubuntu, be sure to run `sudo chmod 666 /dev/ttyACM0` and `sudo chmod 666 /dev/ttyACM1` after plugging in the motor control board.
- Then run `python lerobot/find_port.py` to check the control board ID. Then change the names correspondingly in
- ![image](https://github.com/user-attachments/assets/19264425-8a67-465f-86ba-3c54ec13793e)
- If you are having error of not detecting any motor after `sudo chmod ...`, try replugging the power cable.
- If you are having error of `need 9 motors, but 8 detected`, you need to change the 

### Keyboard Teleop

Complete system control including dual arms, mobile base, and head motors. Run [4_xlerobot_teleop_keyboard.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/4_xlerobot_teleop_keyboard.py) for comprehensive keyboard-based teleoperation of the entire XLeRobot system with separate key mappings for left arm, right arm, base movement, and head control.

### Xbox Controller Teleop

Intuitive gamepad control for the full XLeRobot system. Run [5_xlerobot_teleop_xbox.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/5_xlerobot_teleop_xbox.py) for Xbox controller-based teleoperation with ergonomic stick and trigger mappings for natural human-robot interaction.


<video width="100%" controls>
  <source src="../_static/videos/Real_demos/xlerobot_025_001.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Switch Joycon Teleop

- The Joycon teleop is built based the repo [joycon-robotics (by box2ai)](https://github.com/box2ai-robotics/joycon-robotics). So first you need to git clone that repo and install it following its guide (including installing external packages and make install). Then directly replace all the codes with [my modified version](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/joyconrobotics).

- Based on my own experience, it's recommended to also run `sudo apt install joycond` and `sudo systemctl enable --now joycond` to ensure better bluetooth connection. 

- Put your Joy-Con(s) in pairing mode: Hold down the small sync button on the side of the Joy-Con (between SR and SL buttons) until the lights (single dot) start flashing
- Open Bluetooth settings: Go to Settings → Bluetooth (or use bluetoothctl from terminal).
  - Look for "Joy-Con (L)" or "Joy-Con (R)" in the device list
  - Click to pair each one, then you should see the lights (multiple dots) flashing
  - Then press: Left: L (upper trigger) + Right: R (upper trigger) together, and you should see only the first light dot on both joycons is on, meaning the connection is successful.
- You can run the test file `joycon_test_read.py` first to ensure successful connection.
- Then you can run `6_so100_joycon_ee_control.py` for single SO101 arm control (only one joycon needed) as shown below, and `7_xlerobot_teleop_joycon.py` for the complete XLeRobot teleop (this is what I used for most of the teleoping home tasks in the 0.3.0 demo).


### VR Teleop

You can try [controlling XLeRobot with VR in simulation](https://xlerobot.readthedocs.io/en/latest/simulation/getting_started/vr_sim.html) first. The offical code for VR teleop the real robot is coming soon. 

## Reinforcenment Learning (RL)

You can try [lerobot-sim2real (by Stone Tao)](https://github.com/StoneT2000/lerobot-sim2real) with Maniskill, or [huggingface official tutorial on HIL-SERL](https://huggingface.co/docs/lerobot/hilserl) on single SO101 arm first. The offcial code for complete XLeRobot RL is coming soon. The demo below shows the implementation of [lerobot-sim2real](https://github.com/StoneT2000/lerobot-sim2real), with minor changes to the camera direction and sim-object distribution. 


<video width="100%" controls>
  <source src="../_static/videos/Real_demos/sim2real_2.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## VLA

You can follow [huggingface official VLA tutorial](https://huggingface.co/docs/lerobot/smolvla) on single SO101 arm first.  The offcial code for the complete XLeRobot VLA is coming soon.

## (Optional, not fully tested) Leader-follower Control Based-on Lekiwi

```{note}
To test the single-arm version of XLeRobot with Lekiwi codes, you should detach the SO101 arm that doesn't share the same motor control board with the base, clamp it on your table and connect it to your PC to act as the leader arm.
```
```{note}
To run mobile base version of Lekiwi, you need a RaspberryPi in advance.
```

Follow all of their [software instructions](https://huggingface.co/docs/lerobot/lekiwi) so you can:
-  [Setup VNCviewer for RasberryPi](raspberry_pi_setup.md)
-  [Install software on RasberryPi](https://huggingface.co/docs/lerobot/lekiwi#install-software-on-pi) and setup SSH 
-  [Install LeRobot on PC](https://huggingface.co/docs/lerobot/installation)
-  [Update config](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#update-config)
-  [Calibrate](https://huggingface.co/docs/lerobot/il_robots#set-up-and-calibrate)



After these steps you should be able to teleoperate a basic single-arm version of XLeRobot [the same way Lekiwi does](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#f-teleoperate), to replicate this demo video:


<video width="100%" style="max-width: 100%;" controls>
  <source src="https://github.com/user-attachments/assets/98312e30-9a5d-41a1-a6ce-ef163c3abfd5" type="video/mp4">
  Your browser does not support the video tag.
</video>

<!-- ```{toctree}
:caption: Directory
:maxdepth: 1

anymal_c/index
allegro_hand_left/index
allegro_hand_right/index
allegro_hand_right_touch/index
dclaw/index
fetch/index
fixed_inspire_hand_left/index
fixed_inspire_hand_right/index
floating_inspire_hand_left/index
floating_inspire_hand_right/index
floating_panda_gripper/index
floating_robotiq_2f_85_gripper/index
googlerobot/index
humanoid/index
koch-v1.1/index
panda/index
panda_stick/index
panda_wristcam/index
so100/index
stompy/index
trifingerpro/index
ur_10e/index
unitree_g1/index
unitree_g1_simplified_legs/index
unitree_g1_simplified_upper_body/index
unitree_go2/index
unitree_h1/index
unitree_h1_simplified/index
widowx250s/index
widowxai/index
widowxai_wristcam/index
xarm6_nogripper/index
xarm6_robotiq/index
xarm6_robotiq_wristcam/index
xarm7_ability/index

``` -->
