from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from datetime import timedelta
import random


class Server(Sandbox):
    def __init__(self, capacity, hourly_service_rate, seed=0):
        super().__init__()
        self.__capacity = capacity
        self.__hourly_service_rate = hourly_service_rate
        self.__number_pending = 0
        self.__number_in_service = 0
        self.__on_start = []

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    @property
    def hourly_service_rate(self):
        return self.__hourly_service_rate

    @hourly_service_rate.setter
    def hourly_service_rate(self, value):
        self.__hourly_service_rate = value

    @property
    def number_pending(self):
        return self.__number_pending

    @number_pending.setter
    def number_pending(self, value):
        self.__number_pending = value

    @property
    def number_in_service(self):
        return self.__number_in_service

    @number_in_service.setter
    def number_in_service(self, value):
        self.__number_in_service = value

    @property
    def on_start(self):
        return self.__on_start

    @on_start.setter
    def on_start(self, value):
        self.__on_start.append(value)

    def request_to_start(self):
        self.__number_pending += 1
        print("{0}\t{1}\tRequestToStart. #Pending: {2}. #In-Service: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_in_service))
        Logger.info("{0}\t{1}\tRequestToStart. #Pending: {2}. #In-Service: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_in_service))
        if self.__number_in_service < self.__capacity:
            self.start()
        
    
    def start(self):
        self.__number_pending -= 1
        self.__number_in_service += 1
        print("{0}\t{1}\tStart. #Pending: {2}. #In-Service: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_in_service))
        Logger.info("{0}\t{1}\tStart. #Pending: {2}. #In-Service: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_in_service))
        self.schedule([self.finish], timedelta(hours=round(random.expovariate(1 / self.__hourly_service_rate))))
        for func in self.__on_start:
                if len(func) == 1:
                    func[0]()
                else:
                    func[0](**func[1])


    def finish(self):
        self.__number_in_service -= 1
        print("{0}\t{1}\tStart. #Pending: {2}. #In_Service: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_in_service))
        Logger.info("{0}\t{1}\tStart. #Pending: {2}. #In_Service: {3}".format(self.clock_time, type(self).__name__, self.__number_pending, self.__number_in_service))
        if self.__number_pending > 0:
            self.start()

