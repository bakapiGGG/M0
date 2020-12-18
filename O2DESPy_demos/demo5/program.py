from O2DESPy_demos.demo5.mmc_queue_pull import MMcQueuePull
from O2DESPy.log.logger import Logger
from O2DESPy.application.config import Config
import datetime
import time


if __name__ == '__main__':
    run_code = 'O2DESPy demo 5'
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
    Logger.info("Demo 5 - MMcQueuePull")
    sim1 = MMcQueuePull(capacity=1, hourly_arrival_rate=4, hourly_service_rate=5)
    hc1 = sim1.add_hour_counter()
    sim1.run(duration=datetime.timedelta(hours=100))
    Logger.critical('use time {}'.format(time.time() - start_time))