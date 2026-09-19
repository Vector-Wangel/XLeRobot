## Updates

This folder holds XLeRobot's robot code, configs, and demo scripts. `src/robots/`
and `src/model/` install into LeRobot as plugins - see
[`plugins/README.md`](plugins/README.md) and
[the install guide](https://xlerobot.readthedocs.io/en/latest/software/getting_started/install.html).

- SO100/SO101 control codes: These codes should be compatible to both SO100 and SO101, even if you just keep the name in the codes as so100. 

  - Keyboard Joint control
  - Keyboard EE control with my own analytical IK
  - Keyboard EE control for dual arm setup with my own analytical IK


- Computer Vision codes
  - simple_so100_yolo_ee_control.py: YOLO for object detection and segmentation, real-time tracking with the hand camera
  - <img width="631" height="475" alt="image" src="https://github.com/user-attachments/assets/ea5398ee-dbf1-4dcb-95a4-e6dea4d2c799" />

Real-time test on YOLO-based control for object tracking:

https://github.com/user-attachments/assets/e0eb4aa5-bce2-404c-b9ed-380a83c852fd

