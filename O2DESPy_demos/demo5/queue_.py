from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger


class Queue(Sandbox):
    def __init__(self, seed=0):
        super().__init__()
        self.__seed = seed
        self.__number_waiting = 0

    @property
    def number_waiting(self):
        return self.__number_waiting

    def enqueue(self):
        self.__number_waiting += 1
        print("{0}\t{1}\tEnqueue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))
        Logger.info("{0}\t{1}\tEnqueue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))

    def dequeue(self):
        self.__number_waiting -= 1
        print("{0}\t{1}\tDequeue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))
        Logger.info("{0}\t{1}\tDequeue. #Waiting: {2}".format(self.clock_time, type(self).__name__, self.__number_waiting))