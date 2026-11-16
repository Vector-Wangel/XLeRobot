## VLA (1) ACT

Single arm VLA policy implementation on XLeRobot:

<video width="100%" controls>
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/Act_on_RPi_Xle.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

# Vision-Language-Action (VLA) Training for XLeRobot

This tutorial will guide you through the process of training a Vision-Language-Action (VLA) model to control your XLeRobot arms autonomously. As control devices we will use VR and leader arm. If you want us to add more control devices (as xbox controller or keyboard) feel free to open an issue.

## What You'll Learn

1. How to teleoperate and record demonstration datasets for XLeRobot
2. How to train and evaluate your policy
3. How to make the policy work effectively

By following these steps, you'll be able to train your XLeRobot to autonomously perform various household tasks using LeRobot policies (such as ACT), including picking up objects, wiping tables, or organizing items.

---

## 1. Hardware Setup and Check

### 1.1 Turn the head camera to an appropriate angle

For both VLA dataset collection and inference you need to keep consistent head servos angles - otherwise policy will not work or performance will drop.

Also, ensure the camera fully sees arms operation field - if for example your policy takes object from table and puts it into robot basket - both table and basket need to be fully visible.

You can turn the camera by your hand or use utility from RoboCrew lib (especially if you want to use your VLA policy as LLM agent tool) - this will provide you with a perfect repeatability of the camera angle:

```python
from robocrew.robots.XLeRobot.servo_controls import ServoControler

servo_controler = ServoControler(left_arm_head_usb='/dev/arm_left')
servo_controler.turn_head_to_vla_position()
```

### 1.2 Check Camera Status

Use the LeRobot [cameras](https://huggingface.co/docs/lerobot/cameras) tutorial to verify your camera setup:

```bash
lerobot-find-cameras opencv  # or use 'realsense' for Intel RealSense cameras
```

You should see output similar to this:

```
--- Detected Cameras ---
Camera #0:
  Name: OpenCV Camera @ 0
  Type: OpenCV
  Id: 0
  Backend api: AVFOUNDATION
  Default stream profile:
    Format: 16.0
    Width: 1920
    Height: 1080
    Fps: 15.0
--------------------
(more cameras ...)
```

XLeRobot has three cameras: two wrist cameras and one head camera. Make sure all three are detected.

---

## 2.1. Record Dataset for a Single Arm Using a Leader Arm

Very often the single arm is enough to perform your pick-and-place task. Using single arm only means using less servos and cameras, so it will be much easier for your model to learn the policy. If your task is simple enough to be done with one arm - let's train policy for it.

Connect a leader arm to the Raspberry Pi or other computer you use to record a dataset.

Following script will start recording:

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/right_arm \
  --robot.id=robot_right_arm \
  --robot.cameras="{ head: {type: intelrealsense, serial_number_or_name: 935422072196, width: 640, height: 480, fps: 30, use_depth: True}, right: {type: opencv, index_or_path: '/dev/video6', width: 640, height: 480, fps: 30}}" \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM0 \
  --teleop.id=my_leader_arm \
  --display_data=true \
  --dataset.repo_id=your_huggingface_id/clear_table_single_arm \
  --dataset.num_episodes=50 \
  --dataset.single_task="Clear the table"
```

## 2.2. Record Dataset for XLeRobot with VR

For more complicated policies, let's use VR to activate both robot's arms and wheels.

```{warning}
The VR recording script, `software/src/record.py`, was written for the LeRobot layout before XLeRobot became a set of plugins, and it does not run on LeRobot 0.6 or later. It is being ported. The steps below describe the previous workflow.
```

Before the official merge into LeRobot, copy the required code from XLeRobot to LeRobot:
```bash
cp your_dir/XLeRobot/software/src/record.py your_dir/lerobot/src/lerobot/record.py
cp your_dir/XLeRobot/software/src/teleporators/xlerobot_vr your_dir/lerobot/src/lerobot/teleporators/xlerobot_vr -r
```

### Recording Script Example

Run the following script to start recording:

```bash
python /your_dir/lerobot/src/lerobot/record.py \
  --robot.type=xlerobot \
  --robot.cameras="{ head: {type: intelrealsense, serial_number_or_name: 935422072196, width: 640, height: 480, fps: 30, use_depth: True}, right: {type: opencv, index_or_path: '/dev/video6', width: 640, height: 480, fps: 20}, left: {type: opencv, index_or_path: '/dev/video8', width: 640, height: 480, fps: 20} }" \
  --dataset.repo_id=your_huggingface_id/clear_table \
  --dataset.single_task="Clear the table." \
  --dataset.root=your_dir/clear_table \
  --display_data=true \
  --teleop.type=xlerobot_vr
```

### Important Notes

1. **Camera Configuration**: The `robot.cameras` parameter should match the output from section 1.2. If you encounter camera timeout errors, reduce the FPS (e.g., from 30 to 20).

2. **VR Connection**: At the beginning of the script, it will wait for VR connection. Visit the URL displayed in the terminal output using your VR device. Data collection will start automatically once the connection is established.

3. **VR Controls**: The left-hand controller has four functions (practice several times to become familiar):
   - **Reset Position**: Returns the robot arms to their zero position
   - **Early Exit**: Ends the current episode collection (use when you've completed the task)
   - **Delete Episode**: Deletes the current episode (use if the task failed)
   - **Stop Recording**: Stops the dataset recording session

<p align="center">
  <img src="https://github.com/user-attachments/assets/4b9004d7-6d4c-47c6-9d87-043e2a120bad" width="45%">
  <img src="https://github.com/user-attachments/assets/b2bddd83-1a95-4aee-bbb5-4f13e927f7c7" width="45%">
</p>

---

```{note}
Some tips for a better performance:

1. **Check for Dropped Frames**: Review [these examples](https://gold-column-7d2.notion.site/Some-examples-for-VLA-dataset-2a2e20e657ad8037aa09d1228a2bf4bf?pvs=73) to understand what dropped frames look like. Monitor your bandwidth and CPU usage during recording. If issues occur, optimize your system accordingly.

2. **Avoid Redundant Frames**: Use the early exit function when the task is completed, rather than letting the script continue logging static robot data.

3. **Maintain Scene Consistency**: Avoid having additional moving objects or people in the camera view during recording.
```
---

## 3. Train a Policy

After collecting your datasets, refer to the LeRobot [training tutorial](https://huggingface.co/docs/lerobot/il_robots#train-a-policy) to select and train a policy.

## 4. Deploy a Model

The simplest way to test your trained model:
```bash
lerobot-rollout \
  --strategy.type=base \
  --policy.path=your_huggingface_id/your_policy \
  --robot.type=xlerobot \
  --robot.cameras="{ head: {type: intelrealsense, serial_number_or_name: 935422072196, width: 640, height: 480, fps: 30, use_depth: True}, right: {type: opencv, index_or_path: '/dev/video6', width: 640, height: 480, fps: 20}, left: {type: opencv, index_or_path: '/dev/video8', width: 640, height: 480, fps: 20} }" \
  --task="Clear the table." \
  --duration=60 \
  --display_data=true
```

Script above runs policy locally on your robot's Raspberry. For lightweight ACT policy it's enough, but for other more resource-consuming policies, the Raspberry will not provide enough computation. 

To run powerful policies as SmolVLA or PI0,5 we need an external computer with GPU. Follow the LeRobot [remote inference guide](https://huggingface.co/docs/lerobot/remote_inference) to run `lerobot-policy-server` on your PC and connect `lerobot-rollout --inference.type=remote` on XLeRobot to it. This needs LeRobot 0.7; LeRobot 0.6 uses the [async inference guide](https://huggingface.co/docs/lerobot/async) instead.

In most cases you'll want to use your VLA policy not by itself, but as a tool of the [LLM agent](https://xlerobot.readthedocs.io/en/latest/software/getting_started/LLM_agent.html). RoboCrew lib already provides you with async client in the tool. Before using it, remember to run policy server on the server machine. RoboCrew installs LeRobot 0.6.0, so run this command in RoboCrew's environment:

```
python -m lerobot.async_inference.policy_server \
     --host=0.0.0.0 \
     --port=8080
```



