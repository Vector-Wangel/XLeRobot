# RaspberryPi Setup Guide for XLeRobot

This guide provides comprehensive instructions for setting up a RaspberryPi for use with XLeRobot mobile base version.

## Prerequisites

- RaspberryPi (recommended: Pi 4 or newer)
- MicroSD card (32GB or larger recommended)
- Computer with SD card reader
- Network connection (WiFi or Ethernet)

## 1. Installing the Operating System

### Download Raspberry Pi OS
1. Visit the [official Raspberry Pi website](https://www.raspberrypi.org/software/)
2. Download Raspberry Pi Imager
3. Download Raspberry Pi OS (recommended: Raspberry Pi OS with desktop)

### Flash the OS to SD Card
1. Insert your microSD card into your computer
2. Open Raspberry Pi Imager
3. Select the downloaded OS image
4. Select your SD card
5. Click "Write" to flash the OS

### Initial Setup
1. Insert the SD card into your RaspberryPi
2. Connect keyboard, mouse, and monitor
3. Power on the RaspberryPi
4. Follow the initial setup wizard:
   - Set country, language, and timezone
   - Create user account and password
   - Connect to WiFi network
   - Update system packages

```{note}
The hostname option defines the hostname your Raspberry Pi broadcasts to the network using mDNS. When you connect your Raspberry Pi to your network, other devices on the network can communicate with your computer using `<hostname>`.local or `<hostname>`.lan.

The username and password option defines the username and password of the admin user account on your Raspberry Pi.

The wireless LAN option allows you to enter an SSID (name) and password for your wireless network. If your network does not broadcast an SSID publicly, you should enable the "Hidden SSID" setting. By default, Imager uses the country you’re currently in as the "Wireless LAN country". This setting controls the Wi-Fi broadcast frequencies used by your Raspberry Pi. Enter credentials for the wireless LAN option if you plan to run a headless Raspberry Pi.

```

   <img src="https://www.raspberrypi.com/documentation/computers/images/imager/os-customisation-general.png?hash=6509321c9eebb02e53dd711c12395571" alt="Raspberry Pi OS Customisation" width="700"/>


## 2. Setting Up VNC for Remote Desktop

### Enable VNC Server
1. Open Terminal on RaspberryPi
2. Run the configuration tool:
```bash
sudo raspi-config
```
3. Navigate to "Interface Options" → "VNC" → "Enable"
4. Reboot the system

### Alternative: Enable VNC via Command Line
```bash
sudo systemctl enable vncserver-x11-serviced
sudo systemctl start vncserver-x11-serviced
```

### Install VNC Viewer on Your PC
1. Download [RealVNC Viewer](https://www.realvnc.com/en/connect/download/viewer/)
2. Install and launch VNC Viewer
3. Connect using `<hostname>`.local or `<hostname>`.lan, for me is XLerobot.local **(Make sure these devices are in the same network)**
4. Use your Pi's username and password to authenticate

<img width="681" height="478" alt="image" src="https://github.com/user-attachments/assets/fd704e2e-2f79-4b88-96cd-c9d0b5f466b8" />

For detailed VNC setup instructions, refer to [this comprehensive guide](https://www.raspberrypi.com/documentation/computers/remote-access.html#vnc).

## 3. System Updates and Dependencies

### Update System Packages
```bash
sudo apt update
sudo apt upgrade -y
```

### Install Essential Packages
```bash
sudo apt install -y python3-pip git curl wget
```

## 4. Enable SSH Access (Optional)

### Enable SSH
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

### Find Your Pi's IP Address
```bash
hostname -I
```

### Connect from Your PC
```bash
ssh pi@<your-pi-ip-address>
```

## 5. Installing XLeRobot Software

Follow the official [software installation instructions](https://huggingface.co/docs/lerobot/installation#install-lerobot-) for detailed steps.

And copy the [config files](https://xlerobot.readthedocs.io/en/latest/index.html).

## Next Steps

After completing this setup, you can run the code in the same way as the laptop:

<img width="655" height="363" alt="image" src="https://github.com/user-attachments/assets/e4225cae-c012-4975-b7e7-577a7fd6510e" />

## Additional Resources

- [Official Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [RealVNC Setup Guide](https://pidoc.cn/docs/computers/getting-started)
- [XLeRobot GitHub Repository](https://xlerobot.readthedocs.io/en/latest/index.html)
