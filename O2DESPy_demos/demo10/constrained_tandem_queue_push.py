from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo10.generator import Generator
from O2DESPy_demos.demo10.queue import Queue
from O2DESPy_demos.demo10.server import Server


class ConstrainedTandemQueuePush(Sandbox):
    def __init__(self, queue_capacity, server_capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        self.__queue_capacity = queue_capacity
        self.__server_capacity = server_capacity
        self.__hourly_arrival_rate = hourly_arrival_rate
        self.__hourly_service_rate = hourly_service_rate

        self.__generator = self.add_child(Generator(self.__hourly_arrival_rate))
        self.__queue1 = self.add_child(Queue(self.__queue_capacity))
        self.__server1 = self.add_child(Server(self.__server_capacity, self.__hourly_service_rate))
        self.__queue2 = self.add_child(Queue(self.__queue_capacity))
        self.__server2 = self.add_child(Server(self.__server_capacity, self.__hourly_service_rate))
        
        # Connets 1st Queue & Server
        self.__generator.on_generate = [self.queue1.enqueue]
        self.__queue1.__on_dequeue = [self.server1.start]
        self.__server1.on_change_accessibility = [self.queue1.update_to_dequeue]

        # Connects for 2nd Queue & Server
        self.__server1.on_depart = [self.queue2.enqueue]
        self.__queue2.on_dequeue = [self.server2.start]
        self.__queue2.on_change_accessibility = [self.server1.update_to_depart]
        self.__server2.on_change_accessibility = [self.queue2.update_to_dequeue]

    @property
    def queue_capacity(self):
        return self.__queue_capacity

    @queue_capacity.setter
    def queue_capacity(self, value):
        self.__queue_capacity = value

    @property
    def server_capacity(self):
        return self.__server_capacity

    @server_capacity.setter
    def server_capacity(self, value):
        self.__server_capacity = value

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