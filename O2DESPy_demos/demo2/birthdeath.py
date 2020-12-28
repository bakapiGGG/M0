from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
from datetime import timedelta
import datetime
import time
import random

class BirthDeath(Sandbox):
    def __init__(self, hourly_birth_rate, hourly_death_rate, seed=0):
        super().__init__()
        self.__seed = seed
        self.__hourly_birth_rate = hourly_birth_rate
        self.__hourly_death_rate = hourly_death_rate
        self.__population = 0

        self.schedule([self.birth], timedelta(seconds=0))

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def hourly_birth_rate(self):
        return self.__hourly_birth_rate

    @property
    def hourly_death_rate(self):
        return self.__hourly_death_rate  

    @property
    def population(self):
        return self.__population
    
    def birth(self):
        self.__population += 1
        print("{0}\tBirth (Population: #{1}!)".format(self.clock_time, self.__population))
        Logger.info("{0}\tBirth (Population: #{1}!)".format(self.clock_time, self.__population))
        self.schedule([self.birth], timedelta(hours=round(random.expovariate(1 / self.__hourly_birth_rate),2)))
        self.schedule([self.death], timedelta(hours=round(random.expovariate(1 / self.__hourly_death_rate),2)))

    def death(self):
        self.__population -= 1
        print("{0}\tDeath (Population: #{1}!)".format(self.clock_time, self.__population))
        Logger.info("{0}\tDeath (Population: #{1}!)".format(self.clock_time, self.__population))

if __name__ == '__main__':
    run_code = 'O2DESPy demo 2'
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

    # Demo 2
    Logger.info("Demo 2 - Birth Death Process")
    sim2 = BirthDeath(20, 1, seed=1)
    sim2.warmup(till=datetime.datetime(year=1, month=1, day=1, hour=0, minute=0, second =0))
    # sim2.run(event_count=10)
    # sim2.run(speed=10)
    # sim2.run(terminate=datetime.datetime(year=1, month=1, day=1, hour=0, minute=5))
    sim2.run(duration=datetime.timedelta(hours=30))
    Logger.critical('use time {}'.format(time.time() - start_time))