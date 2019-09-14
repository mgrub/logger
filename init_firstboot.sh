# This script prepares a service on the SD-card, that will launch the 
# one-time-run firstboot.service on first start of the RPi. 
# It allows to setup the RPi without keyboard/ssh-access.

# define the mount points of the boot and rootfs partitions on the RPi-SD-card
export ROOTFS=/media/$USER/rootfs
export BOOTFS=/media/$USER/boot

# directories of interest
export PI_HOME=$ROOTFS/home/pi
export LOGGER=$PI_HOME/logger

# clone into git repo
cd $PI_HOME
git clone https://github.com/mgrub/logger

# copy the script itself and the unit-file
sudo cp $LOGGER/firstrun.sh $BOOTFS
sudo cp $LOGGER/firstrun.service $ROOTFS/etc/systemd/system/

# enable systemd-services
cd $ROOTFS/etc/systemd/system/multi-user.target.wants
sudo ln -sf /etc/systemd/system/firstboot.service firstboot.service

# does the same as: sudo systemctl enable firstboot.service

# change hostname
NEW_NAME="Logger_01"
echo $NEW_NAME > $ROOTFS/etc/hostname
sed -i "s/raspberrypi/$NEW_NAME/g" $ROOTFS/etc/hosts
hostname $NEW_NAME

