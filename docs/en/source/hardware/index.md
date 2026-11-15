# Hardware

## Total Cost

> Cost excludes 3D printing, tools, shipping, and taxes.
> 

```{xl-pricing}
currencies:
  - {code: US, label: "US $", symbol: "$"}
  - {code: EU, label: "EU €", symbol: "€"}
  - {code: CN, label: "CN ¥", symbol: "¥"}
  - {code: IN, label: "IN ₹", symbol: "₹"}
labels: {currency: Currency, total: Estimated total, included: Included}
base:
  label: Basic (use your laptop, single RGB head cam)
  prices: {US: 660, EU: 680, CN: 3999, IN: 87000}
choices:
  - legend: Head camera
    type: radio
    options:
      - {label: Single RGB head cam, prices: {US: 0, EU: 0, CN: 0, IN: 0}}
      - {label: Stereo dual-eye RGB head cam, prices: {US: 30, EU: 30, CN: 199, IN: 6550}}
      - {label: RealSense RGBD head cam, prices: {US: 220, EU: 230, CN: 1499, IN: 35726}}
  - legend: Add-ons
    type: checkbox
    options:
      - {label: RaspberryPi, prices: {US: 79, EU: 79, CN: 399, IN: 7999}}
note: Cost excludes 3D printing, tools, shipping, and taxes.
```

| Price | US | EU | CN | IN |
| --- | --- | --- | --- | --- |
| **Basic** (use your laptop, single RGB head cam) | **~$660** | **~€680** | **~¥3999** | **~₹87000** |
| ↑ Stereo dual-eye RGB head cam | +$30 | +€30 | +¥199 | +₹6550 |
| + RaspberryPi | +$79 | +€79 | +¥399 | +₹7999 |
| ↑ RealSense RGBD head cam | +$220 | +€230 | +¥1499 | +₹35726 |


## Get Started

##### [Bill of Material](getting_started/material)

##### [3D Printing](getting_started/3d)

##### [Assembly](getting_started/assemble)

##### [Assembly Dual-wheel](getting_started/assemble_2wheel)

##### [Assembly Mecanum wheels](getting_started/assemble_mecanum)

##### [Hardware Intro](hardware_intro/index)

### Choose a base

```{xl-cards}
:columns: 3

- icon: circle-dot
  eyebrow: XLeRobot 0.3.0
  title: Three omni wheels
  text: The Lekiwi-style base, so you can upgrade directly from Lekiwi.
  bullets:
    - 3× 4-inch omni wheels
    - No motor ID changes or mods needed
  links:
    - {label: Assembly, url: "doc:hardware/getting_started/assemble"}
- icon: arrows-left-right
  eyebrow: XLeRobot 0.4.0
  title: Dual wheel
  text: More stable, higher moving speed, better passability, and larger torque.
  bullets:
    - Servo motor or brushless motor version
    - Modular arm base, 360° compact head
  links:
    - {label: Assembly Dual-wheel, url: "doc:hardware/getting_started/assemble_2wheel"}
- icon: up-down-left-right
  eyebrow: Community
  title: Mecanum wheels
  text: Holonomic motion, strafe and turn in place, on the dual-wheel hardware stack.
  bullets:
    - Four drive motors, more torque and traction
    - X-pattern wheel layout
  links:
    - {label: Assembly Mecanum wheels, url: "doc:hardware/getting_started/assemble_mecanum"}
```

---


```{toctree}
:caption: Get started
getting_started/material
getting_started/3d
getting_started/assemble
getting_started/assemble_2wheel
getting_started/assemble_mecanum
```

```{toctree}
:caption: Hardware Intro
hardware_intro/index
```


