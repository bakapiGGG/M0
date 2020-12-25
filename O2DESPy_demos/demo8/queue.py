from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger


class Queue(Sandbox):
    def __init__(self, seed=0):
        super().__init__()
        self.__seed = seed
        self.__number_waiting = 0
        self.__able_to_dequeue = True
        self.__on_dequeue = []
        
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def number_waiting(self):
        return self.__number_waiting

    @property
    def able_to_dequeue(self):
        return self.__able_to_dequeue
    
    @property
    def on_dequeue(self):
        return self.__on_dequeue

    @on_dequeue.setter
    def on_dequeue(self, value):
        self.__on_dequeue.append(value)

    def enqueue(self):
        self.__number_waiting += 1
        print("{0}\t{1}\tEnqueue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))
        Logger.info("{0}\t{1}\tEnqueue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))
        if (self.__able_to_dequeue):
            self.dequeue()

    def update_to_dequeue(self, able_to_dequeue):
        self.__able_to_dequeue = able_to_dequeue
        print("{0}\t{1}\tUpdateToDequeue. AbleToDequeue: {2}".format(self.clock_time, type(self).__name__, self.__able_to_dequeue))
        Logger.info("{0}\t{1}\tUpdateToDequeue. AbleToDequeue: {2}".format(self.clock_time, type(self).__name__, self.__able_to_dequeue))
        if (self.__able_to_dequeue and self.__number_waiting > 0):
            self.dequeue()

    def dequeue(self):
        self.__number_waiting -= 1
        print("{0}\t{1}\tDequeue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))
        Logger.info("{0}\t{1}\tDequeue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))
        for func in self.__on_dequeue:
            if len(func) == 1:
                func[0]()
            else:
                func[0](**func[1])
