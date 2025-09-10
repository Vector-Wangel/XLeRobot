# Get Started

### Prerequisites

- Ubuntu operating system
- Basic familiarity with terminal commands
- [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) (recommended)

### Installation

#### 1. Create a Conda Environment

If you already have a `lerobot` conda environment, you can use that. Otherwise, create a new environment:

```bash
conda create -y -n lerobot python=3.11
conda activate lerobot

```

> Note: It's recommended to have ManiSkill and lerobot code in the same environment for future sim2real deployment.
> 

#### 2. Install ManiSkill

Follow the [official installation instructions](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/installation.html) for ManiSkill.

```bash
# Basic installation
pip install mani-skill

# Download scene dataset
python -m mani_skill.utils.download_asset "ReplicaCAD"

```

If the dataset downloading goes wrong, you can directly download the dataset from [this google drive link](https://drive.google.com/file/d/1mqImztNX1LYZFBzt9z895C814RsyGe4N/view?usp=sharing). And then folder contents should go to

```bash
~/.maniskill/data/scene_datasets/replica_cad_dataset

```

Familiarize yourself with ManiSkill using the [quickstart guide](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/quickstart.html) and [demo scripts](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/quickstart.html). 

Try this command to test whether you have successfully installed Maniskill:

```{note}
Change shader="rt-fast" to "default" for faster rendering or if your computer doesn't support ray-tracing rendering.
```

```bash
python -m mani_skill.examples.demo_random_action -e "ReplicaCAD_SceneManipulation-v1" \\
  --render-mode="human" --shader="rt-fast"

```

And you should be looking at something like this:

![image](https://github.com/user-attachments/assets/c7509843-f037-4f37-9b1c-e7cad939037c)

#### 3. Additional Dependencies

We use **pygame** to read keyboard input and show the control panel in real time, and **Rerun** to visualize and collect camera data.

```bash
pip install pygame
pip install rerun-sdk
```

#### 4. Put XLeRobot Files to Maniskill

```{note}
We are expecting Maniskill to offer official support for XLeRobot soon, after that this step can be skipped.
```

Navigate to the ManiSkill package folder in your conda environment:

```bash
cd ~/miniconda3/envs/lerobot/lib/python3.10/site-packages/mani_skill
```

Put the XLeRobot files into Maniskill folders:

1. Download the [**XLeRobot Robot files** here](https://github.com/Vector-Wangel/XLeRobot/tree/main/simulation/Maniskill):
2. Put the files in /agents/robots, /assets/robots, and /envs/scenes:
   ![image](https://github.com/user-attachments/assets/59ae0104-7b9b-441a-a526-e9d0e2f99278)
   
   ![image](https://github.com/user-attachments/assets/a9107171-193b-485c-9620-f453e03f8f56)

   ![image](https://github.com/user-attachments/assets/f3d6072e-225e-4fe8-8b58-4f99e63b0e22)

   After putting XLeRobot robot description files to /agents/robots, add this line in /agents/robots/init.py
   ![image](https://github.com/user-attachments/assets/89c8fd71-2306-4963-8717-257795d8f8f1)
    
4. Add the control codes to /examples:
    
    ![image](https://github.com/user-attachments/assets/7b3c955e-bfa2-403e-9eb5-a3b3f9b52117)

    
5. Modify utils/scene_builder/replicacad/scenebulider.py: For new robot ids, you need to add them to ReplicaCAD scene first.

   ![image](https://github.com/user-attachments/assets/2beda6c3-71aa-4574-851b-e4e989fd4b6a)



#### Get Moving

```{note}
Change shader="default" to "rt-fast" for photo-realistic ray-tracing rendering (but slower).
```

##### Joint Control

```bash
python -m mani_skill.examples.demo_ctrl_action -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos_dual_arm"

```
![image](https://github.com/user-attachments/assets/11f6d417-9d1b-45d7-84c7-58b9d1611922)



##### End Effector Control 

Original dual-arm version:

```bash
python -m mani_skill.examples.demo_ctrl_action_ee_keyboard -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos_dual_arm"

```

Single-arm version:

```
python -m mani_skill.examples.demo_ctrl_action_ee_keyboard_single -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot_single"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos"
```

With Camera Visualization via Rerun:

```bash
python -m mani_skill.examples.demo_ctrl_action_ee_cam_rerun -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos_dual_arm"

```



![image](https://github.com/user-attachments/assets/12129988-e386-4d71-b1b2-79fe8492f419)

