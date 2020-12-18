from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
from datetime import timedelta
import datetime
import time
import random


class HelloWorld(Sandbox):
    def __init__(self, hourly_arrival_rate, seed=0):
        super().__init__()
        self.__hourly_arrival_rate = hourly_arrival_rate
        self.__count = 0
        self.__seed = seed
        self.__hc = self.add_hour_counter()

        self.schedule([self.arrive], timedelta(seconds=0))

    @property
    def hourly_arrival_rate(self):
        return self.__hourly_arrival_rate

    @hourly_arrival_rate.setter
    def hourly_arrival_rate(self, value):
        self.__hourly_arrival_rate = value

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def hc(self):
        return self.__hc

    def arrive(self):
        Logger.info("{0}\tHello World #{1}!".format(self.clock_time, self.__count))
        self.__count += 1
        # self.schedule([self.arrive], timedelta(seconds=round(random.expovariate(1 / self.__hourly_arrival_rate))))
        self.schedule([self.arrive], timedelta(hours=5))


if __name__ == '__main__':
    run_code = 'O2DESPy demo 1'
    start_time = time.time()

    Logger.debug("Init time: {}".format(time.time() - start_time))
    Logger.critical('Run: {}'.format(run_code))
    Logger.update_config(
        file_path=Config.log_file_path,
        dynamic=True,
        include_log=['debug', 'info', 'warning', 'error', 'critical'],
        name=run_code,
        stream_level='critical',
        output_mode=['stream', 'file'],
        file_level='debug',
        fmt='%(levelname)s: %(message)s')

    # Demo 1
    Logger.info("Demo 1 - Hello world")
    sim1 = HelloWorld(10, seed=3)
    hc1 = sim1.add_hour_counter()
    sim1.warmup(till=datetime.datetime(year=1, month=1, day=1, hour=0, minute=5))
    # sim1.run(event_count=10)
    # sim1.run(speed=10)
    # sim1.run(terminate=datetime.datetime(year=1, month=1, day=1, hour=0, minute=5))
    sim1.run(duration=datetime.timedelta(hours=30))
    Logger.critical('use time {}'.format(time.time() - start_time))
