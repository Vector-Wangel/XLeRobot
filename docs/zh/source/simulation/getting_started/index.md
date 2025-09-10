# 开始使用

### 前提条件

- Ubuntu操作系统
- 基本熟悉终端命令
- [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) (推荐)

### 安装

#### 1. 创建Conda环境

如果您已经有一个`lerobot` conda环境，可以使用该环境。否则，创建一个新环境：

```bash
conda create -y -n lerobot python=3.11
conda activate lerobot

```

> 注意：建议将ManiSkill和lerobot代码放在同一个环境中，以便未来的sim2real部署。
> 

#### 2. 安装ManiSkill

按照ManiSkill的[官方安装说明](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/installation.html)进行安装。

```bash
# 基本安装
pip install mani-skill

# 下载场景数据集
python -m mani_skill.utils.download_asset "ReplicaCAD"

```

如果数据集下载出现问题，您可以直接从[这个Google Drive链接](https://drive.google.com/file/d/1mqImztNX1LYZFBzt9z895C814RsyGe4N/view?usp=sharing)下载数据集。然后文件夹内容应该放到

```bash
~/.maniskill/data/scene_datasets/replica_cad_dataset

```

使用[快速入门指南](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/quickstart.html)和[演示脚本](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/quickstart.html)熟悉ManiSkill。

尝试此命令来测试您是否成功安装了ManiSkill：

```{note}
将shader="rt-fast"更改为"default"以获得更快的渲染，或者如果您的计算机不支持光线追踪渲染。
```

```bash
python -m mani_skill.examples.demo_random_action -e "ReplicaCAD_SceneManipulation-v1" \\
  --render-mode="human" --shader="rt-fast"

```

您应该看到类似这样的内容：

![image](https://github.com/user-attachments/assets/c7509843-f037-4f37-9b1c-e7cad939037c)

#### 3. 额外依赖

我们使用pygame来读取键盘输入并实时显示控制面板，使用Rerun来可视化和收集相机数据。

```bash
pip install pygame
pip install rerun-sdk
```

#### 4. 将XLeRobot文件放入ManiSkill

```{note}
我们期待ManiSkill很快为XLeRobot提供官方支持，之后可以跳过此步骤。
```

导航到您conda环境中的ManiSkill包文件夹：

```bash
cd ~/miniconda3/envs/lerobot/lib/python3.10/site-packages/mani_skill
```

将XLeRobot文件放入ManiSkill文件夹：

1. 在[这里下载**XLeRobot机器人文件**](https://github.com/Vector-Wangel/XLeRobot/tree/main/simulation/Maniskill)：
2. 将文件放入/agents/robots、/assets/robots和/envs/scenes：
   ![image](https://github.com/user-attachments/assets/59ae0104-7b9b-441a-a526-e9d0e2f99278)
   
   ![image](https://github.com/user-attachments/assets/a9107171-193b-485c-9620-f453e03f8f56)

   ![image](https://github.com/user-attachments/assets/f3d6072e-225e-4fe8-8b58-4f99e63b0e22)

   将XLeRobot机器人描述文件放入/agents/robots后，在/agents/robots/init.py中添加这一行
   ![image](https://github.com/user-attachments/assets/89c8fd71-2306-4963-8717-257795d8f8f1)
    
4. 将控制代码添加到/examples：
    
    ![image](https://github.com/user-attachments/assets/7b3c955e-bfa2-403e-9eb5-a3b3f9b52117)

    
5. 修改utils/scene_builder/replicacad/scenebulider.py：对于新的机器人id，您需要先将它们添加到ReplicaCAD场景中。

   ![image](https://github.com/user-attachments/assets/2beda6c3-71aa-4574-851b-e4e989fd4b6a)
    

#### 开始运行

```{note}
将shader="default"更改为"rt-fast"以获得照片级真实感光线追踪渲染(但更慢)。
```

##### 关节控制

```bash
python -m mani_skill.examples.demo_ctrl_action -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos_dual_arm"

```
![image](https://github.com/user-attachments/assets/11f6d417-9d1b-45d7-84c7-58b9d1611922)



##### 末端执行器控制 

原始双臂版本：

```bash
python -m mani_skill.examples.demo_ctrl_action_ee_keyboard -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos_dual_arm"

```

单臂版本：

```
python -m mani_skill.examples.demo_ctrl_action_ee_keyboard_single -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot_single"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos"
```

通过Rerun进行相机可视化：

```bash
python -m mani_skill.examples.demo_ctrl_action_ee_cam_rerun -e "ReplicaCAD_SceneManipulation-v1" -r "xlerobot"  --render-mode="human" --shader="default" -c "pd_joint_delta_pos_dual_arm"

```



![image](https://github.com/user-attachments/assets/12129988-e386-4d71-b1b2-79fe8492f419)

