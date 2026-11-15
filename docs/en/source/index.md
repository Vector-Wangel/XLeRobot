# XLeRobot

::::{container} xl-hero
:::{container} xl-hero-subtitle
Open-source Household Dual-arm Mobile Robot
:::

:::{container} xl-hero-tagline
Bring Embodied AI to Every Developer Around the World!
:::

:::{container} xl-cta
[Get started](hardware/index.md) <a href="#film">Watch the film</a> [View on GitHub](https://github.com/Vector-Wangel/XLeRobot)
:::

:::{container} xl-badges
[![GitHub](https://img.shields.io/badge/GitHub-XLeRobot-181717?logo=github&style=flat)](https://github.com/Vector-Wangel/XLeRobot) [![Stars](https://img.shields.io/github/stars/Vector-Wangel/XLeRobot?style=social)](https://github.com/Vector-Wangel/XLeRobot) [![Twitter/X](https://img.shields.io/twitter/follow/VectorWang?style=social)](https://twitter.com/VectorWang2) [![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Discord](https://img.shields.io/badge/Discord-Join%20Chat-7289da.svg?logo=discord&logoColor=white)](https://discord.gg/bjZveEUh6F)
:::

:::{container} xl-hero-media
![XLeRobot, an open-source household dual-arm mobile robot for $660 and 4 hours of assembly](https://github.com/user-attachments/assets/f9c454ee-2c46-42b4-a5d7-88834a1c95ab)
:::

:::{container} xl-hero-credits
*Built upon the giants: [LeRobot](https://github.com/huggingface/lerobot), [SO-100/SO-101](https://github.com/TheRobotStudio/SO-ARM100), [Lekiwi](https://github.com/SIGRobotics-UIUC/LeKiwi), [Bambot](https://github.com/timqian/bambot)*
:::
::::

```{xl-stats}
- value: "~$660"
  label: Total cost, basic version
- value: "<4 hrs"
  label: Total assembly time
- value: "~12 kg"
  label: Easily lifted by an adult
- value: "10 hrs+"
  label: Normal operation on one charge
```

<div class="xl-film" id="film">
<video controls playsinline preload="metadata">
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/xlerobot030.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
</div>

## Why XLeRobot?

:::{container} xl-lead
**XLeRobot = XL + LeRobot**
:::

```{xl-compose}
groups:
  - eyebrow: Core
    title: LeRobot
    items:
      - icon: hand
        label: 2× SO-100/SO-101 arms
        note: 90% 3D printed, affordable motors
      - icon: code
        label: LeRobot software
        note: pip install and a few lines of code
      - icon: users
        label: LeRobot community
        note: SOTA VLA models, datasets and tools
  - eyebrow: Enhancement
    title: XL
    items:
      - icon: cart-flatbed
        label: IKEA RÅSKOG cart
        note: Sturdy, global, household height
      - icon: circle-dot
        label: Omni-wheel base
        note: Upgrade directly from Lekiwi
      - icon: battery-full
        label: Anker SOLIX C300
        note: 288Wh, powers everything over USB-C
      - icon: camera
        label: Head camera
        note: RGB, stereo or RealSense
result:
  eyebrow: Result
  title: XLeRobot
  text: A practical low-cost household dual-arm mobile robot.
  chips: ["~$660", "<4 hrs assembly", "~12 kg"]
```

<div class="xl-spacer"></div>

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Why "LeRobot" Core?
:class-card: xl-card

- **Cheap Materials** 💴: 90% 3D printed components with affordable motors and electronics.
- **Easy Assembly** 🔨: 67 min to assemble 2 SO101 arms and configure motors.
- **Plug-&-Play** 🧩: Get robots running with simple pip install and a few lines of code.
- **Thriving LeRobot Community** 🌍:
World's largest low-cost robotics community featuring
    - Multiple [SOTA VLA models🧠](https://huggingface.co/lerobot), datasets📊, and tools🔨 ready for deployment.
    - 10k+ members for brainstorming and discussions🧑‍🤝‍🧑.
:::

:::{grid-item-card} Why "XL" Enhancement?
:class-card: xl-card

![image](https://github.com/user-attachments/assets/b48a0a41-7422-4f10-8dc6-a66a2fd746ad)

- 🏠 The field/market lacks affordable, stable, dual-arm home robots that match LeRobot's ease of assembly.
- 🖨️ Traditional 3D printed chassis suffer from limited durability, stability, and load capacity — impractical for daily use.
- ⚡ DIY mobile robots face power supply challenges, leading to complex wiring setups.
:::
::::

:::{container} xl-subhead
Overall Advantages
:::

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">💴</span>

**Cost-effective**: Complete build costs \$660, or directly upgrade from your SO101 Arm and Lekiwi for \$250.
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">⏫</span>

**Easy upgrade** from **Lekiwi** and **SO-100/SO-101**
- Hardware: No motor ID changes or mods needed
- Software: Same tabletop single/dual-arm setup—transfer your policies directly from SO101 arm
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">💪</span>

**Practical and reliable**: Performs many daily tasks comparable to $30,000 closed-source robots.
- More tasks demonstrated in the [**Huggingface LeRobot World-wide Hackathon**](https://huggingface.co/spaces/LeRobot-worldwide-hackathon/all-winners).
- **Note**: Not currently designed for in-hand dexterity 🤹, heavy lifting (over 1kg per arm) 🏋️, or highly dynamic movements (catch ball) 🏃
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">📕</span>

**Rich open-source resources**
- LeRobot's plug-and-play code🧩 and extensive AI model library🧠
- Backed by an active, growing community of contributors🧑‍🤝‍🧑
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">⚠️</span>

**Safety always matters**: XLeRobot has inherent physical hardware limitations (low-torque motors, short arm length, wheel-based), making it **physically** almost incapable of harming humans, while still maintaining its ability to perform many household tasks.
:::
::::

## Get started

```{xl-section}
:band: gray
```

:::{container} xl-lead
From a box of parts to a robot that learns. Each step links to its guide.
:::

```{xl-flow}
:numbered:

items:
  - icon: cart-shopping
    title: Bill of Material
    text: Order the parts, about $660 for the basic version.
    link: doc:hardware/getting_started/material
  - icon: print
    title: 3D Printing
    text: Print the arm, base and head parts.
    link: doc:hardware/getting_started/3d
  - icon: screwdriver-wrench
    title: Assembly
    text: Under 4 hours in total.
    link: doc:hardware/getting_started/assemble
  - icon: terminal
    title: Install software
    text: LeRobot plus the XLeRobot plugins.
    link: doc:software/getting_started/install
  - icon: gamepad
    title: Teleoperate
    text: Drive both arms and the base.
    chips: [Keyboard, Xbox, Joycon, VR]
    link: doc:software/getting_started/XLeRobot_teleop
  - icon: brain
    title: Learn and deploy
    text: Train policies or run an LLM agent.
    chips: [ACT, SmolVLA, π0.5, RL]
    link: doc:software/index
branch:
  icon: cube
  title: Want to try it first?
  text: Play with XLeRobot in the web MuJoCo simulation or ManiSkill.
  link: doc:simulation/index
```

## Cost

:::{container} xl-lead
Buy the parts yourself, then add only what you need.
:::

```{xl-pricing}
currencies:
  - {code: US, label: "US $", symbol: "$"}
  - {code: EU, label: "EU €", symbol: "€"}
  - {code: CN, label: "CN ¥", symbol: "¥"}
  - {code: IN, label: "IN ₹", symbol: "₹"}
labels:
  currency: Currency
  total: Estimated total
  included: Included
base:
  label: Basic (use your laptop, single RGB head cam)
  prices: {US: 660, EU: 680, CN: 3999, IN: 87000}
choices:
  - legend: Head camera
    type: radio
    options:
      - label: Single RGB head cam
        prices: {US: 0, EU: 0, CN: 0, IN: 0}
      - label: Stereo dual-eye RGB head cam
        prices: {US: 30, EU: 30, CN: 199, IN: 6550}
      - label: RealSense RGBD head cam
        prices: {US: 220, EU: 230, CN: 1499, IN: 35726}
  - legend: Add-ons
    type: checkbox
    options:
      - label: RaspberryPi
        prices: {US: 79, EU: 79, CN: 399, IN: 7999}
note: Prices are approximate and exclude 3D printing, tools, shipping and taxes.
```

| Price (Buy Parts Yourself) | US | EU | CN | IN |
| --- | --- | --- | --- | --- |
| **Basic** (use your laptop, single RGB head cam) | **~$660** | **~€680** | **~¥3999** | **~₹87000** |
| ↑ Stereo dual-eye RGB head cam | +$30 | +€30 | +¥199 | +₹6550 |
| + RaspberryPi | +$79 | +€79 | +¥399 | +₹7999 |
| ↑ RealSense RGBD head cam | +$220 | +€230 | +¥1499 | +₹35726 |

The developer assembly kit went on sale on 2025-09-09. See [News](#news) for purchase links.

## Who is XLeRobot For?

```{xl-section}
:band: gray
```

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🚀</span>

**Startups & Labs**: Build prototypes faster with one of the world's cheapest general robotics platform
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">👩‍🔬</span>

**Self Researchers**: Experiment with embodied AI without breaking the bank 💸
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🎓</span>

**Educators**:
- High School Teachers: Bring cutting-edge robotics to STEM classes 🧪
- University Professors: Affordable platform for robotics/AI courses 📚
- Students: From beginners to researchers 🎒→🎓
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🤖</span>

**DIY Enthusiasts**: Perfect for indoor projects - plant care, delivery bots, home automation 🌱📦
:::
::::

## News

:::{container} xl-lead
From the first demo to today.
:::

```{xl-timeline}
- version: "0.1.0"
  text: "First demo: [where XLeRobot started](doc:demos/index)."
- version: "0.2.0"
  date: "2025-06-13"
  text: Hardware setup fully capable for household tasks, with 660$ cost.
- version: "0.3.0"
  date: "2025-08-30"
  text: Final outfit touch up and household chores showcase demos.
- version: "0.4.0"
  date: "2025-12 / 2026-01"
  badge: Draft
  state: current
  text: Dual-wheel base, modular arm base, 360° compact head. The last version fully based on Feetech servos.
- version: Next
  state: next
  text: More product-level, low-cost open-source mobile robots on higher-performance motors, with Hightorque and Wowrobo.
```

```{xl-cards}
:columns: 3
:visible: 6
:more: More news ({n})
:variant: news

- eyebrow: "2026-10-06"
  badge: Draft
  title: XLeRobot installs as a LeRobot plugin
  text: "The robots (`xlerobot`, `xlerobot_2wheels`, `xlerobot_mecanum`) and the VR teleoperator install with pip and work with any LeRobot CLI command, e.g. `--robot.type=xlerobot`."
  links:
    - {label: Install guide, url: "doc:software/getting_started/install"}
- eyebrow: "2026-09-24"
  badge: Draft
  title: New Community page
  text: 9 research papers and 34 community projects that use or extend XLeRobot, searchable in English and Chinese.
  image: "_static/community/makermods.jpg"
  image_alt: A MakerMods robot built on XLeRobot
  links:
    - {label: Browse the community, url: "doc:relatedworks/index"}
- eyebrow: "2026-04-21"
  badge: Draft
  title: Mecanum wheel base
  text: "Holonomic drive (strafe and turn in place) with four drive motors, on the same hardware stack as the dual-wheel version. Contributed by the community (#135)."
  image: "_static/xlerobot_mecanum.gif"
  image_alt: XLeRobot driving on mecanum wheels
  links:
    - {label: Mecanum assembly, url: "doc:hardware/getting_started/assemble_mecanum"}
- eyebrow: "2026-02-01"
  badge: Draft
  title: Web MuJoCo simulation
  text: Play with XLeRobot instantly in the browser, using the MuJoCo engine and 3DGS.
  links:
    - {label: Try it, url: "doc:simulation/index"}
    - {label: MuJoCo-GS-Web, url: "https://github.com/Vector-Wangel/MuJoCo-GS-Web"}
- eyebrow: "2026-01-04"
  badge: Draft
  title: XLeRobot 0.4.0, dual-wheel version
  text: "More stable, faster and stronger than three omni wheels, in servo and brushless versions, with a modular arm base and a 360° compact head. Official assembly videos from Wowrobo."
  image: "https://github.com/user-attachments/assets/7e71afda-1ec5-4b96-a199-42a0cd726226"
  image_alt: XLeRobot 0.4.0 dual-wheel version
  links:
    - {label: Dual-wheel assembly, url: "doc:hardware/getting_started/assemble_2wheel"}
- eyebrow: "2025-12-24"
  badge: Draft
  title: VLA tutorials from the community
  text: "Train and deploy ACT, SmolVLA and π0.5 on XLeRobot, with datasets and three-camera bimanual demos."
  image: "https://vector-wangel.github.io/XLeRobot-assets/videos/Community/makermod/demoshow.gif"
  image_alt: SmolVLA demo on XLeRobot
  links:
    - {label: ACT, url: "doc:software/getting_started/VLA_ACT"}
    - {label: SmolVLA, url: "doc:software/getting_started/VLA_smol"}
    - {label: π0.5, url: "doc:software/getting_started/VLA_pi05"}
- eyebrow: "2025-10-17"
  badge: Draft
  title: Autonomous LLM agent
  text: Control XLeRobot with an LLM agent that uses camera vision and voice commands to move the robot and manipulate objects.
  image: "https://github.com/user-attachments/assets/296f6f60-52a4-4fa0-9a77-a113b4868f83"
  image_alt: LLM agent controlling XLeRobot
  links:
    - {label: LLM agent tutorial, url: "doc:software/getting_started/LLM_agent"}
- eyebrow: "2025-09-22"
  title: Hardware Assembly Video Tutorial
  text: "Available at [Youtube](https://www.youtube.com/watch?v=upB1CEFeOlk) and [Bilibili](https://www.bilibili.com/video/BV1AGWFzUEJf/). Thanks WOWROBO for making this video!"
- eyebrow: "2025-09-09"
  title: Developer Assembly kit (excluding battery and IKEA cart) ready for purchase
  text: "In [China (Taobao) for **3699￥**](https://e.tb.cn/h.SZFbBgZABZ8zRPe?tk=ba514rTBRjQ) and [world-wide for **579$**](https://shop.wowrobo.com/products/xlerobot-dual-arm-mobile-household-robot-kit?variant=47297659961561). (In collaboration with **Wowrobo**, one of the official collaborators with Huggingface SO101 arm, they have sold 5k+ SO101 arm worldwide with great customer feedbacks.)"
  image: "https://github.com/user-attachments/assets/788836c1-966a-4d11-a911-5c37befc0b85"
  image_alt: Assembly kit packages and shop pages
  notes:
    - Non-profit, I personally don't earn any from this. I also asked Wowrobo to set the price as low as possible.
    - This is only the assembly kit for developers, please check documentation website and this repo for available codes and tutorials before you purchase.
- eyebrow: "2025-09-09"
  title: Embodied AI Home Robot Hackathon
  text: "Joined [Embodied AI Home Robot Hackathon](https://www.seeedstudio.com/embodied-ai-worldwide-hackathon-home-robot.html) (Oct 25–26, Bay Area) held by **SEEED x Nvidia x Huggingface** as mentor! [Register HERE](https://docs.google.com/forms/d/e/1FAIpQLSdYYDegdgIypxuGJNLcoc8kbdmU4jKgl49zg4X-107LAmBN4g/viewform)."
  image: "https://github.com/user-attachments/assets/4132c23b-5c86-4bb9-94b4-a6b12059685b"
  image_alt: Embodied AI Hackathon mentor team poster
- eyebrow: "2025-08-30"
  title: XLeRobot 0.3.0 Release
  text: With final outfit touch up and household chores showcase demos.
  links:
    - {label: Watch the film, url: "#film"}
- eyebrow: "2025-07-30"
  title: Control XLeRobot in real life
  text: "With **keyboard/Xbox/Switch joycon** in the wild (bluetooth, no wifi, 0 latency)."
  image: "https://github.com/user-attachments/assets/de8f50ad-a370-406c-97fb-fc01638d5624"
  image_alt: XLeRobot controlled with a game controller
  links:
    - {label: Software, url: "doc:software/index"}
- eyebrow: "2025-07-08"
  title: Maniskill Simulation
  text: "With URDFs, control scripts (support Quest3 VR, keyboard, Xbox, Switch Joycon). Supports for multiple sensors (depth, segmentation, tactile, etc), RL/IL/VLA environments. Get started in 15 min."
  image: "https://github.com/user-attachments/assets/68b77bea-fdcf-4f42-9cf0-efcf1b188358"
  image_alt: XLeRobot in ManiSkill simulation with VR control
  links:
    - {label: Simulation, url: "doc:simulation/index"}
- eyebrow: "2025-07-01"
  title: Documentation website
  text: Out for more organized tutorials, demos and resources.
  links:
    - {label: Documentation, url: "https://xlerobot.readthedocs.io/en/latest/index.html"}
- eyebrow: "2025-06-13"
  title: XLeRobot 0.2.0
  text: Hardware setup fully capable for household tasks, with 660$ cost.
  links:
    - {label: Hardware, url: "doc:hardware/index"}
```

## Limitations

```{xl-section}
:band: gray
```

:::{container} xl-lead
(Hey, for this price, what more could you ask for?)
:::

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">🔒</span>

Fixed height—adding a stable lifting platform would significantly increase cost and assembly difficulty
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">📏</span>

Smaller workspace compared to Aloha—while we try to maximize the SO101 workspace, the arm has size limitations (~40cm reach), though XLeRobot still handles most tasks effectively
:::

:::{grid-item-card}
:class-card: xl-card

<span class="xl-icon xl-icon--emoji">⚖️</span>

Limited payload capacity (600~1000g) for a single arm
:::
::::

:::{container} xl-lead
However, with all considered — cost, community support, ease of assembly, and practical utility — XLeRobot stands out as one of the most compelling low-cost robot for indoor application!
:::

## Contribute

```{xl-section}
:class: xl-compact
```

**👋 Want to contribute?**
Please refer to [CONTRIBUTING.md](https://github.com/Vector-Wangel/XLeRobot/blob/main/CONTRIBUTING.md) for guidance on how to get involved!

**Main Contributors**

- [Gaotian/Vector Wang](https://vector-wangel.github.io/)(myself)
- Zhuoyi Lu: RL sim2real deploy, teleop on real robot (Xbox, VR, Joycon)
- Nicole Yue: Documentation website setup
- Yuesong Wang: Mujoco simulation assets

This is just a small brick in the pyramid, made possible by [LeRobot](https://github.com/huggingface/lerobot), [SO-100](https://github.com/TheRobotStudio/SO-ARM100), [Lekiwi](https://github.com/SIGRobotics-UIUC/LeKiwi), and [Bambot](https://github.com/timqian/bambot). Thanks to all the talented contributors behind these detailed and professional projects.

Looking forward to collaborating with anyone interested in contributing to this project!

(citation)=
## Citation

```{xl-section}
:class: xl-compact
```

If you want, you can cite this work with:

```
@misc{wang2025xlerobot,
    author = {Wang, Gaotian and Lu, Zhuoyi},
    title = {XLeRobot: A Practical Low-cost Household Dual-Arm Mobile Robot Design for General Manipulation},
    howpublished = "\\url{<https://github.com/Vector-Wangel/XLeRobot>}",
    year = {2025}
}

```

## Disclaimer

```{xl-section}
:class: xl-compact xl-fineprint
```

> If you build, buy, or develop a XLeRobot based on this repo, you will be fully responsible for all the physical and mental damages it does to you or others.

![image](https://github.com/user-attachments/assets/682ef049-bb42-4b50-bf98-74d6311e774d)

```{toctree}
:maxdepth: 1
:hidden:
hardware/index
simulation/index
software/index
demos/index
Community <relatedworks/index>
```
