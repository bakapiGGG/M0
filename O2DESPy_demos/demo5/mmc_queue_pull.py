from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo5.generator import Generator
from O2DESPy_demos.demo5.queue_ import Queue
from O2DESPy_demos.demo5.server import Server
import datetime
import random

class MMcQueuePull(Sandbox):
    def __init__(self, capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        random.seed(seed)
        self.capacity = capacity
        self.hourly_arrival_rate = hourly_arrival_rate
        self.hourly_service_rate = hourly_service_rate
        self.generator = self.add_child(Generator(self.hourly_arrival_rate))
        self.queue = self.add_child(Queue())
        self.server = self.add_child(Server(self.capacity, self.hourly_service_rate))
        
        self.generator.on_generate.add_event_method(self.queue.enqueue)
        # self.__generator.on_generate = [self.queue.enqueue]
        self.generator.on_generate.add_event_method(self.server.request_to_start)
        # self.__generator.on_generate = [self.server.request_to_start]
        self.server.on_start.add_event_method(self.queue.dequeue)
        # self.__server.on_start = [self.queue.dequeue]


if __name__ == '__main__':
    # Demo 5
    sim1 = MMcQueuePull(capacity=1, hourly_arrival_rate=4, hourly_service_rate=5)
    hc1 = sim1.add_hour_counter()
    sim1.run(duration=datetime.timedelta(hours=100))
