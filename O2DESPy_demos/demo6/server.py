from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from datetime import timedelta
import random


class Server(Sandbox):
    def __init__(self, capacity, hourly_service_rate, seed=0):
        super().__init__()
        self.__capacity = capacity
        self.__hourly_service_rate = hourly_service_rate
        self.__number_in_service = 0
        self.__seed = seed 
        self.__on_change_accessibility = []

    @property
    def capacity(self):
        return self.__capacity

    @property
    def hourly_service_rate(self):
        return self.__hourly_service_rate

    @property
    def number_in_service(self):
        return self.__number_in_service
    
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def on_change_accessibility(self):
        return self.__on_start

    @on_change_accessibility.setter
    def on_change_accessibility(self, value):
        self.__on_change_accessibility.append(value)
    
    def start(self):
        # still need to discuss about this condition; contradicts with latter condition of ==
        if self.__number_in_service >= self.__capacity:
            return "Insufficient Vacancy."
        self.__number_in_service += 1
        print("{0}\t{1}\tStart. #In-Service: {2}".format(self.clock_time, type(self).__name__, self.__number_in_service))
        Logger.info("{0}\t{1}\tStart. .#In-Service: {2}".format(self.clock_time, type(self).__name__, self.__number_in_service))
        self.schedule([self.finish], timedelta(hours=round(random.expovariate(1 / self.__hourly_service_rate))))
        if self.__number_in_service == self.__capacity:
            # Not sure what change_accessibility does. Intuitively, cant start service when capacity is full (join queue).
            self.schedule([self.change_accessibility])

    def finish(self):
        self.__number_in_service -= 1
        print("{0}\t{1}\tFinish. #In_Service: {2}".format(self.clock_time, type(self).__name__, self.__number_in_service))
        Logger.info("{0}\t{1}\tFinish. #In_Service: {2}".format(self.clock_time, type(self).__name__, self.__number_in_service))
        if self.__number_in_service == self.__capacity - 1:
            self.schedule([self.change_accessibility])

    def change_accessibility(self):
    # OnChangeAccessibility.Invoke(NumberInService < Capacity); Not sure what invoke with condition within its paratheses mean
        for func in self.__on_change_accessibility:
            if len(func) == 1:
                        func[0]()
                    else:
                        func[0](**func[1])


# public event Action<bool> OnChangeAccessibility = (accessible) => { }; to pass "accessible" parameter into the function 