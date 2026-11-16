# XLeRobot

::::{container} xl-hero
:::{container} xl-hero-subtitle
开源家用双臂移动机器人
:::

:::{container} xl-hero-tagline
让具身AI走向全世界每位开发者！
:::

:::{container} xl-cta
[开始组装](hardware/index.md) [在线仿真](simulation/index.md) <a href="#film">观看视频</a> [在 GitHub 上查看](https://github.com/Vector-Wangel/XLeRobot)
:::

:::{container} xl-badges
[![GitHub](https://img.shields.io/badge/GitHub-XLeRobot-181717?logo=github&style=flat)](https://github.com/Vector-Wangel/XLeRobot) [![Stars](https://img.shields.io/github/stars/Vector-Wangel/XLeRobot?style=social)](https://github.com/Vector-Wangel/XLeRobot) [![Twitter/X](https://img.shields.io/twitter/follow/VectorWang?style=social)](https://twitter.com/VectorWang2) [![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Discord](https://img.shields.io/badge/Discord-Join%20Chat-7289da.svg?logo=discord&logoColor=white)](https://discord.gg/bjZveEUh6F)
:::

:::{container} xl-hero-media
![XLeRobot：开源家用双臂移动机器人，660美元，4小时组装](https://github.com/user-attachments/assets/f9c454ee-2c46-42b4-a5d7-88834a1c95ab)
:::

:::{container} xl-hero-credits
*站在巨人的肩膀上: [LeRobot](https://github.com/huggingface/lerobot), [SO-100/SO-101](https://github.com/TheRobotStudio/SO-ARM100), [Lekiwi](https://github.com/SIGRobotics-UIUC/LeKiwi), [Bambot](https://github.com/timqian/bambot)*
:::
::::

```{xl-stats}
- value: "~¥3999"
  label: 基础版总成本
- value: "<4 小时"
  label: 总组装时间
- value: "~12 kg"
  label: 成年人可轻松搬动
- value: "10 小时+"
  label: 一次充电正常运行
```

<div class="xl-film" id="film">
<video controls playsinline preload="metadata">
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/xlerobot030.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
</div>

## 为什么选择XLeRobot？

:::{container} xl-lead
**XLeRobot = XL + LeRobot**
:::

```{xl-compose}
groups:
  - eyebrow: 核心
    title: LeRobot
    items:
      - icon: hand
        label: 2× SO-100/SO-101 手臂
        note: 90% 3D打印，电机经济实惠
      - icon: code
        label: LeRobot 软件
        note: pip 安装，几行代码即可运行
      - icon: users
        label: LeRobot 社区
        note: 最先进的模型、数据集和工具
  - eyebrow: 增强
    title: XL
    items:
      - icon: cart-flatbed
        label: 宜家 RÅSKOG 推车
        note: 结实、全球有售、家用高度
      - icon: circle-dot
        label: 全向轮底座
        note: 可直接从 Lekiwi 升级
      - icon: battery-full
        label: Anker SOLIX C300
        note: 288Wh，USB-C 为全部设备供电
      - icon: camera
        label: 头部摄像头
        note: RGB、双目或 RealSense
result:
  eyebrow: 结果
  title: XLeRobot
  text: 实用的低成本家用双臂移动机器人。
  chips: ["~¥3999", "<4 小时组装", "~12 kg"]
```

<div class="xl-spacer"></div>

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 为什么选择"LeRobot"核心？
:class-card: xl-card

- **廉价材料** 💴: 90%的3D打印组件，配合经济实惠的电机和电子元件。
- **简易组装** 🔨: 67分钟即可组装2个SO101手臂并配置电机。
- **即插即用** 🧩: 通过简单的pip安装和几行代码让机器人运行起来。
- **蓬勃发展的LeRobot社区** 🌍:
世界上最大的低成本机器人社区，特色包括
    - 多个[最先进的预训练AI模型🧠](https://huggingface.co/lerobot)、数据集📊和工具🔨，随时可以部署。
    - 7000+聪明才智的头脑进行头脑风暴和讨论🧑‍🤝‍🧑。
:::

:::{grid-item-card} 为什么需要"XL"增强？
:class-card: xl-card

![image](https://github.com/user-attachments/assets/b48a0a41-7422-4f10-8dc6-a66a2fd746ad)

- 🏠 该领域/市场缺乏价格合理、稳定的双臂家用机器人，能够与LeRobot的简易组装相匹配。
- 🖨️ 传统3D打印底盘耐久性、稳定性和负载能力有限——使其不适合日常使用。
- ⚡ DIY移动机器人面临电源供应挑战，导致复杂的接线设置。
:::
::::

:::{container} xl-subhead
整体优势
:::

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">💴</span>

**经济实惠**: 完整构建成本4000￥，或者从现有SO101Arm和Lekiwi升级仅需不到1500￥。
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">⏫</span>

**轻松升级** 从**Lekiwi**和**SO-100/SO-101**
- 硬件：无需更改电机ID或硬件修改
- 软件：与桌面单臂/双臂设置相同——直接从SO-100/SO-101手臂转移您训练好的策略
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">💪</span>

**实用可靠**: 执行许多日常任务，可与市场上$30,000的闭源机器人相媲美。
- 更多任务在[**Huggingface LeRobot全球黑客马拉松**](https://huggingface.co/spaces/LeRobot-worldwide-hackathon/all-winners)中展示。
- **注意**：目前不适用于手内灵巧操作🤹、重物提升(每臂超过1kg)🏋️或高度动态运动(接球)🏃
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">📕</span>

**丰富的开源资源**
- LeRobot的即插即用代码🧩和广泛的AI模型库🧠
- 由活跃、不断增长的贡献者社区支持🧑‍🤝‍🧑
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">⚠️</span>

**安全始终重要**: XLeRobot具有固有的物理硬件限制(低扭矩电机、短臂长、轮式基础)，使其**物理上**几乎不可能伤害人类，同时仍然保持执行许多家庭任务的能力。
:::
::::

## 开始上手

```{xl-section}
:band: gray
```

:::{container} xl-lead
从一箱零件，到一台会学习的机器人。每一步都可以点进对应教程。
:::

```{xl-flow}
:numbered:

items:
  - icon: cart-shopping
    title: 材料清单
    text: 购买零件，基础版约 ¥3999。
    link: doc:hardware/getting_started/material
  - icon: print
    title: 3D打印
    text: 打印手臂、底座和头部零件。
    link: doc:hardware/getting_started/3d
  - icon: screwdriver-wrench
    title: 组装
    text: 总共不到 4 小时。
    link: doc:hardware/getting_started/assemble
  - icon: terminal
    title: 安装软件
    text: LeRobot 加 XLeRobot 插件。
    link: doc:software/getting_started/install
  - icon: gamepad
    title: 遥操作
    text: 控制双臂和底盘。
    chips: [键盘, Xbox, Joycon, VR]
    link: doc:software/getting_started/XLeRobot_teleop
  - icon: brain
    title: 学习与部署
    text: 训练策略，或运行 LLM 智能体。
    chips: [ACT, SmolVLA, π0.5, RL]
    link: doc:software/index
branch:
  icon: cube
  title: 想先试试？
  text: 在网页 MuJoCo 仿真或 ManiSkill 里体验 XLeRobot。
  link: doc:simulation/index
```

## 成本

:::{container} xl-lead
自己购买零件，按需添加配件。
:::

```{xl-pricing}
currencies:
  - {code: CN, label: "中国 ¥", symbol: "¥"}
  - {code: US, label: "美国 $", symbol: "$"}
  - {code: EU, label: "欧盟 €", symbol: "€"}
  - {code: IN, label: "印度 ₹", symbol: "₹"}
labels:
  currency: 货币
  total: 预计总价
  included: 已包含
base:
  label: 基础版 (使用自己的笔记本电脑，单RGB头部摄像头)
  prices: {US: 660, EU: 680, CN: 3999, IN: 87000}
choices:
  - legend: 头部摄像头
    type: radio
    options:
      - label: 单RGB头部摄像头
        prices: {US: 0, EU: 0, CN: 0, IN: 0}
      - label: 立体双RGB头部摄像头
        prices: {US: 30, EU: 30, CN: 199, IN: 6550}
      - label: RealSense RGBD头部摄像头
        prices: {US: 220, EU: 230, CN: 1499, IN: 35726}
  - legend: 附加配件
    type: checkbox
    options:
      - label: 树莓派
        prices: {US: 79, EU: 79, CN: 399, IN: 7999}
note: 价格为估算值，不含3D打印、工具、运费和税费。
```

| 价格（自己购买零件） | 美国 | 欧盟 | 中国 | 印度 |
| --- | --- | --- | --- | --- |
| **基础版** (使用自己的笔记本电脑，单RGB头部摄像头) | **~$660** | **~€680** | **~¥3999** | **~₹87000** |
| ↑ 立体双RGB头部摄像头 | +$30 | +€30 | +¥199 | +₹6550 |
| + 树莓派 | +$79 | +€79 | +¥399 | +₹7999 |
| ↑ RealSense RGBD头部摄像头 | +$220 | +€230 | +¥1499 | +₹35726 |

面向开发者的组装套件已于 2025-09-09 上架，购买链接见[新闻](#新闻)。

## XLeRobot适合谁？

```{xl-section}
:band: gray
```

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🚀</span>

**初创公司和实验室**: 使用世界上最便宜的模块化平台更快地构建原型
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">👩‍🔬</span>

**自研人员**: 在不破产的情况下实验具身AI 💸
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🎓</span>

**教育英雄**:
- 高中教师: 将前沿机器人技术带入STEM课堂 🧪
- 大学教授: 机器人/AI课程的经济实惠平台 📚
- 学生: 从初学者到研究人员 🎒→🎓
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🤖</span>

**DIY爱好者**: 完美适合室内项目 - 植物护理、递送机器人、家庭自动化 🌱📦
:::
::::

## 新闻

:::{container} xl-lead
从第一个演示到今天。
:::

```{xl-timeline}
- version: "0.1.0"
  text: "第一个演示：[XLeRobot 的起点](doc:demos/index)。"
- version: "0.2.0"
  date: "2025-06-13"
  text: 硬件设置完全具备家务任务能力，成本660美元。
- version: "0.3.0"
  date: "2025-08-30"
  text: 最终外观完善和家庭杂务展示演示。
- version: "0.4.0"
  date: "2025-12 / 2026-01"
  state: current
  text: 双轮底盘、模块化手臂底座、360° 紧凑头部。最后一个完全基于飞特舵机的版本。
- version: 下一步
  state: next
  text: 与 Hightorque 和 Wowrobo 合作，基于更高性能的电机，打造更接近产品级的低成本开源移动机器人。
```

```{xl-cards}
:columns: 3
:visible: 6
:more: 更多新闻（{n}）
:variant: news

- eyebrow: "2026-10-06"
  title: XLeRobot 以 LeRobot 插件形式安装
  text: "机器人（`xlerobot`、`xlerobot_2wheels`、`xlerobot_mecanum`）和 VR 遥操作器可通过 pip 安装，并直接用于任何 LeRobot 命令行，例如 `--robot.type=xlerobot`。"
  links:
    - {label: 安装教程, url: "doc:software/getting_started/install"}
- eyebrow: "2026-09-24"
  title: 新增社区页面
  text: 收录 9 篇研究论文和 34 个社区项目，均使用或扩展了 XLeRobot，支持中英文搜索。
  image: "_static/community/makermods.jpg"
  image_alt: 基于 XLeRobot 的 MakerMods 机器人
  links:
    - {label: 浏览案例, url: "doc:relatedworks/index"}
- eyebrow: "2026-04-21"
  title: 麦克纳姆轮底盘
  text: "全向移动（平移和原地转向），四个驱动电机，与双轮版共用同一套硬件。由社区贡献（#135）。"
  links:
    - {label: 麦克纳姆轮组装（英文）, url: "https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble_mecanum.html"}
- eyebrow: "2026-02-01"
  title: 网页版 MuJoCo 仿真
  text: 基于 MuJoCo 引擎和 3DGS，在浏览器里即刻体验 XLeRobot。
  links:
    - {label: 立即体验, url: "doc:simulation/index"}
    - {label: Hugging Face, url: "https://huggingface.co/spaces/VectorW/xlerobot-sim"}
- eyebrow: "2026-01-04"
  title: XLeRobot 0.4.0 双轮版
  text: "相比三全向轮更稳、更快、扭矩更大，提供舵机和无刷电机两个版本，配模块化手臂底座和 360° 紧凑头部。附 Wowrobo 官方组装视频。"
  image: "https://github.com/user-attachments/assets/7e71afda-1ec5-4b96-a199-42a0cd726226"
  image_alt: XLeRobot 0.4.0 双轮版
  links:
    - {label: 双轮组装（英文）, url: "https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble_2wheel.html"}
- eyebrow: "2025-12-24"
  title: 社区贡献的 VLA 教程
  text: "在 XLeRobot 上训练和部署 ACT、SmolVLA 和 π0.5，附数据集和三相机双臂演示。"
  image: "https://vector-wangel.github.io/XLeRobot-assets/videos/Community/makermod/demoshow.gif"
  image_alt: XLeRobot 上的 SmolVLA 演示
  links:
    - {label: ACT, url: "doc:software/getting_started/VLA_ACT"}
    - {label: SmolVLA, url: "doc:software/getting_started/VLA_smol"}
    - {label: π0.5, url: "doc:software/getting_started/VLA_pi05"}
- eyebrow: "2025-10-17"
  title: 自主 LLM 智能体
  text: 用 LLM 智能体控制 XLeRobot，借助相机视觉和语音指令移动机器人、操作物体。
  image: "https://github.com/user-attachments/assets/296f6f60-52a4-4fa0-9a77-a113b4868f83"
  image_alt: LLM 智能体控制 XLeRobot
  links:
    - {label: LLM 智能体教程, url: "doc:software/getting_started/LLM_agent"}
- eyebrow: "2025-09-22"
  title: 硬件组装教程视频
  text: "发布于 [Youtube](https://www.youtube.com/watch?v=upB1CEFeOlk) 和 [Bilibili](https://www.bilibili.com/video/BV1AGWFzUEJf/). 感谢 WOWROBO 费心制作!"
- eyebrow: "2025-09-09"
  title: 面向开发者的组装套件 (不包括电池和宜家推车) 正式上架
  text: "[中国 (淘宝) **3699￥**](https://e.tb.cn/h.SZFbBgZABZ8zRPe?tk=ba514rTBRjQ) 和 [全球 **579$**](https://shop.wowrobo.com/products/xlerobot-dual-arm-mobile-household-robot-kit?variant=47297659961561). (与**Wowrobo**合作, Huggingface SO101 手臂官方合作商之一, 已在全球范围卖出 5千+ SO101 手臂，用户反馈好)"
  image: "https://github.com/user-attachments/assets/788836c1-966a-4d11-a911-5c37befc0b85"
  image_alt: 组装套件内容和购买页面
  notes:
    - 售卖套件仅为项目推广，我本人不从中获利，并要求wowrobo以尽可能低价售卖.
    - 组装套件仅面向开发者，非消费级产品，请详细阅读文档和repo，确认目前可用的代码和教程后再购买.
- eyebrow: "2025-09-09"
  title: 具身智能家庭机器人黑客松
  text: "作为导师团队之一参与由英伟达，Huggingface，SEEED联合举办的[具身智能家庭机器人黑客松](https://www.seeedstudio.com/embodied-ai-worldwide-hackathon-home-robot.html) (10.18-19深圳，10.25–26, 湾区)!."
  image: "https://github.com/user-attachments/assets/89039122-e758-406b-b64b-72016e00285b"
  image_alt: 具身智能黑客松导师团队海报
- eyebrow: "2025-08-30"
  title: XLeRobot 0.3.0 发布
  text: 最终外观完善和家庭杂务展示演示。
  links:
    - {label: 观看视频, url: "#film"}
- eyebrow: "2025-07-30"
  title: 控制XLeRobot在真实环境中
  text: "使用**键盘/Xbox/Switch joycon**（蓝牙，无需wifi，0延迟）。"
  image: "https://github.com/user-attachments/assets/de8f50ad-a370-406c-97fb-fc01638d5624"
  image_alt: 用手柄控制 XLeRobot
  links:
    - {label: 软件, url: "doc:software/index"}
- eyebrow: "2025-07-08"
  title: Maniskill仿真
  text: "支持URDF、控制脚本（支持Quest3 VR、键盘、Xbox、Switch Joycon）。支持多种传感器（深度、分割、触觉等），RL/IL/VLA环境。15分钟快速上手。"
  image: "https://github.com/user-attachments/assets/68b77bea-fdcf-4f42-9cf0-efcf1b188358"
  image_alt: ManiSkill 仿真中的 XLeRobot 和 VR 控制
  links:
    - {label: 仿真, url: "doc:simulation/index"}
- eyebrow: "2025-07-01"
  title: 文档网站上线
  text: 提供更有序的教程、演示和资源。
  links:
    - {label: 文档, url: "https://xlerobot.readthedocs.io/en/latest/index.html"}
- eyebrow: "2025-06-13"
  title: XLeRobot 0.2.0
  text: 硬件设置完全具备家务任务能力，成本660美元。
  links:
    - {label: 硬件, url: "doc:hardware/index"}
```

## 局限性

```{xl-section}
:band: gray
```

:::{container} xl-lead
(嘿，这个价格，还要什么自行车？)
:::

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🔒</span>

固定高度——添加稳定的升降平台将显著增加成本和组装难度
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">📏</span>

与Aloha相比工作空间较小——虽然我们最大化了SO101的工作空间，但手臂有尺寸限制(~40cm reach)，不过XLeRobot仍能有效处理大多数任务
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">⚖️</span>

单臂负载能力有限(600~1000g)
:::
::::

:::{container} xl-lead
综合考虑——成本、社区支持、组装便捷性和实用性——XLeRobot脱颖而出，成为室内应用最具吸引力的低成本机器人之一！
:::

## 贡献

```{xl-section}
:class: xl-compact
```

**👋 想要贡献？**
请参考[CONTRIBUTING.md](https://github.com/Vector-Wangel/XLeRobot/blob/main/CONTRIBUTING.md)了解如何参与！

**主要贡献者**

- [Gaotian/Vector Wang](https://vector-wangel.github.io/)(我自己)
- Zhuoyi Lu: RL sim2real部署，真实机器人遥操作(Xbox, VR, Joycon)
- Nicole Yue: 文档网站设置
- Yuesong Wang: Mujoco仿真资源

这只是金字塔中的一小块砖，由[LeRobot](https://github.com/huggingface/lerobot)、[SO-100](https://github.com/TheRobotStudio/SO-ARM100)、[Lekiwi](https://github.com/SIGRobotics-UIUC/LeKiwi)和[Bambot](https://github.com/timqian/bambot)共同实现。感谢这些详细且专业项目背后所有才华横溢的贡献者。

期待与任何有兴趣为该项目做出贡献的人合作！

(citation)=
## 引用

```{xl-section}
:class: xl-compact
```

如果您愿意，可以使用以下方式引用本工作：

```bibtex
@misc{wang2025xlerobot,
    author = {Wang, Gaotian and Lu, Zhuoyi and Huang, Yiyang and Liu, Yihao},
    title = {XLeRobot: A Practical Low-cost Household Dual-Arm Mobile Robot Design for General Manipulation},
    howpublished = "\url{https://github.com/Vector-Wangel/XLeRobot}",
    year = {2025}
}
```

## 免责声明

```{xl-section}
:class: xl-compact xl-fineprint
```

> 如果您基于此仓库构建、购买或开发XLeRobot，您将对其对您或他人造成的所有物理和精神损害负全部责任。

![image](https://github.com/user-attachments/assets/682ef049-bb42-4b50-bf98-74d6311e774d)

```{toctree}
:maxdepth: 1
:hidden:
hardware/index
simulation/index
software/index
demos/index
社区 <relatedworks/index>
```
