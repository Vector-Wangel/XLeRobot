### XLeRobot Teleop

### FAQ

- If you are using Ubuntu, be sure to run `sudo chmod 666 /dev/ttyACM0` and `sudo chmod 666 /dev/ttyACM1` after plugging in the motor control board.
- Then run `python lerobot/find_port.py` to check the control board ID. Then change the names correspondingly in
- ![image](https://github.com/user-attachments/assets/19264425-8a67-465f-86ba-3c54ec13793e)
- If you are having error of not detecting any motor after `sudo chmod ...`, try replugging the power cable.
- If you are having error of `need 9 motors, but 8 detected`, you need to switch the port names in the above figure.

### Keyboard Teleop

Complete system control including dual arms, mobile base, and head motors. Run [4_xlerobot_teleop_keyboard.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/4_xlerobot_teleop_keyboard.py) for comprehensive keyboard-based teleoperation of the entire XLeRobot system with separate key mappings for left arm, right arm, base movement, and head control.

### Xbox Controller Teleop

Intuitive gamepad control for the full XLeRobot system. Run [5_xlerobot_teleop_xbox.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/5_xlerobot_teleop_xbox.py) for Xbox controller-based teleoperation with ergonomic stick and trigger mappings for natural human-robot interaction.


<video width="100%" controls>
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/xlerobot_025_001.mp4" type="video/mp4">
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

You can try [controlling XLeRobot with VR in simulation](https://xlerobot.readthedocs.io/en/latest/simulation/getting_started/vr_sim.html) first.

For the real robot, run [8_xlerobot_teleop_vr.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/8_xlerobot_teleop_vr.py). Both arms follow the controllers, the trigger drives the gripper, and the right thumbstick drives the base. There is also a `Teleoperator` subclass at [software/src/teleporators/xlerobot_vr](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/src/teleporators/xlerobot_vr) that follows the `teleop_keyboard` format.

The script starts [XLeVR](https://github.com/Vector-Wangel/XLeRobot/tree/main/XLeVR) inside its own process, so the headset connects to whichever machine runs the example. Four things to set up first:

- put the `XLeVR` directory itself on `PYTHONPATH`, so `from vr_monitor import VRMonitor` resolves
- install `pygame`, `scipy` and `websockets` into the same environment as `lerobot`
- pass `id` and the serial ports to `XLerobotConfig()`. Without `id` the calibration file is looked up as `None.json`, and `connect()` starts the 17-motor interactive calibration instead of restoring the saved one
- regenerate `cert.pem` / `key.pem`. The bundled certificate expired on 2026-06-27 and carries no `subjectAltName`. Deleting them does not help, because the HTTPS server starts before the WebSocket server and is the only one that does not call `ensure_ssl_certificates`

In the headset browser, accept the certificate for **both** `https://<host>:8443` (web UI) and `https://<host>:8442` (WebSocket). `vr_app.js` hardcodes port 8442, and accepting 8443 alone leaves the WebSocket silently unable to connect.

Tested on a real XLeRobot (dual SO-101 arms, head pan-tilt, 3-wheel omni base) driven from a Raspberry Pi 5 with a Quest 3S.
