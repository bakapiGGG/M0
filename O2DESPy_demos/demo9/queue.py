from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger


class Queue(Sandbox):
    def __init__(self, capacity, seed=0):
        super().__init__()
        self.__capacity = capacity
        self.__seed = seed
        self.__number_waiting = 0
        self.__number_pending = 0
        self.__on_enqueue = []

    @property
    def capacity(self):
        return self.__capacity

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
    def number_pending(self):
        return self.__number_pending
    
    @property
    def on_enqueue(self):
        return self.__on_enqueue
    
    @on_enqueue.setter
    def on_enqueue(self, value):
        self.__on_enqueue = value

    def request_to_enqueue(self):
        self.__number_pending += 1
        print("{0}\t{1}\tRequestToEnqueue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_waiting))
        Logger.info("{0}\t{1}\tRequestToEnqueue. #Pending: {2}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_waiting))
        if self.__number_waiting < self.__capacity:
            self.enqueue()

    def enqueue(self):
        self.__number_pending -=1
        self.__number_waiting += 1
        print("{0}\t{1}\tEnqueue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_waiting))
        Logger.info("{0}\t{1}\tEnqueue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_waiting))
        for func in self.__on_enqueue:
                if len(func) == 1:
                    func[0]()
                else:
                    func[0](**func[1])

    def dequeue(self):
        self.__number_waiting -= 1
        print("{0}\t{1}\tDequeue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_waiting))
        Logger.info("{0}\t{1}\tDequeue. #Pending: {2}. #Waiting: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_waiting))
        if self.__number_pending > 0:
            self.enqueue()
        