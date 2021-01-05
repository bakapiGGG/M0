from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo8.generator import Generator
from O2DESPy_demos.demo8.queue_ import Queue
from O2DESPy_demos.demo8.server import Server
import datetime
import random


class TandemQueuePush(Sandbox):
    def __init__(self, capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        random.seed(seed)
        self.capacity = capacity
        self.hourly_arrival_rate = hourly_arrival_rate
        self.hourly_service_rate = hourly_service_rate

        self.generator = self.add_child(Generator(self.hourly_arrival_rate))
        self.queue1 = self.add_child(Queue(queue_id=1))
        self.server1 = self.add_child(Server(self.capacity, self.hourly_service_rate, server_id=1))
        self.queue2 = self.add_child(Queue(queue_id=2))
        self.server2 = self.add_child(Server(self.capacity, self.hourly_service_rate, server_id=2))
        
        # Connects 1st Queue & Server
        self.generator.on_generate.add_event_method(self.queue1.enqueue)
        self.queue1.on_dequeue.add_event_method(self.server1.start)
        self.server1.on_change_accessibility.add_event_method((self.queue1.update_to_dequeue, self.queue1.able_to_dequeue))

        # Connects for 2nd Queue & Server
        self.server1.on_finish.add_event_method(self.queue2.enqueue)
        self.queue2.on_dequeue.add_event_method(self.server2.start)
        self.server2.on_change_accessibility.add_event_method((self.queue2.update_to_dequeue, self.queue2.able_to_dequeue))


if __name__ == '__main__':
    # Demo 8
    sim1 = TandemQueuePush(capacity=1, hourly_arrival_rate=1, hourly_service_rate=2)
    hc1 = sim1.add_hour_counter()
    sim1.run(duration=datetime.timedelta(hours=10))
