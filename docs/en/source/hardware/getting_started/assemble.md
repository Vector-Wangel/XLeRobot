# ⚒️ Assembly

![image](https://github.com/user-attachments/assets/949a670b-a5a2-459d-ab7f-45c51b93afa2)

> Estimated Assembly time: From scratch: 2-4 hrs; with assembled SO100/SO101 arms: 1-2 hrs
> 
```{tip}
If you'd rather skip the fun of tightening screws, you can also buy [pre-assembled kits](https://github.com/TheRobotStudio/SO-ARM100#kits) for SO101 arms.
```

## 🦾 SO101 Arms

![IMG_0264](https://github.com/user-attachments/assets/072d1e5b-f0c3-4bc6-a7cc-5ff38d42565c)


> If you already have 2x SO101 arms assembled with motors configured, skip.
>

- Build 2x SO101 arms by following [SO101 Step-by-Step Assembly Instructions](https://huggingface.co/docs/lerobot/so101) to build 2 identical follower arms with 2 sets of motors (both previous indexed as 1-6) for 2 control boards.
- Then continue to [configure the motors](https://huggingface.co/docs/lerobot/so101#configure-the-motors) for the SO101 arms. 
- Follow this [installation guide](https://github.com/TheRobotStudio/SO-ARM100/tree/main/Optional/SO101_Wrist_Cam_Hex-Nut_Mount_32x32_UVC_Module) to add wrist cameras.
- If you have [3M gripper tape](https://www.amazon.com/gp/product/B0093CQPW8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1), now it's time to wrap it on the fingers.


## 🤔 Configure Motors

![image](https://github.com/user-attachments/assets/fc674d38-d703-40bd-87a2-a502af1b52c7)

> Since the official lerobot codebase currently doesn't support motor configuring besides the arm, we use [Bambot](https://bambot.org/) instead (works on Windows and Mac, Linux needs 'sudo chmod 666 /dev/ttyACM0' first).
>

- Connect the motor you want to configure (one-by-one) to a control board, and directly connect the board to your computer. 
- Navigate to [the motor configuration page of Bambot](https://bambot.org/feetech.js), establish the connection and scan for your servo motor.
  ![image](https://github.com/user-attachments/assets/89eb4674-e26e-4edc-9943-ad5c0d4516ec)

- Rename the motor id following the instruction below.
  ![image](https://github.com/user-attachments/assets/49d3a1a4-71eb-4d32-9f0a-e8b6026c0b66)

- You need to configure two sets of motors for 2 motor control boards in addition to the SO101 arms:
    - one for **head** (motor ids: 7, 8)
    - and the other for **the wheel base** (motors ids: 7, 8, 9).
- Tips: write the numbers on motors with marker and distinguish motors for different boards (such as L1-L8 and R1-R9).

## 🛒 IKEA Cart

- Just in case you accidentally throw your manual away, [here it is](https://github.com/Vector-Wangel/XLeRobot/blob/main/others/Manuals_raskog_utility_cart.pdf).

<img width="925" alt="1745897734515" src="https://github.com/user-attachments/assets/f9f95840-5080-4084-bebb-ea456a097d55" />

## 🧑‍🦼‍➡ Wheel Base

> If you already have a Lekiwi base, detach the battery, servo mounts, etc. Base plate will only have 3 mounted motors with wheels (keep the wirings).
>

![image](https://github.com/user-attachments/assets/4599c9d0-3ce3-40e8-9a8e-d21e1e5feb01)

```{note}
Don't choose the wrong plate, each plate comes in a certain order.
```

- Mount the omni-wheels to the plate according to the figure above.
  - The specific motor id should be installed accordingly.
- Note that the connector of the omni-wheel needs 3x M4 screws.
- Wiring the motors regularly as the [tutorial](https://github.com/SIGRobotics-UIUC/LeKiwi/blob/main/Assembly.md#2-bottom-plate-assembly), after that instead of connecting the motor cable to the control board, use the extended wire/connector kit to extend the wire.

![image](https://github.com/user-attachments/assets/ac4ab4b4-6488-4e07-8349-e4167bf417f6)

- Mount the top plate according to the figure above.
- Leave the motor cable hanging ,don't pull it out from the top plate just yet.

![image](https://github.com/user-attachments/assets/651c7e03-6bdd-47de-8ab6-f9157ced06fe)

- Mount 3x connectors on the top plate according to the figure above.

```{tip}
Put the Lekiwi base with the connectors under the cart to see whether it can give enough pressure to the cart, with four wheels of the cart can still touch the ground. If not, try to modify the connectors' 3D model by slightly adjust the z-axis scale directly in the slicer software (keeping the xy-axis scale unchanged) and print them again.
```

![image](https://github.com/user-attachments/assets/c6bd27ec-6a2e-42ea-aee4-bb28079ccaf0)


```{tip}
Flip the cart over to do the assembly below.
```

- Now install the Lekiwi base with the connectors onto the bottom of the IKEA cart, with the thinner plate on the other side.
- Refer to the figure to find the desired assembly direction based on the motor index. 

```{note}
This new hardware version is compatible with the IKEA cart metal mesh, and all the 12 M3 screws should be able to fit in easily.
```

![image](https://github.com/user-attachments/assets/7792ee8d-7300-449f-b2bb-a78417dbc56b)


- Use needle-nose pliers to cut out the metal mesh at the corresponding holes in the top base, removing only the central "x" to maintain structural integrity. This creates openings for cable routing.
- Then, run the previously extended wire up through the cart from below.


## 🦾 Arm Base

### Top Base Assembly
![image](https://github.com/user-attachments/assets/1ea61764-6e4c-4edf-8d0f-0979430a7921)


- Easier assembly when the base is flipped over.

### Head Assembly

![image](https://github.com/user-attachments/assets/e24df68f-6140-456e-aeee-9e51f3c8a9f7)


- It should be the same as the first two steps of [SO101 arm assembly](https://huggingface.co/docs/lerobot/so101#joint-1).

## 🧵 Wiring

```{important}
Complete all wiring and cable management for the top base and put the Raspberry Pi in its case before clamping the top base into the IKEA cart.
```

![image](https://github.com/user-attachments/assets/798eeebf-a64f-4c16-b592-c32c8d9c62df)



- Prepare the extended 5264 wire with the connector kit if you don't have one already.
- Use needle-nose pliers to cut out the metal mesh at for the upper two layers for cable routing, similar to the bottom layer previously. Choose the location as needed.
```{note}
When extending the 5264 wire yourself, be careful with the polarity—reversed connections will cause errors.
```
- Connect the extended 5264 **motor cable** from **the Lekiwi base** to **one of the SO101 arms** (this makes the base and the arm as Lekiwi).
- Connect the 2 **USB-C to USB-A** **data cables** from 2 **motor control board** to **Rasberry Pi** (2 USB-A slots left for the cameras).
- Connect all 3 **power cables**: 2 **USB-C to DC(12V)** from 2 **motor control board** and 1 **USB-C to USB-C** from **Rasberry Pi**, to the fast charging section of the power supply. Each slot provides up to 100W power when charging simultaneously, which is tested sufficient for 12V version operation.

### 🔋 Place the Battery 🛒

- Anywhere you like on the middle or lower level of the cart to maintain a low center of mass. The battery has an anti-slip bottom so it won't easily slide during normal operations.
- Maintain placed upright for safety.
- Just in case you also accidentally throw the battery manual away, [here it is](https://github.com/Vector-Wangel/XLeRobot/blob/main/others/Manual_Anker_SOLIX_C300_DC_Portable_Power_Station.pdf).

```{important}
In order to protect the motor control board, make sure to connect the power cables last. And always disconnect the power cables when plugging/unplugging other cables.
```
## 📸 Final Assembly

### Base into the Cart

```{important}
Complete all wiring and cable management for the top base and put the Raspberry Pi in its case before clamping the top base into the IKEA cart.
```

![image](https://github.com/user-attachments/assets/2b568626-77c4-4956-a9ab-22db3638eb50)


- Be careful not to break the case when you jam the IKEA cart edge into the case socket.
- For easier testing, the SO101 arms clamp directly onto the cart. Position the [arm bases](https://github.com/Vector-Wangel/XLeRobot/blob/main/3D_Models/3D_models_for_printing/XLeRobot_special/SO_5DOF_ARM100_Assemblybases.stl) at the two corners of the cart's top layer, then secure with clamps.
- Don't forget to put the bambulab filament cardboard spool inside to provide stable structural support if you have one.


After these steps, the XLeRobot should be physically well-built and ready to do some chores.


![image](https://github.com/user-attachments/assets/4efa2b31-627c-4f62-9977-d6a50d8dce0e)

![image](https://github.com/user-attachments/assets/1d553e6a-dad6-4b17-bc82-e4d6d3e2ecc8)




```{important}
Once XLeRobot is fully assembled, do not push it around like the IKEA cart, as this can damage the motor gears. Instead, lift the robot (~12kg) whenever you need to move it manually.
```
```{note}
Current form of the wheel connector is not strong, occasionally rescrewing the center screw may be needed.
```
### Optional Visual Upgrades

For better visual outlook, you can wear these parts to XLeRobot if you like. 

![image](https://github.com/user-attachments/assets/91491f62-a466-4421-ac9b-db3492849a89)

- **Shells** for the Control board and the first joint for better protection and visual.
  - You may need to take off the hand camera first before wearing the 2nd shell onto the arm.
- Sports sleeves to hide the cables and make XLeRobot more sleek.
  
![image](https://github.com/user-attachments/assets/9847f2a6-f79a-4899-bd20-64a25c709660)
