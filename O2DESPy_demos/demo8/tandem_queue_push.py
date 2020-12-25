from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo8.generator import Generator
from O2DESPy_demos.demo8.queue_ import Queue
from O2DESPy_demos.demo8.server import Server


class TandemQueuePull(Sandbox):
    def __init__(self, capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        self.__capacity = capacity
        self.__hourly_arrival_rate = hourly_arrival_rate
        self.__hourly_service_rate = hourly_service_rate
        self.__seed = seed

        self.__generator = self.add_child(Generator(self.__hourly_arrival_rate))
        self.__queue1 = self.add_child(Queue())
        self.__server1 = self.add_child(Server(self.__capacity, self.__hourly_service_rate))
        self.__queue2 = self.add_child(Queue())
        self.__server2 = self.add_child(Server(self.__capacity, self.__hourly_service_rate))
        
        # Connets 1st Queue & Server
        self.__generator.on_generate = [self.queue1.enqueue]
        self.__queue.on_dequeue = [self.server1.start]
        self.__server1.on_change_accessibility = [self.queue1.update_to_dequeue]

        # Connects for 2nd Queue & Server
        self.__server1.on_finish = [self.queue2.enqueue]
        self.__server1.on_dequeue = [self.server2.start]
        self.__server2.on_change_accessibility = [self.queue2.update_to_dequeue]

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
    def queue1(self):
        return self.__queue1

    @property
    def server1(self):
        return self.__server1
    
    @property
    def queue2(self):
        return self.__queue2

    @property
    def server2(self):
        return self.__server2