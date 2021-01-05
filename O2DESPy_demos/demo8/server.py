from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from datetime import timedelta
import random


class Server(Sandbox):
    def __init__(self, capacity, hourly_service_rate, server_id, seed=0):
        super().__init__()
        random.seed(seed)
        self.capacity = capacity
        self.hourly_service_rate = hourly_service_rate
        self.server_id = server_id
        self.number_in_service = 0
        self.on_change_accessibility = self.create_event()
        self.on_finish = self.create_event()
    
    def start(self):
        if self.number_in_service >= self.capacity:
            return "Insufficient Vacancy."
        self.number_in_service += 1
        print("{0}\t{1}\tStart. #In-Service: {2}. Server id: {3}".format(self.clock_time, type(self).__name__, self.number_in_service, self.server_id))
        self.schedule(self.finish, timedelta(hours=round(random.expovariate(1 / self.hourly_service_rate),2)))
        if self.number_in_service == self.capacity:
            self.schedule(self.change_accessibility)

    def finish(self):
        self.number_in_service -= 1
        print("{0}\t{1}\tFinish. #In_Service: {2}. Server id: {3}".format(self.clock_time, type(self).__name__, self.number_in_service, self.server_id))
        if self.number_in_service == self.capacity - 1:
            self.schedule(self.change_accessibility)
        self.invoke(self.on_finish)

    def change_accessibility(self):
        print("{0}\t{1}\tChangeAccessibility. #In_Service: {2}. Server id: {3}".format(self.clock_time, type(self).__name__, self.number_in_service, self.server_id))
        self.invoke((self.on_change_accessibility, self.number_in_service < self.capacity))
