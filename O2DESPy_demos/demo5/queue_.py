from O2DESPy.sandbox import Sandbox
import random


class Queue(Sandbox):
    def __init__(self, seed=0):
        super().__init__()
        random.seed(seed)
        self.number_waiting = 0

    def enqueue(self):
        self.number_waiting += 1
        print("{0}\t{1}\tEnqueue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.number_waiting))

    def dequeue(self):
        self.number_waiting -= 1
        print("{0}\t{1}\tDequeue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.number_waiting))
