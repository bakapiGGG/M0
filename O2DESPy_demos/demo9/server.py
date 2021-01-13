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
        self.number_pending = 0
        self.number_in_service = 0
        self.on_start = self.create_event()
        self.on_ready_to_finish = self.create_event()

    def request_to_start(self):
        self.number_pending += 1
        print("{0}\t{1}\tRequestToStart. #Pending Server: {2}. #In-Service: {3}. Server id: {4}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_in_service, self.server_id))
        if self.number_in_service < self.capacity:
            self.start()

    def start(self):
        self.number_pending -= 1
        self.number_in_service += 1
        print("{0}\t{1}\tStart. #Pending Server: {2}. #In-Service: {3}. Server id: {4}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_in_service, self.server_id))
        self.schedule(self.ready_to_finish, timedelta(hours=round(random.expovariate(1 / self.hourly_service_rate),2)))
        self.invoke(self.on_start)

    def ready_to_finish(self):
        print("{0}\t{1}\tReadyToFinish. #Pending Server: {2}. #In_Service: {3}. Server id: {4}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_in_service, self.server_id))
        self.invoke(self.on_ready_to_finish)
    
    def finish(self):
        print("{0}\t{1}\tFinish. #Pending Server: {2}. #In_Service: {3}. Server id: {4}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_in_service, self.server_id))
        self.number_in_service -= 1
        if self.number_pending > 0:
            self.start()
