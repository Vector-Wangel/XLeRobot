# XLeRobot 2-Wheels (Differential Drive)

This is a modified version of XLeRobot that uses a 2-wheel differential drive base instead of the original 3-wheel omni wheel base.

## Key Changes from Original XLeRobot

### Hardware Changes
- **Wheels**: Reduced from 3 omni wheels to 2 differential drive wheels
- **Motor IDs**: 
  - Left wheel: Motor ID 9
  - Right wheel: Motor ID 10
  - Removed: Back wheel (previously Motor ID 8)

### Kinematics Changes
- **Movement**: Only supports forward/backward (x) and rotation (θ)
- **No lateral movement**: Cannot move sideways (y) like the omni wheel version
- **Differential drive equations**:
  - Left wheel speed = (v - ω*L/2) / r
  - Right wheel speed = (v + ω*L/2) / r
  - Where v = linear velocity, ω = angular velocity, L = wheelbase, r = wheel radius

### Configuration Parameters
- `wheel_radius`: 0.05 meters (default)
- `wheelbase`: 0.25 meters (default)
- These can be adjusted in the config files

### Control Interface
- **Forward/Backward**: 'i'/'k' keys
- **Rotate Left/Right**: 'u'/'o' keys
- **Speed Control**: 'n'/'m' keys (3 speed levels)
- **No lateral movement keys**: 'j'/'l' keys removed

## Usage

### Running the Host (on robot hardware)
```bash
python -m lerobot_robot_xlerobot_2wheels.xlerobot_2wheels_host --robot.id=my_xlerobot_2wheels
```

### Running the Teleop Client
```bash
python examples/4_xlerobot_2wheels_teleop_keyboard.py
```

### Direct Connection (no ZMQ)
```python
from lerobot_robot_xlerobot_2wheels import XLerobot2Wheels, XLerobot2WheelsConfig

config = XLerobot2WheelsConfig()
robot = XLerobot2Wheels(config)
robot.connect()
```

## Files Structure

- `xlerobot_2wheels.py`: Main robot class with differential drive kinematics
- `xlerobot_2wheels_client.py`: ZMQ client for remote control
- `xlerobot_2wheels_host.py`: ZMQ host running on robot hardware
- `config_xlerobot_2wheels.py`: Configuration classes
- `__init__.py`: Package initialization

## Key Differences from Original

1. **State Features**: Removed `y.vel` from state features (only `x.vel` and `theta.vel`)
2. **Motor Configuration**: Only 2 base motors instead of 3
3. **Kinematics Functions**: 
   - `_body_to_wheel_raw()`: Implements differential drive forward kinematics
   - `_wheel_raw_to_body()`: Implements differential drive inverse kinematics
4. **Control Interface**: Simplified to only support differential drive movements

## Advantages of Differential Drive

1. **Simpler Hardware**: Only 2 wheels instead of 3
2. **Lower Cost**: Fewer motors and simpler mechanical design
3. **Easier Maintenance**: Less complex wheel system
4. **Better for Indoor**: More suitable for flat indoor environments

## Limitations

1. **No Lateral Movement**: Cannot move sideways without rotating first
2. **Less Maneuverable**: Requires more complex maneuvers for precise positioning
3. **Wheel Slip**: May experience wheel slip on uneven surfaces

## Migration from Original XLeRobot

To migrate from the original 3-wheel version:

1. Update motor IDs in hardware configuration
2. Remove the back wheel motor
3. Update control code to use only forward/backward and rotation commands
4. Adjust movement strategies to account for no lateral movement capability
