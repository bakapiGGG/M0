from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
from datetime import timedelta
import datetime
import time
import random


class MMcQueue(Sandbox):
    def __init__(self, hourly_arrival_rate, hourly_service_rate, capacity, seed=0):
        super().__init__()
        self.__seed = seed 
        self.__hourly_arrival_rate = hourly_arrival_rate
        self.__hourly_service_rate = hourly_service_rate
        self.__capacity = capacity
        self.__in_queue = 0
        self.__in_service = 0

        self.schedule([self.arrive], timedelta(seconds=0))
    
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def hourly_arrival_rate(self):
        return self.__hourly_arrival_rate

    @property
    def hourly_service_rate(self):
        return self.__hourly_service_rate

    @property
    def capacity(self):
        return self.__capacity

    @property
    def in_queue(self):
        return self.__in_queue

    @property
    def in_service(self):
        return self.__in_service

    def arrive(self):
        if self.__in_service < self.__capacity:
            self.__in_service += 1
            print("{0}\tArrive and Start Service (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.__in_queue, self.__in_service))
            Logger.info("{0}\tArrive and Start Service (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.__in_queue, self.__in_service))
            self.schedule([self.depart], timedelta(hours=round(random.expovariate(1 / self.__hourly_service_rate),2)))
        else:
            self.__in_queue += 1
            print("{0}\tArrive and Join Queue (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.__in_queue, self.__in_service))
            Logger.info("{0}\tArrive and Join Queue (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.__in_queue, self.__in_service))
        self.schedule([self.arrive], timedelta(hours=round(random.expovariate(1 / self.__hourly_arrival_rate),2)))

    def depart(self):
        if self.__in_queue > 0:
            self.__in_queue -= 1
            print("{0}\tDepart and Start Service (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.__in_queue, self.__in_service))
            Logger.info("{0}\tDepart and Start Service (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.__in_queue, self.__in_service))
            self.schedule([self.depart], timedelta(hours=round(random.expovariate(1 / self.__hourly_service_rate),2)))
        else:
            self.__in_service -= 1
            print("{0}\tDepart (In-Queue: {1}, In-Service: {2})".format(self.clock_time, self.__in_queue, self.__in_service))

    
if __name__ == '__main__':
    run_code = 'O2DESPy demo 3'
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

    # Demo 3
    Logger.info("Demo 3 - MMcQueue")
    sim1 = MMcQueue(hourly_arrival_rate=1, hourly_service_rate=2, capacity=2)
    sim1.run(duration=datetime.timedelta(hours=30))
    Logger.critical('use time {}'.format(time.time() - start_time))