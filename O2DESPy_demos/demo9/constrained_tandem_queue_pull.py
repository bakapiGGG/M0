from O2DESPy.sandbox import Sandbox
from O2DESPy_demos.demo9.generator import Generator
from O2DESPy_demos.demo9.queue_ import Queue
from O2DESPy_demos.demo9.server import Server
import datetime


class ConstrainedTandemQueuePull(Sandbox):
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
        self.generator.on_generate.add_event_method(self.queue1.request_to_enqueue)
        self.generator.on_generate.add_event_method(self.server1.request_to_start)
        self.server1.on_start.add_event_method(self.queue1.dequeue)

        # Connects for 2nd Queue & Server
        self.server1.on_ready_to_finish.add_event_method(self.queue2.request_to_enqueue)
        self.server1.on_ready_to_finish.add_event_method(self.server2.request_to_start)
        self.queue2.on_enqueue.add_event_method(self.server1.finish)
        self.server2.on_start.add_event_method(self.queue2.dequeue)

        # Enclose 2nd Server
        self.server2.on_ready_to_finish.add_event_method(self.server2.finish)


if __name__ == '__main__':
    # Demo 9
    sim1 = ConstrainedTandemQueuePull(queue_capacity=2, server_capacity=1, hourly_arrival_rate=5, hourly_service_rate=5)
    hc1 = sim1.add_hour_counter()
    sim1.run(duration=datetime.timedelta(hours=100))
