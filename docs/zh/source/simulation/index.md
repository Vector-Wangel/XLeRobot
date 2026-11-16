# 仿真

<div class="xl-sim-stage" id="xl-sim">
<iframe src="https://vectorw-xlerobot-sim.static.hf.space/index.html?env=tabletop&amp;style=pixel" title="XLeRobot Sim：在浏览器里用 MuJoCo 仿真 XLeRobot" allow="fullscreen" allowfullscreen></iframe>
</div>
<div class="xl-sim-bar">
<p class="xl-sim-bar__text"><strong>XLeRobot Sim</strong> 在浏览器里运行 MuJoCo：用键盘控制机器人，运行它的技能和学习到的策略，或者直接告诉智能体要做什么。</p>
<p class="xl-sim-bar__links"><button type="button" data-xl-fullscreen="xl-sim" hidden>全屏</button><a href="https://huggingface.co/spaces/VectorW/xlerobot-sim" target="_blank" rel="noopener">在 Hugging Face 打开</a><a class="xl-sim-bar__more" href="#maniskill">ManiSkill、VR 控制和更多场景</a></p>
</div>

(maniskill)=
## 在 ManiSkill 中仿真

XLeRobot 也可以在 [ManiSkill](https://github.com/haosulab/ManiSkill) 中运行，支持键盘、末端执行器和 VR 控制。

### [开始使用](getting_started/index)

- [解析逆运动学介绍的简短技术博客](https://vectorwang.notion.site/Analytical-IK-for-SO101-20abb280f59380d288bcdd398ffbfab1)。

- 详细的[**逐步安装指南**](getting_started/index)，让您能在10分钟内开始复制这个演示。

- URDF文件、maniskill机器人代理脚本、关节/末端执行器控制脚本。

### [VR控制](getting_started/vr_sim)

<video width="100%" style="max-width: 100%;" controls>
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Sim_demos/XLeRobot_0_2_3.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### [更多场景](getting_started/simdemos)

<video width="100%" style="max-width: 100%;" controls>
  <source src="https://vector-wangel.github.io/XLeRobot-assets/videos/Sim_demos/XLeRobot_0_1_5.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

```{toctree}
getting_started/index
getting_started/vr_sim
getting_started/simdemos
```
