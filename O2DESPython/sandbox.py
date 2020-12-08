from abc import ABC, abstractmethod
from sortedcontainers import SortedSet
from event import Event
from pointer import Pointer
from hour_counter import HourCounter
import pandas as pd
import time
from log.logger import Logger
import datetime


class ISandbox(ABC):
    def __init__(self, index=None, id=None, pointer=None, seed=None, parent=None, children=None, clock_time=None,
                 log_file=None, debug_mode=None):
        self.__index = index
        self.__id = id
        self.__pointer = pointer
        self.__seed = seed
        self.__parent = parent
        self.__children = children
        self.__clock_time = clock_time
        self.__log_file = log_file
        self.__debug_mode = debug_mode

    @property
    def index(self):
        return self.__index

    @property
    def id(self):
        return self.__id

    @property
    def pointer(self):
        return self.__pointer

    @property
    def seed(self):
        return self.__seed

    @property
    def parent(self):
        return self.__parent

    @property
    def children(self):
        return self.__children

    @property
    def clock_time(self):
        return self.__clock_time

    @property
    def log_file(self):
        return self.__log_file

    @log_file.setter
    def log_file(self, value):
        self.__log_file = value

    @property
    def debug_mode(self):
        return self.__debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        self.__debug_mode = value

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def warmup(self, *args, **kwargs):
        pass


class Sandbox(ISandbox):
    __count = 0

    def __init__(self, assets=None, seed=0, id=None, pointer=Pointer()):
        super().__init__(id, pointer, seed)
        self.__assets = assets
        self.__seed = seed
        self.__id = id
        self.__pointer = pointer
        Sandbox.__count += 1
        self.__index = Sandbox.__count
        self.__future_event_list = SortedSet()
        self.__head_event = None
        self.__parent = None
        self.__children = []
        self.__clock_time = datetime.datetime.min
        self.__realtime_for_last_run = None
        self.__on_warmup = [[self.warmup_handler()]]
        self.__hour_counters = []

    @property
    def assets(self):
        return self.__assets

    @assets.setter
    def assets(self, value):
        self.__assets = value

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

    @property
    def id(self):
        return self.__id

    @property
    def pointer(self):
        return self.__pointer

    @property
    def index(self):
        return self.__index

    @property
    def future_event_list(self):
        return self.__future_event_list

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def children(self):
        return self.__children

    @property
    def clock_time(self):
        if self.__parent is None:
            return self.__clock_time
        return self.__parent.clock_time

    @property
    def on_warmup(self):
        return self.__on_warmup

    @on_warmup.setter
    def on_warmup(self, value):
        self.__on_warmup.append(value)

    @property
    def hour_counters(self):
        return self.__hour_counters

    @property
    def log_file(self):
        return self.__log_file

    @log_file.setter
    def log_file(self, log_file):
        self.__log_file = log_file

    def schedule(self, action, clock_time=None, tag=None):
        if len(action) > 1:
            paras = list(action[1])[0] if isinstance(action[1], list) else action[1]
            if type(clock_time) is datetime.datetime:
                Logger.info(
                    'Schedule task "{}" arrive at: {}. Owner: {} | {}'.format(paras, clock_time, self.id, action[1]))
            elif type(clock_time) is datetime.timedelta:
                Logger.info(
                    'Schedule task "{}" arrive at: {}. Owner: {} | {}.'.format(paras, self.clock_time + clock_time,
                                                                               self.id, action[1]))

        if isinstance(clock_time, pd.Timestamp):
            clock_time = clock_time.to_pydatetime()
        if type(clock_time) is datetime.datetime:
            self.__future_event_list.add(Event(owner=self, action=action, scheduled_time=clock_time, tag=tag))
        elif type(clock_time) is datetime.timedelta:
            self.__future_event_list.add(
                Event(owner=self, action=action, scheduled_time=self.clock_time + clock_time, tag=tag))
        else:
            Logger.error("clock_time type error {}".format(clock_time))
            raise TypeError()

    @property
    def head_event(self):
        head_event = None
        if len(self.__future_event_list) > 0:
            head_event = self.__future_event_list[0]
        for child in self.__children:
            child_head_event = child.head_event
            if head_event is None or (child_head_event is not None and child_head_event < head_event):
                head_event = child_head_event
        return head_event

    def run(self, *args, **kwargs):
        if kwargs == {}:
            if self.__parent is not None:
                return self.__parent.run()
            head = self.head_event
            if head is None:
                return False
            head.owner.future_event_list.discard(head)
            self.__clock_time = head.scheduled_time
            head.invoke()
            return True
        elif 'duration' in kwargs:
            if self.__parent is not None:
                return self.__parent.run(duration=kwargs['duration'])
            return self.run(terminate=self.clock_time + kwargs['duration'])
        elif 'terminate' in kwargs:
            Logger.info('start with terminate {}'.format(kwargs))
            if self.__parent is not None:
                return self.__parent.run(terminate=kwargs['terminate'])
            n = 0
            step_time = time.time()
            while True:
                n += 1
                head = self.head_event
                # print('1', head.scheduled_time, kwargs['terminate'], head.scheduled_time <= kwargs['terminate'])
                if head is not None and head.scheduled_time <= kwargs['terminate']:  # Finish all event or time out
                    start_time = time.time()
                    Logger.warning(
                        '{} {} {} {} {}'.format('----' * 9, 'Run once', n, '', '----' * 10))
                    self.run()
                    use_time = time.time() - start_time
                    use_time = 'Time_out_:{}'.format(use_time) if use_time > 0.02 else use_time
                    Logger.warning('{} {} {} {} {} {} Time: {}'
                                   .format('----' * 9, 'Run once', n, 'done', '----' * 9,
                                           use_time, '\n'))
                    if n % 200 == 0:
                        current_time = time.time()
                        Logger.critical('{} events have been processed! Use time: {}. Current time: {}'.format(n, current_time - step_time, self.clock_time))
                        step_time = current_time

                else:
                    self.__clock_time = kwargs['terminate']
                    return head is not None
        elif 'event_count' in kwargs:
            if self.__parent is not None:
                return self.__parent.run(event_count=kwargs['event_count'])
            while kwargs['event_count'] > 0:
                kwargs['event_count'] -= 1
                r = self.run()
                if not r:
                    return False
            return True
        elif 'speed' in kwargs:
            if self.__parent is not None:
                return self.__parent.run(speed=kwargs['speed'])
            rtn = True
            if self.__realtime_for_last_run is not None:
                time_gap = datetime.datetime.now() - self.__realtime_for_last_run
                time_gap = datetime.timedelta(seconds=time_gap.total_seconds() * kwargs['speed'])
                rtn = self.run(terminate=self.clock_time + time_gap)
            self.__realtime_for_last_run = datetime.datetime.now()
            return rtn
        else:
            raise TypeError()

    def add_child(self, child):
        self.__children.append(child)
        child.parent = self
        self.__on_warmup += child.on_warmup
        return child

    def add_hour_counter(self, keep_history=False):
        hc = HourCounter(self, keep_history=keep_history)
        self.__hour_counters.append(hc)
        self.__on_warmup.append([hc.warmed_up, {'clock_time': self.__clock_time}])
        return hc

    def to_string(self):
        _id = self.__id
        if self.__id is None or len(self.__id) == 0:
            _id = type(self)
        _id += '#' + str(self.__index)
        return _id

    def warmup(self, *args, **kwargs):
        if 'period' in kwargs:
            if self.__parent is not None:
                return self.__parent.warmup(kwargs['period'])
            return self.warmup(self.clock_time + kwargs['period'])
        elif 'till' in kwargs:
            if self.__parent is not None:
                return self.__parent.warmup(kwargs['till'])
            result = self.run(terminate=kwargs['till'])
            for func in self.__on_warmup:
                if len(func) == 1:
                    func[0]()
                else:
                    func[0](**func[1])
            return result

    def warmup_handler(self):
        return -1
