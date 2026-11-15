## VLA (1) ACT

XLeRobot上的单臂VLA策略实现：

<video width="100%" controls>
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/Act_on_RPi_Xle.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

# XLeRobot的视觉-语言-动作(VLA)训练

本教程将指导您完成训练视觉-语言-动作(VLA)模型以自主控制XLeRobot手臂的过程。作为控制设备，我们将使用VR和leader arm。如果您希望我们添加更多控制设备（如xbox控制器或键盘），请随时提出问题。

## 您将学习什么

1. 如何遥操作和记录XLeRobot的演示数据集
2. 如何训练和评估您的策略
3. 如何使策略有效工作

通过遵循这些步骤，您将能够训练您的XLeRobot使用LeRobot策略（如ACT）自主执行各种家务任务，包括拾取物体、擦拭桌子或整理物品。

---

## 1. 硬件设置和检查

### 1.1 将头部摄像头转到适当的角度

对于VLA数据集收集和推理，您需要保持一致的头部舵机角度——否则策略将无法工作或性能会下降。

此外，确保摄像头完全看到手臂操作区域——例如，如果您的策略从桌子上取物体并将其放入机器人篮子——桌子和篮子都需要完全可见。

您可以手动转动摄像头或使用RoboCrew库中的实用程序（特别是如果您想将VLA策略用作LLM agent工具）——这将为您提供完美的摄像头角度可重复性：

```python
from robocrew.robots.XLeRobot.servo_controls import ServoControler

servo_controler = ServoControler(left_arm_head_usb='/dev/arm_left')
servo_controler.turn_head_to_vla_position()
```

### 1.2 检查摄像头状态

使用LeRobot [cameras](https://huggingface.co/docs/lerobot/cameras)教程验证您的摄像头设置：

```bash
lerobot-find-cameras opencv  # 或使用'realsense'用于Intel RealSense摄像头
```

您应该看到类似这样的输出：

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

XLeRobot有三个摄像头：两个手腕摄像头和一个头部摄像头。确保所有三个都被检测到。

---

## 2.1. 使用Leader Arm记录单臂数据集

通常单臂足以执行您的抓取和放置任务。仅使用单臂意味着使用更少的舵机和摄像头，因此您的模型学习策略会容易得多。如果您的任务足够简单，可以用一只手臂完成——让我们为它训练策略。

将leader arm连接到树莓派或您用于记录数据集的其他计算机。

以下脚本将开始记录：

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

## 2.2. 使用VR记录XLeRobot数据集

对于更复杂的策略，让我们使用VR来激活机器人的双臂和轮子。

```{warning}
VR录制脚本`software/src/record.py`是在XLeRobot改为插件之前，按旧版LeRobot的目录结构编写的，无法在LeRobot 0.6及以后的版本上运行，目前正在移植。以下步骤为之前的流程。
```

在正式合并到LeRobot之前，从XLeRobot复制所需代码到LeRobot：
```bash
cp your_dir/XLeRobot/software/src/record.py your_dir/lerobot/src/lerobot/record.py
cp your_dir/XLeRobot/software/src/teleporators/xlerobot_vr your_dir/lerobot/src/lerobot/teleporators/xlerobot_vr -r
```

### 记录脚本示例

运行以下脚本开始记录：

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

### 重要提示

1. **摄像头配置**：`robot.cameras`参数应与第1.2节的输出匹配。如果遇到摄像头超时错误，请降低FPS（例如，从30降至20）。

2. **VR连接**：在脚本开始时，它将等待VR连接。使用您的VR设备访问终端输出中显示的URL。连接建立后，数据收集将自动开始。

3. **VR控制**：左手控制器有四个功能（练习几次以熟悉）：
   - **重置位置**：将机器人手臂返回到零位置
   - **提前退出**：结束当前episode收集（在完成任务时使用）
   - **删除Episode**：删除当前episode（如果任务失败时使用）
   - **停止记录**：停止数据集记录会话

<p align="center">
  <img src="https://github.com/user-attachments/assets/4b9004d7-6d4c-47c6-9d87-043e2a120bad" width="45%">
  <img src="https://github.com/user-attachments/assets/b2bddd83-1a95-4aee-bbb5-4f13e927f7c7" width="45%">
</p>

---

```{note}
一些提高性能的技巧：

1. **检查丢帧**：查看[这些示例](https://gold-column-7d2.notion.site/Some-examples-for-VLA-dataset-2a2e20e657ad8037aa09d1228a2bf4bf?pvs=73)以了解丢帧的样子。在记录期间监控您的带宽和CPU使用情况。如果出现问题，请相应地优化您的系统。

2. **避免冗余帧**：在任务完成时使用提前退出功能，而不是让脚本继续记录静态机器人数据。

3. **保持场景一致性**：在记录期间避免在摄像头视野中有额外的移动物体或人员。
```
---

## 3. 训练策略

收集数据集后，参考LeRobot [训练教程](https://huggingface.co/docs/lerobot/il_robots#train-a-policy)选择并训练策略。

## 4. 部署模型

测试您训练模型的最简单方法：
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

上面的脚本在您的机器人树莓派上本地运行策略。对于轻量级ACT策略来说这已经足够了，但对于其他更消耗资源的策略，树莓派将无法提供足够的计算能力。

要运行强大的策略（如SmolVLA或PI0,5），我们需要一台带GPU的外部计算机。按照LeRobot [远程推理指南](https://huggingface.co/docs/lerobot/remote_inference)，在您的PC上运行`lerobot-policy-server`，并在XLeRobot上用`lerobot-rollout --inference.type=remote`连接它。这需要LeRobot 0.7；LeRobot 0.6请参考[异步推理指南](https://huggingface.co/docs/lerobot/async)。

在大多数情况下，您希望将VLA策略用作[LLM agent](https://xlerobot.readthedocs.io/en/latest/software/getting_started/LLM_agent.html)的工具，而不是单独使用。RoboCrew库已经在工具中为您提供了异步客户端。在使用之前，请记住在服务器机器上运行策略服务器。RoboCrew会安装LeRobot 0.6.0，因此请在RoboCrew的环境中运行以下命令：

```
python -m lerobot.async_inference.policy_server \
     --host=0.0.0.0 \
     --port=8080
```



