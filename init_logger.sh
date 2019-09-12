# install git
sudo apt-get install git

# clone into git repo
cd /home/pi
git clone https://github.com/mgrub/logger
cd logger

# copy unit-files
sudo cp logger_temp_warn.service /etc/systemd/system/
sudo cp logger_usb_copy.service /etc/systemd/system/

# enable systemd-services
sudo systemctl enable logger_temp_warn.service 
sudo systemctl enable logger_usb_copy.service 

# restart and hope for the best
sudo reboot
