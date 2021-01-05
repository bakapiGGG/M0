from O2DESPy.sandbox import Sandbox
import random


class Queue(Sandbox):
    def __init__(self, capacity, queue_id, seed=0):
        super().__init__()
        random.seed(seed)
        self.capacity = capacity
        self.queue_id = queue_id
        self.number_waiting = 0
        self.able_to_dequeue = True
        self.on_dequeue = self.create_event()
        self.on_change_accessibility = self.create_event()

    def enqueue(self):
        self.number_waiting += 1
        print("{0}\t{1}\tEnqueue. #Waiting: {2}. Queue id: {3}".format(self.clock_time, type(self).__name__, self.number_waiting, self.queue_id))
        self.schedule(self.attempt_to_dequeue)
        if self.number_waiting == self.capacity:
            self.change_accessibility()

    def update_to_dequeue(self, able_to_dequeue):
        self.able_to_dequeue = able_to_dequeue
        print("{0}\t{1}\tUpdateToDequeue. AbleToDequeue: {2}".format(self.clock_time, type(self).__name__, self.able_to_dequeue))
        if self.able_to_dequeue and (self.number_waiting > 0):
            self.dequeue()

    def attempt_to_dequeue(self):
        if self.able_to_dequeue and (self.number_waiting > 0):
            self.dequeue()

    def dequeue(self):
        self.number_waiting -= 1
        print("{0}\t{1}\tDequeue. #Waiting: {2}. Queue id: {3}".format(self.clock_time, type(self).__name__, self.number_waiting, self.queue_id))
        if self.number_waiting == self.capacity - 1:
            self.change_accessibility()
        self.invoke(self.on_dequeue)
    
    def change_accessibility(self):
        print("{0}\t{1}\tChangeAccessibility. #Waiting: {2}. Queue id: {3}".format(self.clock_time, type(self).__name__, self.number_waiting, self.queue_id))
        self.invoke((self.on_change_accessibility, self.number_waiting < self.capacity))
