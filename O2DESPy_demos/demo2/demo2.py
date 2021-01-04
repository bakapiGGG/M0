from O2DESPy.sandbox import Sandbox
import datetime
import random


class BirthDeath(Sandbox):
    def __init__(self, hourly_birth_rate, hourly_death_rate, seed=0):
        super().__init__()
        random.seed(seed)
        self.hourly_birth_rate = hourly_birth_rate
        self.hourly_death_rate = hourly_death_rate
        self.population = 0

        self.schedule(self.birth)
    
    def birth(self):
        self.population += 1
        print("{0}\tBirth (Population: #{1}!)".format(self.clock_time, self.population))
        self.schedule(self.birth, datetime.timedelta(hours=round(random.expovariate(1 / self.hourly_birth_rate), 2)))
        self.schedule(self.death, datetime.timedelta(hours=round(random.expovariate(1 / self.hourly_death_rate), 2)))

    def death(self):
        self.population -= 1
        print("{0}\tDeath (Population: #{1}!)".format(self.clock_time, self.population))


if __name__ == '__main__':
    sim2 = BirthDeath(5, 1, seed=1)
    sim2.warmup(till=datetime.datetime(year=1, month=1, day=1, hour=0, minute=0, second=0))
    sim2.run(duration=datetime.timedelta(hours=30))
    # sim2.run(event_count=10)
    # sim2.run(speed=10)
    # sim2.run(terminate=datetime.datetime(year=1, month=1, day=1, hour=0, minute=5))
