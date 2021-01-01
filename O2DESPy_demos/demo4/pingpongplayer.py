from O2DESPy.sandbox import Sandbox
import datetime
import random


class PingPongPlayer(Sandbox):
    def __init__(self, index, delay_time_expected, delay_time_CV, seed=0):
        super().__init__()
        self.__index = index
        self.delay_time_expected = delay_time_expected
        self.delay_time_CV = delay_time_CV
        self.seed = seed
        self.count = 0
        self.on_send = self.create_event()

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        self.__index = value

    def send(self):
        print(f"{self.clock_time}\t Send. Player #{self.__index}, Count: {self.count}")
        self.invoke(self.on_send)

    def receive(self):
        self.count += 1
        print(f"{self.clock_time}\t Receive. Player #{self.__index}, Count: {self.count}")
        self.schedule(self.send, datetime.timedelta(seconds=round(random.gammavariate(self.delay_time_expected, self.delay_time_CV))))
