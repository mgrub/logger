import pyudev
import subprocess
import os
import shutil
import time
import datetime
import sys

def main():

    # path definitions
    orig_logfolder  = "/home/pi/logger"
    orig_logfile    = os.path.join(orig_logfolder, "logfile.csv")
    orig_uptime     = os.path.join(orig_logfolder, "uptime.csv")

    archive         = os.path.join(orig_logfolder, "archive")
    archive_logfile = os.path.join(archive, "log_{DATE}.csv")
    archive_uptime  = os.path.join(archive, "uptime_{DATE}.csv")

    try: 
        # monitor kernel for block-device messages
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='block')
        monitor.start()

        for device in iter(monitor.poll, None):
            if 'ID_FS_TYPE' in device:
                print('{0} partition {1} at {2}'.format(device.action, device.get('ID_FS_LABEL'), device.device_node))        

                if device.action == "add":
                    automount = False
                    time.sleep(1)  # give OS time to automount
                    
                    # check if device is already auto-mounted
                    p = subprocess.run(['lsblk', '-o', 'MOUNTPOINT', '-nr',  device.device_node], stdout=subprocess.PIPE)
                    stdout = p.stdout.decode("utf-8").replace("\n", "")  # p.stdout is byte-string with linebreaks

                    if stdout is not "":
                        print(stdout + " already mounted")
                        automount = True
                        mount_point = stdout
                    else:
                        mount_label = "flashdrive"
                        mount_point = os.path.join("/media", mount_label)

                    # define paths on the usb-device
                    dest_logfolder = os.path.join(mount_point, "logs")
                    dest_logfile   = os.path.join(dest_logfolder, "log_{DATE}.csv")
                    dest_uptime    = os.path.join(dest_logfolder, "uptime_{DATE}.csv")

                    # mount the block-device (pmount to mount without admin-rights)
                    if not automount:
                        subprocess.run(['pmount', device.device_node, mount_label])

                    # create destination-folder if necessary
                    if not os.path.exists(dest_logfolder):
                        os.mkdir(dest_logfolder)

                    # copy files
                    date = datetime.datetime.utcnow().strftime("%Y_%m_%d__%H_%M_%S")
                    if os.path.exists(orig_logfile):
                        shutil.copy(orig_logfile, dest_logfile.format(DATE=date))
                    else:
                        print("no logfile.csv")

                    if os.path.exists(orig_uptime):
                        shutil.copy(orig_uptime, dest_uptime.format(DATE=date))
                    else:
                        print("no uptime.csv")

                    # unmount device
                    if not automount:
                        subprocess.run(['pumount', device.device_node])

                    # create archive-folder if necessary
                    if not os.path.exists(archive):
                        os.mkdir(archive)

                    # move logfiles into archive
                    shutil.move(orig_logfile, archive_logfile.format(DATE=date))
                    shutil.move(orig_uptime, archive_uptime.format(DATE=date))

    except KeyboardInterrupt:
        print("Exiting. May leave mounted drives behind.")
        sys.exit(0)


if __name__ == '__main__':
    main()
