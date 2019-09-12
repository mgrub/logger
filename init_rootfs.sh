#sudo apt-get install git

# manually change the directory of the rootfs, i.e.:
export ROOTFS=/media/maxwell/rootfs

# clone into git repo
cd $ROOTFS/home/pi
git clone https://github.com/mgrub/logger
cd logger

# copy unit-files
sudo cp logger_temp_warn.service $ROOTFS/etc/systemd/system/
sudo cp logger_usb_copy.service $ROOTFS/etc/systemd/system/

# enable systemd-services
cd $ROOTFS/etc/systemd/system/multi-user.target.wants
sudo ln -sf /etc/systemd/system/logger_usb_copy.service logger_usb_copy.service
sudo ln -sf /etc/systemd/system/logger_temp_warn.service logger_temp_warn.service

# which should be the equivalent to
#sudo systemctl enable logger_temp_warn.service 
#sudo systemctl enable logger_usb_copy.service
#sudo reboot