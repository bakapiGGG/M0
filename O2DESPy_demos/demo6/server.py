from O2DESPy.sandbox import Sandbox
from datetime import timedelta
import random


class Server(Sandbox):
    def __init__(self, capacity, hourly_service_rate, seed=0):
        super().__init__()
        self.capacity = capacity
        self.hourly_service_rate = hourly_service_rate
        self.number_in_service = 0
        self.seed = seed
        self.on_change_accessibility = self.create_event()
    
    def start(self):
        if self.number_in_service >= self.capacity:
            return "Insufficient Vacancy."
        self.number_in_service += 1
        print("{0}\t{1}\tStart. #In-Service: {2}".format(self.clock_time, type(self).__name__, self.number_in_service))
        self.schedule(self.finish, timedelta(hours=round(random.expovariate(1 / self.hourly_service_rate))))
        if self.number_in_service == self.capacity:
            self.schedule(self.change_accessibility)

    def finish(self):
        self.number_in_service -= 1
        print("{0}\t{1}\tFinish. #In_Service: {2}".format(self.clock_time, type(self).__name__, self.number_in_service))
        if self.number_in_service == self.capacity - 1:
            self.schedule(self.change_accessibility)

    def change_accessibility(self):
        self.invoke(self.on_change_accessibility)
