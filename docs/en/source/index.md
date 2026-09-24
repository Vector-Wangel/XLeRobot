# XLeRobot 


[![GitHub](https://img.shields.io/badge/GitHub-XLeRobot-181717?logo=github&style=flat)](https://github.com/Vector-Wangel/XLeRobot) [![Stars](https://img.shields.io/github/stars/Vector-Wangel/XLeRobot?style=social)](https://github.com/Vector-Wangel/XLeRobot) [![Twitter/X](https://img.shields.io/twitter/follow/VectorWang?style=social)](https://twitter.com/VectorWang2) [![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Discord](https://img.shields.io/badge/Discord-Join%20Chat-7289da.svg?logo=discord&logoColor=white)](https://discord.gg/bjZveEUh6F)

<!-- [![en](https://img.shields.io/badge/lang-en-blue.svg)](..)
[![中文](https://img.shields.io/badge/lang-中文-brown.svg)](README_CN.md)

<div class="lang-switch">
  <a onclick="switchLang('en')" class="active">
    <img src="https://img.shields.io/badge/lang-en-blue.svg" alt="English" />
  </a>
  <a onclick="switchLang('zh')">
    <img src="https://img.shields.io/badge/lang-中文-brown.svg" alt="中文" />
  </a>
</div>

<div class="lang-en">
[English content...]
</div>

<div class="lang-zh">
[Chinese content...]
</div> -->


![image](https://github.com/user-attachments/assets/f9c454ee-2c46-42b4-a5d7-88834a1c95ab)

## Intro

**🚀 Bring Embodied AI to Every Family Around the World! Cheaper than iPhone📱!**

**⏰ <4hrs total assembly time**



*Built upon the giants: [LeRobot](https://github.com/huggingface/lerobot), [SO-100/SO-101](https://github.com/TheRobotStudio/SO-ARM100), [Lekiwi](https://github.com/SIGRobotics-UIUC/LeKiwi), [Bambot](https://github.com/timqian/bambot)*

---

<video width="100%" controls>
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Real_demos/xlerobot030.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## 📰 News 
- 2025-09-22: **Hardware Assembly Video Tutorial** availabe at [Youtube](https://www.youtube.com/watch?v=upB1CEFeOlk) and [Bilibili](https://www.bilibili.com/video/BV1AGWFzUEJf/). Thanks WOWROBO for making this video!
- 2025-09-09: **Developer Assembly kit (excluding battery and IKEA cart) ready for purchase** in [China (Taobao) for **3699￥**](https://e.tb.cn/h.SZFbBgZABZ8zRPe?tk=ba514rTBRjQ) and [world-wide for **579\$**](https://shop.wowrobo.com/products/xlerobot-dual-arm-mobile-household-robot-kit?variant=47297659961561). _(In collaboration with **Wowrobo**, one of the official collaborators with Huggingface SO101 arm, they have sold 5k+ SO101 arm worldwide with great customer feedbacks.)_
  ![image](https://github.com/user-attachments/assets/788836c1-966a-4d11-a911-5c37befc0b85)
  - Non-profit, I personally don't earn any from this. I also asked Wowrobo to set the price as low as possible.
  - This is only the assembly kit for developers, please check documentation website and this repo for available codes and tutorials before you purchase.
- 2025-09-09: Joined [Embodied AI Home Robot Hackathon](https://www.seeedstudio.com/embodied-ai-worldwide-hackathon-home-robot.html) (Oct 25–26, Bay Area) held by **SEEED x Nvidia x Huggingface** as mentor! [Register HERE](https://docs.google.com/forms/d/e/1FAIpQLSdYYDegdgIypxuGJNLcoc8kbdmU4jKgl49zg4X-107LAmBN4g/viewform).
- ![image](https://github.com/user-attachments/assets/4132c23b-5c86-4bb9-94b4-a6b12059685b)

- 2025-08-30: XLeRobot 0.3.0 Release with final outfit touch up and household chores showcase demos. 

- 2025-07-30: [Control XLeRobot in real life](https://xlerobot.readthedocs.io/en/latest/software/index.html)  with **keyboard/Xbox/Switch joycon** in the wild (bluetooth, no wifi, 0 latency).
- ![rea](https://github.com/user-attachments/assets/de8f50ad-a370-406c-97fb-fc01638d5624)


- 2025-07-08: [**Maniskill Simulation**](https://xlerobot.readthedocs.io/en/latest/simulation/index.html) with URDFs, control scripts (support Quest3 VR, keyboard, Xbox, Switch Joycon). 
Supports for multiple sensors (depth, segmentation, tactile, etc), RL/IL/VLA environments. Get started in 15 min.
-  ![vr](https://github.com/user-attachments/assets/68b77bea-fdcf-4f42-9cf0-efcf1b188358)

- 2025-07-01: [**Documentation** website](https://xlerobot.readthedocs.io/en/latest/index.html) out for more organized tutorials, demos and resources.

- 2025-06-13: [**XLeRobot 0.2.0**](https://xlerobot.readthedocs.io) hardware setup fully capable for household tasks, with 660$ cost. 

---
## Cost

| Price (Buy Parts Yourself) | US | EU | CN | IN |
| --- | --- | --- | --- | --- |
| **Basic** (use your laptop, single RGB head cam) | **~$660** | **~€680** | **~¥3999** | **~₹87000** |
| ↑ Stereo dual-eye RGB head cam | +$30 | +€30 | +¥199 | +₹6550 |
| + RaspberryPi | +$79 | +€79 | +¥399 | +₹7999 |
| ↑ RealSense RGBD head cam | +$220 | +€230 | +¥1499 | +₹35726 |

Assembly kit ready for purchase soon, stay tuned!


## 🌟 Why XLeRobot? 🌟

**XLeRobot = XL + LeRobot**

### Why "LeRobot" Core?

- **Cheap Materials** 💴: 90% 3D printed components with affordable motors and electronics.
- **Easy Assembly** 🔨: 67 min to assemble 2 SO101 arms and configure motors.
- **Plug-&-Play** 🧩: Get robots running with simple pip install and a few lines of code.
- **Thriving LeRobot Community** 🌍:
World's largest low-cost robotics community featuring
    - Multiple [SOTA VLA models🧠](https://huggingface.co/lerobot), datasets📊, and tools🔨 ready for deployment.
    - 10k+ members for brainstorming and discussions🧑‍🤝‍🧑.


### Why "XL" Enhancement?

![image](https://github.com/user-attachments/assets/b48a0a41-7422-4f10-8dc6-a66a2fd746ad)

- 🏠 The field/market lacks affordable, stable, dual-arm home robots that match LeRobot's ease of assembly.
- 🖨️ Traditional 3D printed chassis suffer from limited durability, stability, and load capacity — impractical for daily use.
- ⚡ DIY mobile robots face power supply challenges, leading to complex wiring setups.

### Overall Advantages

- **Cost-effective** 💴: Complete build costs \$660, or directly upgrade from your SO101 Arm and Lekiwi for \$250.
- **Easy upgrade** ⏫ from **Lekiwi** and **SO-100/SO-101**
    - Hardware: No motor ID changes or mods needed
    - Software: Same tabletop single/dual-arm setup—transfer your policies directly from SO101 arm
- **Practical and reliable** 💪: Performs many daily tasks comparable to $30,000 closed-source robots.
    - More tasks demonstrated in the [**Huggingface LeRobot World-wide Hackathon**](https://huggingface.co/spaces/LeRobot-worldwide-hackathon/all-winners).
    - **Note**: Not currently designed for in-hand dexterity 🤹, heavy lifting (over 1kg per arm) 🏋️, or highly dynamic movements (catch ball) 🏃
- **Rich open-source resources** 📕
    - LeRobot's plug-and-play code🧩 and extensive AI model library🧠
    - Backed by an active, growing community of contributors🧑‍🤝‍🧑
- **⚠️Safety always matters⚠️**: XLeRobot has inherent physical hardware limitations (low-torque motors, short arm length, wheel-based), making it **physically** almost incapable of harming humans, while still maintaining its ability to perform many household tasks.
  

---

## 🎯 Who is XLeRobot For?

- 🚀 **Startups & Labs**: Build prototypes faster with one of the world's cheapest general robotics platform
- 👩🔬 **Self Researchers**: Experiment with embodied AI without breaking the bank 💸
- 🎓 **Educators**:
    - High School Teachers: Bring cutting-edge robotics to STEM classes 🧪
    - University Professors: Affordable platform for robotics/AI courses 📚
    - Students: From beginners to researchers 🎒→🎓
- 🤖 **DIY Enthusiasts**: Perfect for indoor projects - plant care, delivery bots, home automation 🌱📦

---

## Limitations

(Hey, for this price, what more could you ask for?)

- 🔒 Fixed height—adding a stable lifting platform would significantly increase cost and assembly difficulty
- 📏 Smaller workspace compared to Aloha—while we try to maximize the SO101 workspace, the arm has size limitations (~40cm reach), though XLeRobot still handles most tasks effectively
- ⚖️ Limited payload capacity (600~1000g) for a single arm

However, with all considered — cost, community support, ease of assembly, and practical utility — XLeRobot stands out as one of the most compelling low-cost robot for indoor application!

---

## Contribute

**👋 Want to contribute?**
Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on how to get involved!

** Main Contributors **

- [Gaotian/Vector Wang](https://vector-wangel.github.io/)(myself)
- Zhuoyi Lu: RL sim2real deploy, teleop on real robot (Xbox, VR, Joycon)
- Nicole Yue: Documentation website setup
- Yuesong Wang: Mujoco simulation assets

This is just a small brick in the pyramid, made possible by [LeRobot](https://github.com/huggingface/lerobot), [SO-100](https://github.com/TheRobotStudio/SO-ARM100), [Lekiwi](https://github.com/SIGRobotics-UIUC/LeKiwi), and [Bambot](https://github.com/timqian/bambot). Thanks to all the talented contributors behind these detailed and professional projects.

Looking forward to collaborating with anyone interested in contributing to this project!

---

## Citation

If you want, you can cite this work with:

```
@misc{wang2025xlerobot,
    author = {Wang, Gaotian and Lu, Zhuoyi},
    title = {XLeRobot: A Practical Low-cost Household Dual-Arm Mobile Robot Design for General Manipulation},
    howpublished = "\\url{<https://github.com/Vector-Wangel/XLeRobot>}",
    year = {2025}
}

```

---

## 🪧 Disclaimer 🪧

> If you build, buy, or develop a XLeRobot based on this repo, you will be fully responsible for all the physical and mental damages it does to you or others.
>

![image](https://github.com/user-attachments/assets/682ef049-bb42-4b50-bf98-74d6311e774d)

---

```{toctree}
:maxdepth: 1
hardware/index
simulation/index
software/index
demos/index
Community Use Cases <relatedworks/index>
```
