from O2DESPy.sandbox import Sandbox
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
import datetime
from O2DESPy_demos.demo4.pingpongplayer import PingPongPlayer


class PingPongGame(Sandbox):
    def __init__(self, index_player1, delay_time_expected_player1, delay_time_CV_player1,
                 index_player2, delay_time_expected_player2, delay_time_CV_player2, seed=0):
        super().__init__()
        self.index_player1 = index_player1
        self.delay_time_expected_player1 = delay_time_expected_player1
        self.delay_time_CV_player1 = delay_time_CV_player1
        self.index_player2 = index_player2
        self.delay_time_expected_player2 = delay_time_expected_player2
        self.delay_time_CV_player2 = delay_time_CV_player2

        self.player1 = self.add_child(
            PingPongPlayer(self.index_player1, self.delay_time_expected_player1, self.delay_time_CV_player1))
        self.player2 = self.add_child(
            PingPongPlayer(self.index_player2, self.delay_time_expected_player2, self.delay_time_CV_player2))

        self.player1.on_send.add_event_method(self.player2.receive)
        self.player2.on_send.add_event_method(self.player1.receive)

        self.seed = seed

        self.schedule(self.player1.receive)


if __name__ == '__main__':
    # Demo 4
    Logger.info("Demo 3 - PingPong")
    sim4 = PingPongGame(1, 1, 1, 2, 2, 2)
    sim4.run(duration=datetime.timedelta(hours=1))
