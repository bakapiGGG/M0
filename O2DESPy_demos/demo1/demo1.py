from O2DESPy.sandbox import Sandbox
import datetime
import random


class HelloWorld(Sandbox):
    def __init__(self, hourly_arrival_rate, seed=0):
        super().__init__()
        random.seed(seed)
        self.hourly_arrival_rate = hourly_arrival_rate
        self.count = 0

        self.schedule(self.arrive)

    def arrive(self):
        print("{0}\tHello World #{1}!".format(self.clock_time, self.count))
        self.count += 1
        self.schedule(self.arrive, datetime.timedelta(hours=round(random.expovariate(1 / self.hourly_arrival_rate),2)))


if __name__ == '__main__':
    # Demo 1
    sim1 = HelloWorld(1, seed=1)
    sim1.warmup(till=datetime.datetime(year=1, month=1, day=1, hour=0, minute=0, second=0))
    sim1.run(duration=datetime.timedelta(hours=12))
    # sim1.run(event_count=10)
    # sim1.run(speed=10)
    # sim1.run(terminate=datetime.datetime(year=1, month=1, day=2, hour=0, minute=0))
