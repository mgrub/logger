import asyncio
import time


class Logger():

    def __init__(self, BCM_PIN=4):
        self.bounce_time = 1  # seconds

        self.last_rising_edge = 0.0
        self.last_falling_edge = 0.0

        # RPi settings
        self.PIN = BCM_PIN

        # bare gpio-cli commands (-g --> use BCM-numbers)
        self.cmd_enable_read    = "gpio -g mode {PIN} input".format(PIN=self.PIN)  # input/output/up/down/tri
        self.cmd_detect_rising  = "gpio -g wfi {PIN} rising".format(PIN=self.PIN)  # rising/falling/both
        self.cmd_detect_falling = "gpio -g wfi {PIN} falling".format(PIN=self.PIN)
        

    async def on_rising_edge(self, timestamp):
        tmp = self.last_rising_edge
        self.last_rising_edge = timestamp

        # only log, if the last falling edge was more than bounce_time seconds in the past
        if timestamp - tmp > self.bounce_time:
            self.write_to_logfile("AN", timestamp)


    async def on_falling_edge(self, timestamp):
        self.last_falling_edge = timestamp

        # only log, if after a wait of bounce_time the last falling edge wasn't updated
        await asyncio.sleep(self.bounce_time)

        # self.last_falling_edge could have been altered by another call of on_falling_edge in the meantime
        if self.last_falling_edge - timestamp == 0:
            self.write_to_logfile("AUS", timestamp)


    def write_to_logfile(self, text, timestamp):
        logtext = "{TS}, {TXT}\n".format(TXT=text, TS=timestamp)

        print(logtext)
        #f = open("logfile.csv", "a")
        #f.write(logtext)
        #f.close()


    async def detect_rising_edge(self, PIN, future_timestamp):
        await asyncio.sleep(2)

        # return the value asynchronously
        future_timestamp.set_result(time.time())


    async def detect_falling_edge(self, PIN, future_timestamp):
        #GPIO.wait_for_edge(PIN, GPIO.FALLING)
        await asyncio.sleep(4)

        # return the value asynchronously
        future_timestamp.set_result(time.time())


    async def detection_cycle(self, loop, start_next_cycle):
        # create elements to store the future result of edge-detection
        rising_edge      = loop.create_future()
        falling_edge     = loop.create_future()
        
        # create task to detect edge and do something with result
        loop.create_task(self.detect_rising_edge(self.PIN, rising_edge))
        loop.create_task(self.detect_falling_edge(self.PIN, falling_edge))
        
        await rising_edge
        start_next_cycle.set_result(True)

        await loop.create_task(self.on_rising_edge(await rising_edge))
        await loop.create_task(self.on_falling_edge(await falling_edge))


    async def run(self, cmd):
        proc = await asyncio.create_subprocess_shell(cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')


async def main():
    
    logger = Logger()

    # set PIN into input mode
    await logger.run(logger.cmd_enable_read)

    loop = asyncio.get_event_loop()

    for i in range(5):
        start_next_cycle = loop.create_future()
        loop.create_task(logger.detection_cycle(loop, start_next_cycle))

        await start_next_cycle

    
    #loop.run_forever()
    #loop.close()

if __name__ == "__main__":
    asyncio.run(main())
