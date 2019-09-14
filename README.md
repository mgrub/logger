requirements:

# Python
- Python > 3.7  (asyncio!)
- pip
- pyudev        (to monitor connected USB-devices)

# System
- git
- gpio   (obviously, to read Raspberry Pi GPIO-pins)
- pmount (for mounting USB-devices without sudo)

# setup
- copy the script "init_firstboot.sh" to your PC (i.e. take the text from github and paste it into an empty file)
- adjust the new hostname of your RPi
- adjust the mount points of the RPi-SD-card in that file
- run the script via "/bin/bash $HOME/path/to/init_firstboot.sh"
    - establish the git-repo in "/home/pi/logger" (either clones or updates)
    - enable a service "firstboot.service", which will headlessly setup your RPi
    - set the hostname of RPi

# usage
- PIN GPIO4 / PIN 7 is used (so far only changeable in the code itself)
- logger and usb-copy services are started with systemd after boot
- insert usb-device (fat32 / ext4), current logfile is automatically copied into a "logs"-folder on that drive

# Author
- Maximilian Gruber
