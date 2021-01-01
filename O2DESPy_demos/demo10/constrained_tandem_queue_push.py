from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo10.generator import Generator
from O2DESPy_demos.demo10.queue_ import Queue
from O2DESPy_demos.demo10.server import Server
import datetime


class ConstrainedTandemQueuePush(Sandbox):
    def __init__(self, queue_capacity, server_capacity, hourly_arrival_rate, hourly_service_rate, seed=0):
        super().__init__()
        self.queue_capacity = queue_capacity
        self.server_capacity = server_capacity
        self.hourly_arrival_rate = hourly_arrival_rate
        self.hourly_service_rate = hourly_service_rate

        self.generator = self.add_child(Generator(self.hourly_arrival_rate))
        self.queue1 = self.add_child(Queue(self.queue_capacity))
        self.server1 = self.add_child(Server(self.server_capacity, self.hourly_service_rate))
        self.queue2 = self.add_child(Queue(self.queue_capacity))
        self.server2 = self.add_child(Server(self.server_capacity, self.hourly_service_rate))
        
        # Connects 1st Queue & Server
        self.generator.on_generate.add_event_method(self.queue1.enqueue)
        self.queue1.on_dequeue.add_event_method(self.server1.start)
        self.server1.on_change_accessibility.add_event_method(self.queue1.update_to_dequeue)

        # Connects for 2nd Queue & Server
        self.server1.on_depart.add_event_method(self.queue2.enqueue)
        self.queue2.on_dequeue.add_event_method(self.server2.start)
        self.queue2.on_change_accessibility.add_event_method(self.server1.update_to_depart)
        self.server2.on_change_accessibility.add_event_method(self.queue2.update_to_dequeue)


if __name__ == '__main__':
    # Demo 10
    sim1 = ConstrainedTandemQueuePush(queue_capacity=2, server_capacity=1, hourly_arrival_rate=5, hourly_service_rate=5)
    hc1 = sim1.add_hour_counter()
    sim1.run(duration=datetime.timedelta(hours=100))