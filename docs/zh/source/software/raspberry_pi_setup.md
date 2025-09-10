# XLeRobot树莓派设置指南

本指南提供了为XLeRobot移动底座版本设置树莓派的详细说明。

## 先决条件

- 树莓派(推荐: Pi 4或更新版本)
- MicroSD卡(推荐32GB或更大)
- 带SD卡读卡器的计算机
- 网络连接(WiFi或以太网)

## 1. 安装操作系统

### 下载树莓派操作系统
1. 访问[官方树莓派网站](https://www.raspberrypi.org/software/)
2. 下载树莓派镜像工具
3. 下载树莓派操作系统(推荐: 带桌面的树莓派操作系统)

### 将操作系统刷写到SD卡
1. 将microSD卡插入计算机
2. 打开树莓派镜像工具
3. 选择下载的操作系统镜像
4. 选择您的SD卡
5. 点击"写入"刷写操作系统

### 初始设置
1. 将SD卡插入树莓派
2. 连接键盘、鼠标和显示器
3. 启动树莓派
4. 按照初始设置向导：
   - 设置国家、语言和时区
   - 创建用户账户和密码
   - 连接到WiFi网络
   - 更新系统包

```{note}
主机名选项定义您的树莓派使用mDNS向网络广播的主机名。当您将树莓派连接到网络时，网络上的其他设备可以使用`<hostname>`.local或`<hostname>`.lan与您的计算机通信。

用户名和密码选项定义您树莓派上管理员用户账户的用户名和密码。

无线局域网选项允许您输入无线网络的SSID(名称)和密码。如果您的网络不公开广播SSID，您应该启用"隐藏SSID"设置。默认情况下，镜像工具使用您当前所在的国家作为"无线局域网国家"。此设置控制您的树莓派使用的Wi-Fi广播频率。如果您计划运行无头树莓派，请输入无线局域网选项的凭据。

```

   <img src="https://www.raspberrypi.com/documentation/computers/images/imager/os-customisation-general.png?hash=6509321c9eebb02e53dd711c12395571" alt="树莓派操作系统自定义" width="700"/>


## 2. 设置VNC远程桌面

### 启用VNC服务器
1. 在树莓派上打开终端
2. 运行配置工具：
```bash
sudo raspi-config
```
3. 导航到"接口选项" → "VNC" → "启用"
4. 重启系统

### 替代方案：通过命令行启用VNC
```bash
sudo systemctl enable vncserver-x11-serviced
sudo systemctl start vncserver-x11-serviced
```

### 在您的PC上安装VNC查看器
1. 下载[RealVNC查看器](https://www.realvnc.com/en/connect/download/viewer/)
2. 安装并启动VNC查看器
3. 使用`<hostname>`.local或`<hostname>`.lan连接，对我来说是XLerobot.local **(确保这些设备在同一网络中)**
4. 使用您的Pi的用户名和密码进行身份验证

<img width="681" height="478" alt="image" src="https://github.com/user-attachments/assets/fd704e2e-2f79-4b88-96cd-c9d0b5f466b8" />

有关详细的VNC设置说明，请参考[此综合指南](https://www.raspberrypi.com/documentation/computers/remote-access.html#vnc)。

## 3. 系统更新和依赖项

### 更新系统包
```bash
sudo apt update
sudo apt upgrade -y
```

### 安装基本包
```bash
sudo apt install -y python3-pip git curl wget
```

## 4. 启用SSH访问(可选)

### 启用SSH
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

### 查找您的Pi的IP地址
```bash
hostname -I
```

### 从您的PC连接
```bash
ssh pi@<your-pi-ip-address>
```

## 5. 安装XLeRobot软件

按照官方[软件安装说明](https://huggingface.co/docs/lerobot/installation#install-lerobot-)获取详细步骤。

并复制[配置文件](https://xlerobot.readthedocs.io/en/latest/index.html)。

## 下一步

完成此设置后，您可以像笔记本电脑一样运行代码：

<img width="655" height="363" alt="image" src="https://github.com/user-attachments/assets/e4225cae-c012-4975-b7e7-577a7fd6510e" />

## 其他资源

- [官方树莓派文档](https://www.raspberrypi.org/documentation/)
- [RealVNC设置指南](https://pidoc.cn/docs/computers/getting-started)
- [XLeRobot GitHub仓库](https://xlerobot.readthedocs.io/en/latest/index.html)
