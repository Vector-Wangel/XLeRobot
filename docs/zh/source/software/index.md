<!-- THIS IS ALL GENERATED DOCUMENTATION via generate_robot_docs.py. DO NOT MODIFY THIS FILE DIRECTLY. -->

# 软件

## 安装LeRobot 🤗

要安装LeRobot，请按照[官方安装指南](https://huggingface.co/docs/lerobot/installation)

```{note}
建议使用`pip install -e .`以便更方便的文件传输。
```

如果您还没有配置[SO101手臂](https://huggingface.co/docs/lerobot/so101#configure-the-motors)和[其他电机](https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble.html#configure-motors)的电机，请进行配置。


## 移动XLeRobot文件 

打开已安装的lerobot文件夹并：

将我的SO101机器人解析逆运动学求解器移动到/model文件夹
![image](https://github.com/user-attachments/assets/87248f48-b118-470d-8e57-2b7111f054ed)

将xlerobot机器人文件夹移动到/robots文件夹。
![image](https://github.com/user-attachments/assets/335d571a-a14d-4466-b439-8384517f607b)

```{note}
如果您想基于树莓派构建，请在__init__.py中取消注释xlerobot_host和xlerobot_client。
```
将所有示例代码移动到/example文件夹。
![image](https://github.com/user-attachments/assets/f6e89ff4-7361-408a-83c6-d320bb23da98)

## 快速指南

```{note}
如果您之前没有使用过lerobot SO101手臂，建议先测试单臂设置遥操作并先熟悉一段时间。
```

1. **选择控制方法**: 关节控制(示例0)用于基本电机测试，末端执行器控制用于遥操作(示例1 & 6)
2. **高级功能**: 尝试双臂控制(示例2)或基于视觉的控制(示例3)进行更复杂的任务
3. **完整系统**: 使用键盘(示例4)、Xbox控制器(示例5)或Switch Joycon(示例7)进行完整的XLeRobot遥操作

所有示例脚本都位于[`software/examples/`](https://github.com/Vector-Wangel/XLeRobot/tree/main/software/examples)目录中，在正确设置和校准后可以直接运行。某些示例需要额外校准以确保性能。

```{note}
对于XLeRobot的基础版本，您不需要树莓派。只需使用您的笔记本电脑，如果您想使用完整系统，可以将其放在宜家推车中。
```

## SO100/SO101手臂控制示例

### 1. 键盘关节控制

使用直接关节角度操作的最基本控制方法。运行`0_so100_keyboard_joint_control.py`使用键盘输入手动控制各个关节位置。这提供对每个关节运动的直接访问，无需逆运动学计算。

### 2. 键盘末端执行器控制

使用逆运动学在笛卡尔空间中移动末端执行器的高级控制。运行`1_so100_keyboard_ee_control.py`进行直观控制，其中键盘输入控制末端执行器位置(X、Y坐标)而不是单个关节。

<video width="100%" controls>
  <source src="../_static/videos/Real_demos/keyboard_teleop.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### 3. 双臂键盘控制

通过不同串口(/dev/ttyACM0和/dev/ttyACM1)连接的两个SO100手臂的同时控制。运行`2_dual_so100_keyboard_ee_control.py`进行协调的双臂操作，每个手臂有单独的键盘映射。

### 4. 基于视觉的物体跟踪

YOLO驱动的物体检测和跟踪系统。运行`3_so100_yolo_ee_control.py`使机器人能够使用计算机视觉自动跟踪检测到的物体(如瓶子)。此演示无需训练，结合了实时物体检测和末端执行器控制。

您可以查看[Ultralytics官方网站](https://docs.ultralytics.com/models/)以极其简单的方式尝试各种不同的视觉相关模型和应用。

<video width="100%" controls>
  <source src="../_static/videos/Real_demos/yolo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## XLeRobot遥操作

### 常见问题

- 如果您使用Ubuntu，请确保在插入电机控制板后运行`sudo chmod 666 /dev/ttyACM0`和`sudo chmod 666 /dev/ttyACM1`。
- 然后运行`python lerobot/find_port.py`检查控制板ID。然后在以下位置相应更改名称：
- ![image](https://github.com/user-attachments/assets/19264425-8a67-465f-86ba-3c54ec13793e)
- 如果您在`sudo chmod ...`后遇到未检测到任何电机的错误，请尝试重新插入电源线。
- 如果您遇到`需要9个电机，但检测到8个`的错误，您需要更改

### 5. 键盘遥操作

包括双臂、移动底座和头部电机的完整系统控制。运行[4_xlerobot_teleop_keyboard.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/4_xlerobot_teleop_keyboard.py)进行基于键盘的整个XLeRobot系统综合遥操作，左臂、右臂、底座移动和头部控制有单独的按键映射。

### 6. Xbox控制器遥操作  

完整XLeRobot系统的直观游戏手柄控制。运行[5_xlerobot_teleop_xbox.py](https://github.com/Vector-Wangel/XLeRobot/blob/main/software/examples/5_xlerobot_teleop_xbox.py)进行基于Xbox控制器的遥操作，具有人体工学摇杆和扳机映射，实现自然的人机交互。

<video width="100%" controls>
  <source src="../_static/videos/Real_demos/xlerobot_025_001.mp4" type="video/mp4">
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

您可以先尝试[在仿真中用VR控制XLeRobot](https://xlerobot.readthedocs.io/en/latest/simulation/getting_started/vr_sim.html)。真实机器人的VR遥操作官方代码即将推出。

## 强化学习(RL)

您可以先尝试[lerobot-sim2real (by Stone Tao)](https://github.com/StoneT2000/lerobot-sim2real)与Maniskill，或[huggingface官方HIL-SERL教程](https://huggingface.co/docs/lerobot/hilserl)在单SO101手臂上。完整XLeRobot RL的官方代码即将推出。下面的演示显示了[lerobot-sim2real](https://github.com/StoneT2000/lerobot-sim2real)的实现，对摄像头方向和仿真对象分布进行了小幅修改。

<video width="100%" controls>
  <source src="../_static/videos/Real_demos/sim2real_2.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## VLA

您可以先按照[huggingface官方VLA教程](https://huggingface.co/docs/lerobot/smolvla)在单SO101手臂上。完整XLeRobot VLA的官方代码即将推出。

## (可选，未完全测试)基于Lekiwi的主从控制

```{note}
要使用Lekiwi代码测试XLeRobot的单臂版本，您应该拆下与底座不共享同一电机控制板的SO101手臂，将其夹在桌子上并连接到PC作为主导手臂。
```
```{note}
对于移动底座版本，您需要提前准备一个树莓派。
```

按照他们的所有[软件说明](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#b-install-software-on-pi)，这样您就可以：
-  [在树莓派上安装软件](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#b-install-software-on-pi)并设置SSH 
-  [在PC上安装LeRobot](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#c-install-lerobot-on-laptop)
-  [更新配置](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#update-config)
-  [校准](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#e-calibration)

完成这些步骤后，您应该能够[像Lekiwi一样](https://github.com/huggingface/lerobot/blob/main/examples/11_use_lekiwi.md#f-teleoperate)遥操作XLeRobot的基础单臂版本，以复制此演示视频：

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
