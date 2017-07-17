#!/bin/bash

project_dir="$( readlink -f "$( dirname "$0")/.." )"
setup_dir="$project_dir/setup"

cd "$project_dir"

if [[ "$EUID" != 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

sudo -u pi git submodule init && sudo -u pi git submodule update
sudo apt-get install -y python-dev libjpeg-dev python-pip libfreetype6-dev fonts-dejavu-core python-numpy
pip install -r requirements.txt

setup_tsl2591() {
    cd "$project_dir/"python-tsl2591/
    python setup.py install
    cd "$project_dir"
}

setup_Adafruit_Python_BME280() {
    cd "$project_dir/"Adafruit_Python_BME280
    python setup.py install
    cd "$project_dir"
}

enable_spi() {
    sed -i 's/dtparam=spi=.*//g' /boot/config.txt
    echo dtparam=spi=on >> /boot/config.txt
}

enable_hwclock() {
    sed -i 's/dtparam=i2c_arm=.*//g' /boot/config.txt
    echo dtparam=i2c_arm=on >> /boot/config.txt
    sed -i 's/dtoverlay=i2c-rtc.*//g' /boot/config.txt
    read -e -i "ds3231" -p "Enter RTC module to be used: " rtc_module
    echo "dtoverlay=i2c-rtc,$rtc_module" >> /boot/config.txt
    apt-get purge -y fake-hwclock
    grep -q i2c-dev /etc/modules || echo 'i2c-dev' >> /etc/modules
    cp "$setup_dir"/hwclock/hwclock.service /etc/systemd/system/
    systemctl enable hwclock && systemctl start hwclock 
}

disable_audio() {
    sed -i 's/dtparam=audio=on/dtparam=audio=off/g' /boot/config.txt
}


disable_audio() {
    sed -i 's/dtparam=audio=on/dtparam=audio=off/g' /boot/config.txt
}

enable_ssh() {
    touch /boot/ssh
}



setup_hdmi() {
    cp "$setup_dir"/hdmi-control/hdmi-control /usr/bin
    cp "$setup_dir"/hdmi-control/hdmi-control.service /etc/systemd/system
    read -e -n 1 -p "Disable HDMI port on system startup? (saves a few mA of current) [Y/n] " disable_hdmi
    [ "$disable_hdmi" == n ] && HDMI_ENABLED=1 || HDMI_ENABLED=0
    echo "export HDMI_ENABLED=$HDMI_ENABLED" > /etc/hdmi-control.conf
    systemctl daemon-reload
    systemctl enable hdmi-control
    systemctl restart hdmi-control
}

setup_g_ether() {
    cp "$setup_dir"/ethernet-gadget /usr/local/bin 
    echo "Run 'ethernet-gadget to switch to and from ethernet-gadget OTG mode"
}

setup_ledctl() {
    cp "$setup_dir"/ledctl/ledctl.service /etc/systemd/system
    cp "$setup_dir"/ledctl/toggle-actled /usr/local/bin
    systemctl daemon-reload
    systemctl enable ledctl
    systemctl restart ledctl
}

setup_autostart() {
    cp "$setup_dir/sqm-weather.service" /etc/systemd/system
    systemctl enable sqm-weather.service
    echo "To start the daemon, type:"
    echo "  sudo systemctl start sqm-weather"
}

setup_tsl2591
pwd
setup_Adafruit_Python_BME280
enable_spi
enable_hwclock
disable_audio
enable_ssh
setup_hdmi
setup_g_ether
setup_ledctl
setup_autostart

