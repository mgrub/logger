# This script prepares a service on the SD-card, that will launch the 
# one-time-run firstboot.service on first start of the RPi. 
# It allows to setup the RPi without keyboard/ssh-access.

#### init ####
CWD=$(pwd)

# new hostname of the RPi
NEW_NAME="Logger_01"

# define the mount points of the boot and rootfs partitions on the RPi-SD-card
ROOTFS="/media/$USER/rootfs"
BOOTFS="/media/$USER/boot"

# directories of interest
PI_HOME="$ROOTFS/home/pi"
LOGGER="$PI_HOME/logger"


#### main ####

# clone into git repo
cd $PI_HOME
if [ -d "$LOGGER" ]; then
  cd $LOGGER
  #git pull origin master
  echo "$LOGGER already exists. Assuming it is a git-repo with user-modified content. \nPlease ensure, that firstboot.sh and firstboot.service exist."
else
  git clone https://github.com/mgrub/logger
fi

# copy the script itself and the unit-file
cp $LOGGER/firstboot.sh $BOOTFS
sudo cp $LOGGER/firstboot.service $ROOTFS/etc/systemd/system/

# enable systemd-services
cd $ROOTFS/etc/systemd/system/multi-user.target.wants
sudo ln -sf /etc/systemd/system/firstboot.service firstboot.service  # (does the same as: sudo systemctl enable firstboot.service)

# change hostname
echo $NEW_NAME | sudo tee $ROOTFS/etc/hostname
sudo sed -i "s/raspberrypi/$NEW_NAME/g" $ROOTFS/etc/hosts

CD $CWD
