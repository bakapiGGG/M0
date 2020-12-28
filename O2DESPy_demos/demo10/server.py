from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from datetime import timedelta
from datetime import datetime
import random


class Server(Sandbox):
    def __init__(self, capacity, hourly_service_rate, seed=0):
        super().__init__()
        self.__capacity = capacity
        self.__hourly_service_rate = hourly_service_rate
        self.__number_in_service = 0
        self.__number_pending_depart = 0
        self.__able_to_depart = True
        self.__seed = seed 
        self.__on_change_accessibility = []
        self.__on_depart = []

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
    def number_pending_depart(self):
        return self.__number_pending_depart
    
    @property
    def able_to_depart(self):
        return self.__able_to_depart

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def on_change_accessibility(self):
        return self.__on_change_accessibility

    @on_change_accessibility.setter
    def on_change_accessibility(self, value):
        self.__on_change_accessibility.append(value)
    
    @property
    def on_depart(self):
        return self.__on_depart

    @on_depart.setter
    def on_depart(self, value):
        self.__on_depart.append(value)
    
    def start(self):
        if self.__number_in_service + self.__number_pending_depart >= self.__capacity:
            return "Insufficient Vacancy."
        self.__number_in_service += 1
        print("{0}\t{1}\tStart. #In-Service: {2}. #Pending-Depart: {3}".format(self.clock_time, type(self).__name__, self.__number_in_service, self.__number_pending_depart))
        Logger.info("{0}\t{1}\tStart. #In-Service: {2}. #Pending-Depart: {3}".format(self.clock_time, type(self).__name__, self.__number_in_service, self.__number_pending_depart))
        self.schedule([self.finish], timedelta(hours=round(random.expovariate(1 / self.__hourly_service_rate))))
        if self.__number_in_service == self.__capacity:
            # Not sure what change_accessibility does. Intuitively, cant start service when capacity is full (join queue).
            self.change_accessibility()

    def finish(self):
        if self.clock_time >= datetime(1, 1, 1, 4, 12, 34):
            pass # not sure the effect of condition stated in c# code
        self.__number_in_service -= 1
        self.__number_pending_depart += 1
        print("{0}\t{1}\tFinish. #In-Service: {2}. #Pending-Depart: {3}".format(self.clock_time, type(self).__name__, self.__number_in_service, self.__number_pending_depart))
        Logger.info("{0}\t{1}\tFinish. #In-Service: {2}. #Pending-Depart: {3}".format(self.clock_time, type(self).__name__, self.__number_in_service, self.__number_pending_depart))
        if self.__able_to_depart:
            self.depart()
    
    def depart(self):
        self.__number_pending_depart -= 1
        print("{0}\t{1}\tDepart. #In-Service: {2}. #Pending-Depart: {3}".format(self.clock_time, type(self).__name__, self.__number_in_service, self.__number_pending_depart))
        Logger.info("{0}\t{1}\tDepart. #In-Service: {2}. #Pending-Depart: {3}".format(self.clock_time, type(self).__name__, self.__number_in_service, self.__number_pending_depart))
        if self.__number_in_service + self.__number_pending_depart == self.__capacity - 1:
            self.change_accessibility()
        for func in self.__on_depart:
            if len(func) == 1:
                func[0]()
            func[0](**func[1])
    
    def update_to_depart(self, AbleToDepart):
        self.__able_to_depart = AbleToDepart
        print("{0}\t{1}\tUpdateToDequeue. AbleToDepart: {2}".format(self.clock_time, type(self).__name__, self.__able_to_depart))
        Logger.info("{0}\t{1}\tUpdateToDequeue. AbleToDepart: {2}".format(self.clock_time, type(self).__name__, self.__able_to_depart))
        if self.__able_to_depart and self.__number_pending_depart > 0:
            self.depart()

    def change_accessibility(self):
        print("{0}\t{1}\tChangeAccessibility. #In_Service: {2}".format(self.clock_time, type(self).__name__, self.__number_in_service))
        Logger.info("{0}\t{1}\tChangeAccessibility. #In_Service: {2}".format(self.clock_time, type(self).__name__, self.__number_in_service))
        for func in self.__on_change_accessibility:
            if self.__number_in_service + self.__number_pending_depart < self.__capacity:
                if len(func) == 1:
                    func[0]()
                else:
                    func[0](**func[1])

# public event Action<bool> OnChangeAccessibility = (accessible) => { }; to pass "accessible" parameter into the function 