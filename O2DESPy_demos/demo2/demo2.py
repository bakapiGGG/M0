from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
from datetime import timedelta
import datetime
import time
import random

# public class BirthDeath : Sandbox
class BirthDeath(Sandbox):
    # public BirthDeath(double hourlyBirthRate, double hourlyDeathRate, int seed = 0) : base(seed)
    def __init__(self, hourly_birth_rate, hourly_death_rate, seed=0):
        super().__init__()
        # Static
        self.__hourly_birth_rate = hourly_birth_rate
        self.__hourly_death_rate = hourly_death_rate
        # Dynamic
        self.__population = 0
        self.__seed = seed

        self.__hc = self.add_hour_counter()
        self.schedule([self.birth], timedelta(seconds=0))

    @property # getter
    def hourly_birth_rate(self):
        return self.__hourly_birth_rate
    
    @hourly_birth_rate.setter # setter
    def hourly_birth_rate(self, value):
        self.__hourly_birth_rate = value

    @property
    def hourly_death_rate(self):
        return self.__hourly_death_rate  
    
    @hourly_death_rate.setter
    def hourly_death_rate(self, value):
        self.__hourly_death_rate = value
    
    @property
    def population(self):
        return self.__population

    @population.setter
    def population(self, value):
        self.__population = value

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value
    
    @property
    def hc(self):
        return self.__hc
    
    def birth(self):
        self.__population += 1
        Logger.info("{0}\tBirth (Population: #{1}!".format(self.clock_time, self.__population))
        self.schedule([self.birth], timedelta(hours=round(random.expovariate(1 / self.__hourly_birth_rate))))
        self.schedule([self.death], timedelta(hours=round(random.expovariate(1 / self.__hourly_death_rate))))

    def death(self):
        self.__population -= 1
        Logger.info("{0}\tDeath (Population: #{1}!".format(self.clock_time, self.__population))

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
    sim2 = BirthDeath(15, 11, seed=3)
    hc2 = sim2.add_hour_counter()
    sim2.warmup(till=datetime.datetime(year=1, month=1, day=1, hour=0, minute=5))
    # sim1.run(event_count=10)
    # sim1.run(speed=10)
    # sim1.run(terminate=datetime.datetime(year=1, month=1, day=1, hour=0, minute=5))
    sim2.run(duration=datetime.timedelta(seconds=30))
    Logger.critical('use time {}'.format(time.time() - start_time))