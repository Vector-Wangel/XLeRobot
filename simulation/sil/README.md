# Plugin checks on the simulation

These scripts run the XLeRobot LeRobot plugins against the MuJoCo simulation in `../envhub/`, with no
servos, serial ports or cameras attached. They need LeRobot 0.7 or later, MuJoCo and the plugins:

```bash
pip install "lerobot[feetech]>=0.7" mujoco
pip install -e software/plugins/xlerobot_model -e software/plugins/lerobot_robot_xlerobot  # and the other plugins
python simulation/sil/check_plugin.py --robot xlerobot
```

`virtual_bus.install()` makes LeRobot's `SerialMotorsBus` open a `VirtualServoBus` instead of a
serial port. The virtual bus keeps STS3215 registers and answers them from the simulated robot, so
the plugin's own code runs unchanged:

- handshake;
- calibration restore;
- operating modes and PID registers;
- sync reads and writes.

A servo follows a goal only in the matching operating mode and with its torque on. A plugin that
configures its motors wrongly therefore does not move the simulated robot.

## Running LeRobot commands on the simulation

`run.py` runs any LeRobot command line tool with the same virtual bus. Cameras of type
`xlerobot_sim` render the simulation's camera of the same `name`. For example, a policy rolled out
through the real `xlerobot` plugin:

```bash
python simulation/sil/run.py --sil.height 240 --sil.width 320 lerobot-rollout \
  --strategy.type=base --policy.path=<checkpoint> \
  --robot.type=xlerobot --robot.use_degrees=true --robot.id=sil \
  --robot.cameras="{head: {type: xlerobot_sim, name: head, width: 320, height: 240, fps: 30}, right_wrist: {type: xlerobot_sim, name: right_wrist, width: 320, height: 240, fps: 30}}" \
  --task="Pick up the red cube from the table." --duration=10
```

`run.py` writes a matching calibration unless `--robot.calibration_dir` is given. It answers the
plugin's calibration prompt, and it prints the highest the cube was lifted when the command exits.
Each run resets the cube and joints with the environment's noise; `--sil.seed` picks the draw.

## What the checks cover

`check_plugin.py` reads the virtual servos' registers and the simulated robot, not only what the
plugin reports:

1. **Connect:**
   - arm and head servos are in position mode, and wheels in velocity mode;
   - torque is on and the PID values are written;
   - the calibration is restored to the servos.
2. **Observation:** the plugin reads the simulated joints in degrees.
3. **Arms and head:** position goals reach the simulated joints.
4. **Base** (omniwheel robot): the commanded body velocities move the simulated base backward and
   turn it, through the plugin's wheel kinematics. The plugin also reads the velocity back from the
   wheels.
5. **Grasp** (omniwheel robot): a scripted pick-up through the plugin lifts the cube.
6. **Disconnect:** torque is off.

The dual-wheel and mecanum plugins run checks 1–3 and 6. The simulation has only the omniwheel base.

## Limits

- **What is not simulated:**
  - the servo protocol on the wire, which rustypot encodes;
  - timing and bandwidth of the serial bus;
  - real motor dynamics.
- **LeRobot version:** LeRobot 0.6 drives Feetech servos through `scservo_sdk` rather than
  `SerialMotorsBus`, so these scripts do not run there.
- **Calibration prompt:** the plugin asks on `connect()` whether to restore the calibration file.
  The check answers ENTER.
