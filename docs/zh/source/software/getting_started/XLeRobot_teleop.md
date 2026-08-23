### XLeRobot遥操作

### 常见问题

- 如果您使用Ubuntu，请确保在插入电机控制板后运行`sudo chmod 666 /dev/ttyACM0`和`sudo chmod 666 /dev/ttyACM1`。
- 然后运行`python lerobot/find_port.py`检查控制板ID。然后在以下位置相应更改名称：
- ![image](https://github.com/user-attachments/assets/19264425-8a67-465f-86ba-3c54ec13793e)
- 如果您在`sudo chmod ...`后遇到未检测到任何电机的错误，请尝试重新插入电源线。
- 如果您遇到`需要9个电机，但检测到8个`的错误，您需要交换上图两个控制板的ID。

### 5. 键盘遥操作

包括双臂、移动底座和头部电机的完整系统控制。运行[4_xlerobot_teleop_keyboard.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/4_xlerobot_teleop_keyboard.py)进行基于键盘的整个XLeRobot系统综合遥操作，左臂、右臂、底座移动和头部控制有单独的按键映射。

### 6. Xbox控制器遥操作  

完整XLeRobot系统的直观游戏手柄控制。运行[5_xlerobot_teleop_xbox.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/5_xlerobot_teleop_xbox.py)进行基于Xbox控制器的遥操作，具有人体工学摇杆和扳机映射，实现自然的人机交互。

<video width="100%" controls>
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/xlerobot_025_001.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### 7. Switch Joycon遥操作

- Joycon遥操作基于[joycon-robotics (by box2ai)](https://github.com/box2ai-robotics/joycon-robotics)仓库构建。所以首先您需要git clone该仓库并按照其指南安装(包括安装外部包和make install)。然后直接用[我的修改版本](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/joyconrobotics)替换所有代码。

- 根据我自己的经验，建议也运行`sudo apt install joycond`和`sudo systemctl enable --now joycond`以确保更好的蓝牙连接。

- 将您的Joy-Con置于配对模式：按住Joy-Con侧面的小同步按钮(SR和SL按钮之间)，直到指示灯(单点)开始闪烁
- 打开蓝牙设置：转到设置→蓝牙(或从终端使用bluetoothctl)。
  - 在设备列表中查找"Joy-Con (L)"或"Joy-Con (R)"
  - 点击配对每一个，然后您应该看到指示灯(多点)闪烁
  - 然后按下：左：L(上扳机) + 右：R(上扳机)一起，您应该看到两个joycon上只有第一个指示灯亮起，表示连接成功。
- 您可以先运行测试文件`joycon_test_read.py`以确保连接成功。
- 然后您可以运行`6_so100_joycon_ee_control.py`进行单SO101手臂控制(只需要一个joycon)，如以下所示，以及`7_xlerobot_teleop_joycon.py`进行完整的XLeRobot遥操作(这是我在0.3.0演示中用于大部分家务遥操作的内容)。

### 8. VR遥操作

您可以先尝试[在仿真中用VR控制XLeRobot](https://xlerobot.readthedocs.io/en/latest/simulation/getting_started/vr_sim.html)。

真实机器人请运行 [8_xlerobot_teleop_vr.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/8_xlerobot_teleop_vr.py)。双臂跟随手柄，扳机控制夹爪，右摇杆驱动底盘。[software/src/teleporators/xlerobot_vr](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/src/teleporators/xlerobot_vr) 还提供了遵循 `teleop_keyboard` 格式的 `Teleoperator` 子类。

该脚本会在自己的进程内启动 [XLeVR](https://github.com/Vector-Wangel/XLeRobot/tree/main/XLeVR)，因此头显连接的是运行该示例的那台机器。运行前需要准备四点：

- 把 `XLeVR` 目录本身加入 `PYTHONPATH`，否则 `from vr_monitor import VRMonitor` 无法解析
- 在与 `lerobot` 相同的环境中安装 `pygame`、`scipy` 和 `websockets`
- 给 `XLerobotConfig()` 传入 `id` 和串口路径。不传 `id` 时标定文件会被当作 `None.json` 查找，`connect()` 会启动 17 个舵机的交互式标定，而不是恢复已保存的标定
- 重新生成 `cert.pem` / `key.pem`。仓库自带的证书已于 2026-06-27 过期且没有 `subjectAltName`。删除它们也没用，因为 HTTPS 服务器先于 WebSocket 服务器启动，而它并不调用 `ensure_ssl_certificates`

在头显浏览器中需要**分别**信任 `https://<host>:8443`（网页界面）和 `https://<host>:8442`（WebSocket）两个证书。`vr_app.js` 中写死了端口 8442，只信任 8443 会导致 WebSocket 静默连接失败。

已在真实 XLeRobot（双 SO-101 机械臂、云台头部、三轮全向底盘）上验证，由 Raspberry Pi 5 驱动，头显为 Quest 3S。
