from O2DESPy.sandbox import Sandbox
from datetime import timedelta
import random


class Server(Sandbox):
    def __init__(self, capacity, hourly_service_rate, seed=0):
        super().__init__()
        self.capacity = capacity
        self.hourly_service_rate = hourly_service_rate
        self.number_pending = 0
        self.number_in_service = 0
        self.on_start = self.create_event()
        # self.__on_start = []
        random.seed(seed)

    def request_to_start(self):
        self.number_pending += 1
        print("{0}\t{1}\tRequestToStart. #Pending: {2}. #In-Service: {3}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_in_service))
        if self.number_in_service < self.capacity:
            self.start()
    
    def start(self):
        self.number_pending -= 1
        self.number_in_service += 1
        print("{0}\t{1}\tStart. #Pending: {2}. #In-Service: {3}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_in_service))
        self.schedule(self.finish, timedelta(hours=round(random.expovariate(1 / self.hourly_service_rate),2)))
        # self.schedule([self.finish], timedelta(hours=round(random.expovariate(1 / self.__hourly_service_rate),2)))
        self.invoke(self.on_start)
        ''' 
        for func in self.__on_start:
            if len(func) == 1:
                func[0]()
            else:
                func[0](**func[1])
        '''

    def finish(self):
        self.number_in_service -= 1
        print("{0}\t{1}\tStart. #Pending: {2}. #In_Service: {3}".format(self.clock_time, type(self).__name__, self.number_pending, self.number_in_service))
        if self.number_pending > 0:
            self.start()

