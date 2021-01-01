from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo7.generator import Generator
from O2DESPy_demos.demo7.queue_ import Queue
from O2DESPy_demos.demo7.server import Server
import datetime


class TandemQueuePull(Sandbox):
    def __init__(self, capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        self.capacity = capacity
        self.hourly_arrival_rate = hourly_arrival_rate
        self.hourly_service_rate = hourly_service_rate

        self.generator = self.add_child(Generator(self.hourly_arrival_rate))
        self.queue1 = self.add_child(Queue())
        self.server1 = self.add_child(Server(self.capacity, self.hourly_service_rate))
        self.queue2 = self.add_child(Queue())
        self.server2 = self.add_child(Server(self.capacity, self.hourly_service_rate))
        
        # Connects 1st Queue & Server
        self.generator.on_generate.add_event_method(self.queue1.enqueue)
        self.generator.on_generate.add_event_method(self.server1.request_to_start)
        self.server1.on_start.add_event_method(self.queue1.dequeue)

        # Connects for 2nd Queue & Server
        self.server1.on_finish.add_event_method(self.queue2.enqueue)
        self.server1.on_finish.add_event_method(self.server2.request_to_start)
        self.server2.on_start.add_event_method(self.queue2.dequeue)


if __name__ == '__main__':
    # Demo 7
    sim1 = TandemQueuePull(capacity=1, hourly_arrival_rate=4, hourly_service_rate=5)
    hc1 = sim1.add_hour_counter()
    sim1.run(duration=datetime.timedelta(hours=100))
