from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from datetime import timedelta
import random


class Generator(Sandbox):
    def __init__(self, hourly_rate, seed=0):
        super().__init__()
        random.seed(seed)
        self.hourly_rate = hourly_rate
        self.count = 0
        self.on_generate = self.create_event()
        
        self.schedule((self.generate, 'test'))
        # self.schedule([self.generate, {'test', test}], timedelta(seconds=0))

    def generate(self, test):
        if self.count > 0:
            print("{0}\t{1}\tGenerate. Count: {2}".format(self.clock_time, type(self).__name__, self.count))
            self.invoke(self.on_generate)
            '''
            for func in self.__on_generate:
                if len(func) == 1:
                    func[0]()
                else:
                    func[0](**func[1])
            '''
        self.count += 1
        self.schedule((self.generate, 'test'), timedelta(hours=round(random.expovariate(1 / self.hourly_rate),2)))
        # self.schedule([self.generate,{'test': test}], timedelta(hours=round(random.expovariate(1/self.__hourlyrate),2))
