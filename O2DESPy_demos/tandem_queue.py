from O2DESPy.sandbox import Sandbox
from O2DESPy.standard.generator import Generator
from O2DESPy.standard.queue_ import Queue
from O2DESPy.standard.server import Server
from O2DESPy.standard.load import Load
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
from datetime import timedelta
import time
import datetime
import math
import random


class TandemQueue(Sandbox):
    def __init__(self, arr_rate, svc_rate1, svc_rate2, buffer_q_size, seed=0):
        super().__init__()
        self.__hourly_arrival_rate = arr_rate
        self.__hourly_service_rate1 = svc_rate1
        self.__hourly_service_rate2 = svc_rate2
        self.__buffer_q_size = buffer_q_size
        self.__seed = seed

        self.__generator = self.add_child(Generator(inter_arrival_time=timedelta(seconds=round(random.expovariate(1 / self.__hourly_arrival_rate)))))
        self.__queue1 = self.add_child(Queue(capacity=math.inf, id="Queue1"))
        self.__server1 = self.add_child(Server(capacity=1, service_time=timedelta(seconds=round(random.expovariate(1 / self.__hourly_service_rate1))), id="Server1"))
        self.__queue2 = self.add_child(Queue(capacity=self.__buffer_q_size, id="Queue2"))
        self.__server2 = self.add_child(Server(capacity=1, service_time=timedelta(seconds=round(random.expovariate(1 / self.__hourly_service_rate2))), id="Server2"))

        self.__generator.on_arrive = [self.__queue1.rqst_enqueue, {'load': Load()}]
        self.__generator.on_arrive = [self.__arrive]

        self.__queue1.on_enqueued = [self.__server1.rqst_start]
        self.__server1.on_started = [self.__queue1.dequeue]

        self.__server1.on_ready_to_depart = [self.__queue2.rqst_enqueue]
        self.__queue2.on_enqueued = [self.__server1.depart]

        self.__queue2.on_enqueued = [self.__server2.rqst_start]
        self.__server2.on_started = [self.__queue2.dequeue]

        self.__server2.on_ready_to_depart = [self.__server2.depart]
        self.__server2.on_ready_to_depart = [self.__depart]

        self.__hc_in_system = self.add_hour_counter()

        self.__generator.start()

    # region Static Properties
    @property
    def hourly_arrival_rate(self):
        """Hourly arrival rate to the system"""
        return self.__hourly_arrival_rate

    @property
    def hourly_service_rate1(self):
        """Hourly service rate of Server1"""
        return self.__hourly_service_rate1

    @property
    def hourly_service_rate2(self):
        """Hourly service rate of Server2"""
        return self.__hourly_service_rate2

    @property
    def buffer_queue_size(self):
        """Buffer queue (Queue2) capacity"""
        return self.__queue2.capacity

    # region Dynamic Properties
    @property
    def avgn_queueing1(self):
        return self.__queue1.avgn_queueing

    @property
    def avgn_queueing2(self):
        return self.__queue2.avgn_queueing

    @property
    def avgn_serving1(self):
        return self.__server1.avgn_serving

    @property
    def avgn_serving2(self):
        return self.__server2.avgn_serving

    @property
    def avg_hours_in_system(self):
        return self.__hc_in_system.average_duration

    # region Events / Methods
    def __arrive(self):
        Logger.info("TandemQueue Arrive.")
        self.__hc_in_system.observe_change(1, self.clock_time)

    def __depart(self):
        Logger.info("TandemQueue Depart.")
        self.__hc_in_system.observe_change(-1, self.clock_time)

if __name__ == '__main__':
    run_code = 'O2DESPy Tandem Queue'
    start_time = time.time()

    Logger.debug("Init time: {}".format(time.time() - start_time))
    Logger.critical('Run: {}'.format(run_code))
    Logger.update_config(
        file_path=Config.log_file_path,
        dynamic=True,
        include_log=['debug', 'info', 'warning', 'error', 'critical'],
        name=run_code,
        stream_level='critical',
        output_mode=['stream', 'file'],
        file_level='debug',
        fmt='%(levelname)s: %(message)s')

    # Demo 1
    Logger.info("Demo 1 - Hello world")
    sim = TandemQueue(arr_rate=1, svc_rate1=1, svc_rate2=1, buffer_q_size=10)
    hc1 = sim.add_hour_counter()
    sim.run(duration=datetime.timedelta(seconds=30))
    Logger.critical('use time {}'.format(time.time() - start_time))
