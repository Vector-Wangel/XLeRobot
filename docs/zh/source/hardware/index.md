# 硬件

## 总成本

> 成本不包括3D打印、工具、运输和税费。
> 

```{xl-pricing}
currencies:
  - {code: CN, label: "中国 ¥", symbol: "¥"}
  - {code: US, label: "美国 $", symbol: "$"}
  - {code: EU, label: "欧盟 €", symbol: "€"}
  - {code: IN, label: "印度 ₹", symbol: "₹"}
labels: {currency: 货币, total: 预计总价, included: 已包含}
base:
  label: 基础版 (使用自己的笔记本电脑，单RGB头部摄像头)
  prices: {US: 660, EU: 680, CN: 3999, IN: 87000}
choices:
  - legend: 头部摄像头
    type: radio
    options:
      - {label: 单RGB头部摄像头, prices: {US: 0, EU: 0, CN: 0, IN: 0}}
      - {label: 立体双RGB头部摄像头, prices: {US: 30, EU: 30, CN: 199, IN: 6550}}
      - {label: RealSense RGBD头部摄像头, prices: {US: 220, EU: 230, CN: 1499, IN: 35726}}
  - legend: 附加配件
    type: checkbox
    options:
      - {label: 树莓派, prices: {US: 79, EU: 79, CN: 399, IN: 7999}}
note: 成本不包括3D打印、工具、运输和税费。
```

| 价格 | 美国 | 欧盟 | 中国 | 印度 |
| --- | --- | --- | --- | --- |
| **基础版** (使用自己的笔记本电脑，单RGB头部摄像头) | **~$660** | **~€680** | **~¥3999** | **~₹87000** |
| ↑ 立体双RGB头部摄像头 | +$30 | +€30 | +¥199 | +₹6550 |
| + 树莓派 | +$79 | +€79 | +¥399 | +₹7999 |
| ↑ RealSense RGBD头部摄像头 | +$220 | +€230 | +¥1499 | +₹35726 |


## 开始使用

##### [材料清单](getting_started/material)

##### [3D打印](getting_started/3d)

##### [组装](getting_started/assemble)

##### [硬件介绍](hardware_intro/index)

### 选择底盘

```{xl-cards}
:columns: 3

- icon: circle-dot
  eyebrow: XLeRobot 0.3.0
  title: 三全向轮
  text: 与 Lekiwi 相同的底盘，可直接从 Lekiwi 升级。
  bullets:
    - 3× 4 英寸全向轮
    - 无需更改电机ID或硬件修改
  links:
    - {label: 组装, url: "doc:hardware/getting_started/assemble"}
- icon: arrows-left-right
  eyebrow: XLeRobot 0.4.0
  title: 双轮
  text: 更稳定、移动速度更快、通过性更好、扭矩更大。
  bullets:
    - 舵机版或无刷电机版
    - 模块化手臂底座，360° 紧凑头部
  links:
    - {label: 双轮组装（英文）, url: "https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble_2wheel.html"}
- icon: up-down-left-right
  eyebrow: 社区
  title: 麦克纳姆轮
  text: 全向移动，可平移和原地转向，与双轮版共用同一套硬件。
  bullets:
    - 四个驱动电机，扭矩和抓地力更强
    - X 型轮子布局
  links:
    - {label: 麦克纳姆轮组装（英文）, url: "https://xlerobot.readthedocs.io/en/latest/hardware/getting_started/assemble_mecanum.html"}
```

```{toctree}
:caption: 开始使用
getting_started/material
getting_started/3d
getting_started/assemble
```

```{toctree}
:caption: 硬件介绍
hardware_intro/index
```


