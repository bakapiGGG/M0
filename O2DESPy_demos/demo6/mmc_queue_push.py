from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo6.generator import Generator
from O2DESPy_demos.demo6.queue_ import Queue
from O2DESPy_demos.demo6.server import Server


class MMcQueuePush(Sandbox):
    def __init__(self, capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        self.__capacity = capacity
        self.__hourly_arrival_rate = hourly_arrival_rate
        self.__hourly_service_rate = hourly_service_rate
        self.__seed = seed
        self.__generator = self.add_child(Generator(self.__hourly_arrival_rate))
        self.__queue = self.add_child(Queue())
        self.__server = self.add_child(Server(self.__capacity, self.__hourly_service_rate))

        self.__generator.on_generate = [self.queue.enqueue]
        self.__queue.on_dequeue = [self.server.start]
        self.__server.on_change_accessibility = [self.queue.update_to_dequeue(able_to_dequeue)]

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    @property
    def hourly_arrival_rate(self):
        return self.__hourly_arrival_rate

    @hourly_arrival_rate.setter
    def hourly_arrival_rate(self, value):
        self.__hourly_arrival_rate = value

    @property
    def hourly_service_rate(self):
        return self.__hourly_service_rate

    @hourly_service_rate.setter
    def hourly_service_rate(self, value):
        self.__hourly_service_rate = value
    
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def generator(self):
        return self.__generator

    @property
    def queue(self):
        return self.__queue

    @property
    def server(self):
        return self.__server
    
    