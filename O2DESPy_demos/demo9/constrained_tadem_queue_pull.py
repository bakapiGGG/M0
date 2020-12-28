from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo9.generator import Generator
from O2DESPy_demos.demo9.queue_ import Queue
from O2DESPy_demos.demo9.server import Server


class ConstrainedTandemQueuePull(Sandbox):
    def __init__(self, queue_capacity, server_capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        self.__queue_capacity = queue_capacity
        self.__server_capacity = __server_capacity
        self.__hourly_arrival_rate = hourly_arrival_rate
        self.__hourly_service_rate = hourly_service_rate

        self.__generator = self.add_child(Generator(self.__hourly_arrival_rate))
        self.__queue1 = self.add_child(Queue(self.__queue_capacity))
        self.__server1 = self.add_child(Server(self.__capacity, self.__hourly_service_rate))
        self.__queue2 = self.add_child(Queue(self.__queue_capacity))
        self.__server2 = self.add_child(Server(self.__capacity, self.__hourly_service_rate))
        
        # Connets 1st Queue & Server
        self.__generator.on_generate = [self.queue1.enqueue]
        self.__generator.on_generate = [self.server1.request_to_start]
        self.__server1.on_start = [self.queue1.dequeue]

        # Connects for 2nd Queue & Server
        self.__server1.on_finish = [self.queue2.enqueue]
        self.__server1.on_finish = [self.server2.request_to_start]
        self.__server2.on_start = [self.queue2.dequeue]

        # Enclose 2nd Server
        self.__server2.on_ready_to_finish = [self.server2.finish]

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