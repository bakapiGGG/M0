from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from datetime import timedelta
import random

class Generator(Sandbox):
    def __init__(self, hourly_rate, seed=0):
        super().__init__()
        self.__hourly_rate = hourly_rate
        self.__count = 0
        self.__seed = seed
        self.__on_generate = []
        
        self.schedule([self.generate], timedelta(seconds=0))

    @property
    def hourly_rate(self):
        return self.__hourly_rate

    @property
    def count(self):
        return self.__count
    
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def on_generate(self):
        return self.__on_generate

    @on_generate.setter
    def on_generate(self, value):
        self.__on_generate.append(value)

    def generate(self):
        if self.__count > 0:
            print("{0}\t{1}\tGenerate. Count: {2}".format(self.clock_time, type(self).__name__, self.__count))
            Logger.info("{0}\t{1}\tGenerate. Count: {2}".format(self.clock_time, type(self).__name__, self.__count))
            for func in self.__on_generate:
                if len(func) == 1:
                    func[0]()
                else:
                    func[0](**func[1])
        self.__count += 1
        self.schedule([self.generate], timedelta(hours=round(random.expovariate(1 / self.__hourly_rate))))