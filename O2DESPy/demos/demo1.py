from sandbox import Sandbox
from log.logger import Logger
from datetime import timedelta
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
        self.schedule([self.arrive], timedelta(seconds=5))



