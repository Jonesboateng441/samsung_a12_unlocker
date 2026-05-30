FROM kalilinux/kali-rolling

# Update and install tools
RUN apt update && apt upgrade -y && \
    apt install -y \
    android-tools-adb \
    android-tools-fastboot \
    python3 \
    python3-pip \
    git \
    wget \
    curl \
    usbutils \
    heimdall-flash \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Create udev rules for Samsung devices
RUN echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666"' > /etc/udev/rules.d/51-samsung.rules

# Set entrypoint
ENTRYPOINT ["python3", "src/main.py"]
