from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
from datetime import timedelta
import datetime
import time
import random

class PingPongPlayer(Sandbox):
    def __init__(self, index, delay_time_expected, delay_time_CV, seed=0):
        super().__init__()
        self.__index = index
        self.__delay_time_expected = delay_time_expected
        self.__delay_time_CV = delay_time_CV
        self.__seed = seed 
        self.__count = 0
        self.__on_send = []
    
    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        self.__index = value

    @property
    def delay_time_expected(self):
        return self.__delay_time_expected

    @index.setter
    def delay_time_expected(self, value):
        self.__delay_time_expected = value
    
    @property
    def delay_time_CV(self):
        return self.__delay_time_CV

    @index.setter
    def delay_time_CV(self, value):
        self.__delay_time_CV = value
    
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def count(self):
        return self.__count
    
    @property
    def on_send(self):
        return self.__on_send

    @index.setter
    def on_send(self, value):
        self.__on_send.append(value)

    def send(self):
        print(f"{self.clock_time}\t Send. Player #{self.__index}, Count: {self.__count}")
        for func in self.__on_send:
                if len(func) == 1:
                    func[0]()
                else:
                    func[0](**func[1])
    
    def receive(self):
        self.__count += 1
        print(f"{self.clock_time}\t Receive. Player #{self.__index}, Count: {self.__count}")
        self.schedule([self.send], timedelta(seconds=round(random.gammavariate(self.delay_time_expected,self.delay_time_CV))))



