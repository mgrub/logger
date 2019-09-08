import pyudev
import subprocess
import os
import shutil
import datetime
import sys

def main():

    # path definitions
    mount_label = "flashdrive"
    mount_point = os.path.join("/media", mount_label)

    orig_logfolder = os.getcwd()
    orig_logfile   = os.path.join(orig_logfolder, "logfile.csv")

    dest_logfolder = os.path.join(mount_point, "logs")
    dest_logfile   = os.path.join(dest_logfolder, "log_{DATE}.csv")

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

                    # mount the block-device
                    subprocess.call(['pmount', device.device_node, mount_label])

                    # create folder if necessary
                    if not os.path.exists(dest_logfolder):
                        os.mkdir(dest_logfolder)

                    # copy file
                    date = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
                    shutil.copy(orig_logfile, dest_logfile.format(DATE=date))

                    # unmount device
                    subprocess.call(['pumount', mount_label])

    except KeyboardInterrupt:
        print("Exiting. May leave mounted drives behind.")
        sys.exit(0)


if __name__ == '__main__':
    main()
