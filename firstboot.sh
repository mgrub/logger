#!/bin/bash

# install dependecies
sudo apt-get update
sudo apt-get -y install git pmount python3 python3-pip
pip3 install pyudev

# setup time
sudo timedatectl set-ntp True

# the repository was already cloned during init_firstboot.sh
# git clone https://github.com/mgrub/logger
cd $HOME/logger

# copy unit-files
sudo cp logger_temp_warn.service /etc/systemd/system/
sudo cp logger_usb_copy.service /etc/systemd/system/
sudo cp logger_uptime.service /etc/systemd/system/

# enable and start the services
sudo systemctl enable logger_temp_warn.service --now
sudo systemctl enable logger_usb_copy.service --now
sudo systemctl enable logger_uptime.service --now
