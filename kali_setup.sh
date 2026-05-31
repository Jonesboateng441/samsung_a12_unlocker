#!/bin/bash
# kali_setup.sh - Setup script for Kali Linux

echo "[+] Setting up Samsung A12 Unlock Tool on Kali Linux"

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    android-tools-adb \
    android-tools-fastboot \
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    heimdall-flash \
    libusb-1.0-0-dev \
    usbutils

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup USB permissions for Samsung devices
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666"' | sudo tee /etc/udev/rules.d/51-samsung.rules

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Download additional tools and wordlists
mkdir -p tools wordlists

# Download common wordlists for brute force
wget https://github.com/danielmiessler/SecLists/archive/master.zip -O wordlists/seclists.zip
unzip wordlists/seclists.zip -d wordlists/

# Download Samsung firmware tools
wget https://github.com/ivanmeler/samsung_firmware_downloader/archive/main.zip -O tools/firmware_tool.zip

echo "[+] Setup complete!"
echo "[+] To activate virtual environment: source venv/bin/activate"
echo "[+] To run the tool: python src/main.py"
