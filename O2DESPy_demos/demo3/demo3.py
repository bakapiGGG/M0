from O2DESPy.sandbox import Sandbox
import datetime
import random


class MMcQueue(Sandbox):
    def __init__(self, hourly_arrival_rate, hourly_service_rate, capacity, seed=0):
        super().__init__()
        random.seed(seed)
        self.hourly_arrival_rate = hourly_arrival_rate
        self.hourly_service_rate = hourly_service_rate
        self.capacity = capacity
        self.in_queue = 0
        self.in_service = 0

        self.schedule(self.arrive, datetime.timedelta(seconds=0))

    def arrive(self):
        if self.in_service < self.capacity:
            self.in_service += 1
            print("{0}\tArrive and Start Service (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.in_queue, self.in_service))
            self.schedule(self.depart, datetime.timedelta(hours=round(random.expovariate(1 / self.hourly_service_rate),2)))
        else:
            self.in_queue += 1
            print("{0}\tArrive and Join Queue (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.in_queue, self.in_service))
        self.schedule(self.arrive, datetime.timedelta(hours=round(random.expovariate(1 / self.hourly_arrival_rate),2)))

    def depart(self):
        if self.in_queue > 0:
            self.in_queue -= 1
            print("{0}\tDepart and Start Service (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.in_queue, self.in_service))
            self.schedule(self.depart, datetime.timedelta(hours=round(random.expovariate(1 / self.hourly_service_rate), 2)))
        else:
            self.in_service -= 1
            print("{0}\tDepart (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.in_queue, self.in_service))

    
if __name__ == '__main__':
    # Demo 3
    sim1 = MMcQueue(hourly_arrival_rate=1, hourly_service_rate=2, capacity=2)
    sim1.run(duration=datetime.timedelta(hours=30))
