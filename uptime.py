import os
import time
import datetime


class loggerUptime():
    
    def __init__(self):
        # path definitions
        self.logfile = "/home/pi/logger/uptime.csv"
        self.interval = 10  # seconds


    def init_logfile(self):
        # init the file with a header
        if not os.path.exists(self.logfile):
            logtext = "DATE (UTC)\tTIME (UTC)\tMESSAGE\n"
            f = open(self.logfile, "w")
            f.write(logtext)
            f.close()


    def write_to_logfile(self, text, timestamp, overwriteLastLine=False):

        # human readable time, should be in local time
        #timestring = datetime.datetime.fromtimestamp(timestamp).astimezone().isoformat()

        # human readable date + time, in UTC
        d = datetime.datetime.utcfromtimestamp(timestamp)
        ts_date = d.strftime("%Y-%m-%d")
        ts_time = d.strftime("%H:%M:%S")

        # combine information into a single string
        logtext = "{DATE}\t{TIME}\t{TXT}\n".format(TXT=text, DATE=ts_date, TIME=ts_time)

        # write to file (seems complicated, but this way only the last line 
        # is touched, instead of a full rewrite of the file.)
        print(logtext)

        if overwriteLastLine:

            # remove last line
            number = 1  # number of lines to be removed
            count = 0
            SEEK_CUR = 1
            SEEK_END = 2
            
            f = open(self.logfile, "r+b")
            f.seek(0, SEEK_END)
            end = f.tell()

            # check for linebreaks starting at the end
            while f.tell() > 0:
                f.seek(-1, SEEK_CUR)
                char = f.read(1)

                if char != b'\n' and f.tell() == end:
                    print("No change: file does not end with a newline")
                    break

                if char == b'\n':
                    count += 1

                if count == number + 1:
                    f.truncate()
                    break

                f.seek(-1, SEEK_CUR)

            f.close()
            
        # append to logfile
        f = open(self.logfile, "a")
        f.write(logtext)
        f.close()


    def main(self):
        # write down power-on
        self.write_to_logfile("POWER ON", time.time())
        self.write_to_logfile("POWER OFF", time.time())

        # update the shutoff-time roughly every 60s
        # (so that the most recent line will persist in case of power-off)
        while True:
            time.sleep(self.interval)

            # re-initizalize the file if necessary
            if not os.path.exists(self.logfile):
                self.init_logfile()
                self.write_to_logfile("POWER OFF", time.time())

            self.write_to_logfile("POWER OFF", time.time(), overwriteLastLine=True)



if __name__ == '__main__':
    lu = loggerUptime()
    lu.main()
