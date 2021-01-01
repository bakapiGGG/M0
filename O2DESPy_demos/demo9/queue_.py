from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger


class Queue(Sandbox):
    def __init__(self, capacity, seed=0):
        super().__init__()
        self.capacity = capacity
        self.seed = seed
        self.number_waiting = 0
        self.number_pending = 0
        self.on_enqueue = self.create_event()

    def request_to_enqueue(self):
        self.number_pending += 1
        print("{0}\t{1}\tRequestToEnqueue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_waiting))
        if self.number_waiting < self.capacity:
            self.enqueue()

    def enqueue(self):
        self.number_pending -= 1
        self.number_waiting += 1
        print("{0}\t{1}\tEnqueue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_waiting))
        self.invoke(self.on_enqueue)

    def dequeue(self):
        self.number_waiting -= 1
        print("{0}\t{1}\tDequeue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_waiting))
        if self.number_pending > 0:
            self.enqueue()
