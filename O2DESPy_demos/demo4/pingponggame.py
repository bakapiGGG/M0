from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
from datetime import timedelta
import datetime
import time
import random
from O2DESPy_demos.demo4.pingpongplayer import PingPongPlayer

class PingPongGame(Sandbox):
    def __init__(self, index_player1, delay_time_expected_player1, delay_time_CV_player1,
     index_player2, delay_time_expected_player2, delay_time_CV_player2, seed = 0):
        super().__init__()
        self.__index_player1 = index_player1
        self.__delay_time_expected_player1 = delay_time_expected_player1
        self.__delay_time_CV_player1 = delay_time_CV_player1
        self.__index_player2 = index_player2
        self.__delay_time_expected_player2 = delay_time_expected_player2
        self.__delay_time_CV_player2 = delay_time_CV_player2

        self.__player1 = self.add_child(PingPongPlayer(self.__index_player1, self.__delay_time_expected_player1, self.__delay_time_CV_player1))
        self.__player2 = self.add_child(PingPongPlayer(self.__index_player2, self.__delay_time_expected_player2, self.__delay_time_CV_player2))

        self.__player1.on_send = [self.player2.receive]
        self.__player2.on_send = [self.player1.receive]

        self.__seed = seed 

        self.schedule([self.player1.receive], timedelta(seconds=0))

    @property
    def index_player1(self):
        return self.__index_player1

    @index_player1.setter
    def index_player1(self, value):
        self.__index_player1 = value

    @property
    def delay_time_expected_player1(self):
        return self.__delay_time_expected_player1

    @delay_time_expected_player1.setter
    def delay_time_expected_player1(self, value):
        self.__delay_time_expected_player1 = value

    @property
    def delay_time_CV_player1(self):
        return self.__delay_time_CV_player1

    @delay_time_CV_player1.setter
    def delay_time_CV_player1(self, value):
        self.__delay_time_CV_player1 = value
    
    @property
    def index_player2(self):
        return self.__index_player2

    @index_player2.setter
    def index_player2(self, value):
        self.__index_player2 = value
    
    @property
    def delay_time_expected_player2(self):
        return self.__delay_time_expected_player2

    @delay_time_expected_player2.setter
    def delay_time_expected_player2(self, value):
        self.__delay_time_expected_player2 = value

    @property
    def delay_time_CV_player2(self):
        return self.__delay_time_CV_player2

    @delay_time_CV_player2.setter
    def delay_time_CV_player2(self, value):
        self.__delay_time_CV_player2 = value
    
    @property
    def player1(self):
        return self.__player1

    @property
    def player2(self):
        return self.__player2
    
    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value

if __name__ == '__main__':
    run_code = 'O2DESPy demo 4'
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
    Logger.info("Demo 3 - PingPong")
    sim4 = PingPongGame(1,1,1,2,2,2)
    sim4.run(duration=datetime.timedelta(hours=1))
    Logger.critical('use time {}'.format(time.time() - start_time))