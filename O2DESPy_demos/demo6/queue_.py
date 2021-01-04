from O2DESPy.sandbox import Sandbox
import random


class Queue(Sandbox):
    def __init__(self, seed=0):
        super().__init__()
        random.seed(seed)
        self.number_waiting = 0
        self.able_to_dequeue = True
        self.on_dequeue = self.create_event()
        # self.__on_dequeue = []

    def enqueue(self):
        self.number_waiting += 1
        print("{0}\t{1}\tEnqueue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.number_waiting))
        if self.able_to_dequeue:
            self.dequeue()

    def update_to_dequeue(self, able_to_dequeue):
        self.able_to_dequeue = able_to_dequeue
        print("{0}\t{1}\tUpdateToDequeue. AbleToDequeue: {2}".format(self.clock_time, type(self).__name__, self.able_to_dequeue))
        if self.able_to_dequeue and self.number_waiting > 0:
            self.dequeue()

    def dequeue(self):
        self.number_waiting -= 1
        print("{0}\t{1}\tDequeue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.number_waiting))
        self.invoke(self.on_dequeue)
        '''
        for func in self.__on_dequeue:
            if len(func) == 1:
                func[0]()
            else:
                func[0](**func[1])
        '''
