from O2DESPy.sandbox import Sandbox
from datetime import timedelta
import random


class Generator(Sandbox):
    def __init__(self, hourly_rate, seed=0):
        super().__init__()
        random.seed(seed)
        self.hourly_rate = hourly_rate
        self.count = 0
        self.on_generate = self.create_event()
        
        self.schedule(self.generate)

    def generate(self):
        if self.count > 0:
            print("{0}\t{1}\tGenerate. Count: {2}".format(self.clock_time, type(self).__name__, self.count))
            self.invoke(self.on_generate)
        self.count += 1
        self.schedule(self.generate, timedelta(hours=round(random.expovariate(1 / self.hourly_rate),2)))
