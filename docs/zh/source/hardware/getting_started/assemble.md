# ⚒️ 组装

![image](https://github.com/user-attachments/assets/949a670b-a5a2-459d-ab7f-45c51b93afa2)

> 预计组装时间：从零开始：2-4小时；有已组装的SO100/SO101手臂：1-2小时
> 
```{tip}
如果你宁愿跳过拧螺丝的乐趣，你也可以购买SO101手臂的[预组装套件](https://github.com/TheRobotStudio/SO-ARM100#kits)。
```

## 🦾 SO101手臂

![IMG_0264](https://github.com/user-attachments/assets/072d1e5b-f0c3-4bc6-a7cc-5ff38d42565c)

> 如果你已经有2个配置了电机的组装好的SO101手臂，请跳过。
>

- 按照[SO101逐步组装说明](https://huggingface.co/docs/lerobot/so101)构建2个SO101手臂，制作2个相同的跟随手臂，配备2套电机(之前都索引为1-6)用于2个控制板。
- 然后继续为SO101手臂[配置电机](https://huggingface.co/docs/lerobot/so101#configure-the-motors)。
- 按照这个[安装指南](https://github.com/TheRobotStudio/SO-ARM100/tree/main/Optional/SO101_Wrist_Cam_Hex-Nut_Mount_32x32_UVC_Module)添加手腕相机。
- 如果你有[3M抓握胶带](https://www.amazon.com/gp/product/B0093CQPW8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)，现在是时候将其包裹在手指上了。

## 🤔 配置电机

![image](https://github.com/user-attachments/assets/fc674d38-d703-40bd-87a2-a502af1b52c7)

> 由于官方lerobot代码库目前不支持除手臂外的电机配置，我们使用[Bambot](https://bambot.org/)代替(在Windows和Mac上工作，Linux需要先运行'sudo chmod 666 /dev/ttyACM0')。
>

- 将你想要配置的电机(逐个)连接到控制板，并直接将板子连接到你的计算机。
- 导航到[Bambot的电机配置页面](https://bambot.org/feetech.js)，建立连接并扫描你的舵机电机。
  ![image](https://github.com/user-attachments/assets/89eb4674-e26e-4edc-9943-ad5c0d4516ec)

- 按照下面的说明重命名电机id。
  ![image](https://github.com/user-attachments/assets/49d3a1a4-71eb-4d32-9f0a-e8b6026c0b66)

- 除了SO101手臂外，你还需要为2个电机控制板配置两套电机：
    - 一套用于**头部**(电机id：7, 8)
    - 另一套用于**轮式底座**(电机id：7, 8, 9)。
- 提示：用记号笔在电机上写数字，并区分不同板子的电机(如L1-L8和R1-R9)。

## 🛒 宜家推车

- 万一你意外扔掉了手册，[这里有一份](https://github.com/Vector-Wangel/XLeRobot/blob/main/others/Manuals_raskog_utility_cart.pdf)。

<img width="925" alt="1745897734515" src="https://github.com/user-attachments/assets/f9f95840-5080-4084-bebb-ea456a097d55" />

## 🧑‍🦼‍➡ 轮式底座

> 如果你已经有一个Lekiwi底座，请拆下电池、舵机支架等。底板只需安装3个带轮子的电机(保留接线)。
>

![image](https://github.com/user-attachments/assets/4599c9d0-3ce3-40e8-9a8e-d21e1e5feb01)

```{note}
不要选错板子，每个板子都有特定的顺序。
```

- 根据上图将全向轮安装到板子上。
  - 应相应安装特定的电机id。
- 注意全向轮的连接器需要3个M4螺丝。
- 按照[教程](https://github.com/SIGRobotics-UIUC/LeKiwi/blob/main/Assembly.md#2-bottom-plate-assembly)正常接线电机，之后不要将电机线缆连接到控制板，而是使用延长线/连接器套件来延长线缆。

![image](https://github.com/user-attachments/assets/ac4ab4b4-6488-4e07-8349-e4167bf417f6)

- 根据上图安装顶板。
- 让电机线缆悬挂，暂时不要从顶板拉出来。

![image](https://github.com/user-attachments/assets/651c7e03-6bdd-47de-8ab6-f9157ced06fe)

- 根据上图在顶板上安装3个连接器。

```{tip}
将带连接器的Lekiwi底座放在推车下方，看看是否能给推车足够的压力，推车的四个轮子仍能接触地面。如果不能，尝试通过在切片软件中直接稍微调整z轴比例(保持xy轴比例不变)来修改连接器的3D模型并重新打印。
```

![image](https://github.com/user-attachments/assets/c6bd27ec-6a2e-42ea-aee4-bb28079ccaf0)

```{tip}
翻转推车进行下面的组装。
```

- 现在将带连接器的Lekiwi底座安装到宜家推车的底部，较薄的板子在另一侧。
- 参考图片根据电机索引找到所需的组装方向。

```{note}
这个新硬件版本与宜家推车金属网格兼容，所有12个M3螺丝都应该能够轻松装入。
```

![image](https://github.com/user-attachments/assets/7792ee8d-7300-449f-b2bb-a78417dbc56b)

- 使用尖嘴钳在顶部底座的相应孔位切割金属网格，只移除中央的"x"以保持结构完整性。这为线缆布线创建开口。
- 然后，将之前延长的线缆从下方穿过推车向上布线。

## 🦾 手臂底座

### 顶部底座组装
![image](https://github.com/user-attachments/assets/1ea61764-6e4c-4edf-8d0f-0979430a7921)

- 当底座翻转过来时组装更容易。

### 头部组装

![image](https://github.com/user-attachments/assets/e24df68f-6140-456e-aeee-9e51f3c8a9f7)

- 这应该与[SO101手臂组装](https://huggingface.co/docs/lerobot/so101#joint-1)的前两个步骤相同。

## 🧵 接线

```{important}
在将顶部底座夹到宜家推车之前，完成顶部底座的所有接线和线缆管理，并将树莓派放入其外壳中。
```

![image](https://github.com/user-attachments/assets/798eeebf-a64f-4c16-b592-c32c8d9c62df)

- 如果你还没有，请准备带连接器套件的延长5264线缆。
- 使用尖嘴钳为上层两层切割金属网格进行线缆布线，类似于之前的底层。根据需要选择位置。
```{note}
当你自己延长5264线缆时，要小心极性——反向连接会导致错误。
```
- 将来自**Lekiwi底座**的延长5264**电机线缆**连接到**一个SO101手臂**(这使底座和手臂成为Lekiwi)。
- 将2根**USB-C转USB-A****数据线缆**从2个**电机控制板**连接到**树莓派**(剩下2个USB-A插槽用于相机)。
- 连接所有3根**电源线缆**：2根**USB-C转DC(12V)**从2个**电机控制板**和1根**USB-C转USB-C**从**树莓派**，连接到电源的快充部分。每个插槽在同时充电时提供高达100W功率，经测试足以支持12V版本运行。

### 🔋 放置电池 🛒

- 放在推车中层或下层的任何位置以保持低重心。电池有防滑底部，在正常操作中不易滑动。
- 为了安全保持直立放置。
- 万一你也意外扔掉了电池手册，[这里有一份](https://github.com/Vector-Wangel/XLeRobot/blob/main/others/Manual_Anker_SOLIX_C300_DC_Portable_Power_Station.pdf)。

```{important}
为了保护电机控制板，确保最后连接电源线缆。在插拔其他线缆时始终断开电源线缆。
```

## 📸 最终组装

### 底座装入推车

```{important}
在将顶部底座夹到宜家推车之前，完成顶部底座的所有接线和线缆管理，并将树莓派放入其外壳中。
```

![image](https://github.com/user-attachments/assets/2b568626-77c4-4956-a9ab-22db3638eb50)

- 当你将宜家推车边缘塞入外壳插座时要小心不要弄坏外壳。
- 为了更容易测试，SO101手臂直接夹在推车上。将[手臂底座](https://github.com/Vector-Wangel/XLeRobot/blob/main/3D_Models/3D_models_for_printing/XLeRobot_special/SO_5DOF_ARM100_Assemblybases.stl)定位在推车顶层的两个角落，然后用夹子固定。
- 如果你有bambulab耗材纸质线轴，不要忘记将其放在里面以提供稳定的结构支撑。

![image](https://github.com/user-attachments/assets/4efa2b31-627c-4f62-9977-d6a50d8dce0e)

完成这些步骤后，XLeRobot应该在物理上组装良好，准备做一些家务。

![image](https://github.com/user-attachments/assets/4efa2b31-627c-4f62-9977-d6a50d8dce0e)

![image](https://github.com/user-attachments/assets/1d553e6a-dad6-4b17-bc82-e4d6d3e2ecc8)

```{important}
XLeRobot完全组装后，不要像宜家推车那样推着它到处走，因为这可能损坏电机齿轮。相反，当你需要手动移动时，请抬起机器人(~12kg)。
```
```{note}
当前形式的轮连接器不够坚固，偶尔可能需要重新拧紧中心螺丝。
```
### 可选视觉升级

为了更好的视觉效果，如果您喜欢，可以为XLeRobot穿戴这些零件。

![image](https://github.com/user-attachments/assets/91491f62-a466-4421-ac9b-db3492849a89)

- **外壳**用于控制板和第一个关节，提供更好的保护和视觉效果。
  - 在将第二个外壳穿到手臂上之前，您可能需要先取下手部相机。
- 运动袖套用于隐藏线缆，使XLeRobot更加时尚。
  
![image](https://github.com/user-attachments/assets/9847f2a6-f79a-4899-bd20-64a25c709660)



