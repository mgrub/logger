requirements:

# Python
- Python > 3.7  (asyncio!)
- pyudev        (to monitor connected USB-devices)

# System
- gpio   (obviously, to read Raspberry Pi GPIO-pins)
- pmount (for mounting USB-devices without sudo)

# setup
- set timezone with "sudo raspi-config"
- copy code from github
- adjust PIN-number
- add both scripts to systemctl. --> explain how (TODO)

# usage
- run logger
- insert usb-device, current logfile is automatically copied into a "logs"-folder on that drive
