import os
import time
from datetime import date

from ttp_monitor.watcher import Watcher

HEARTBEAT_INTERVAL = 0
PROCESS_THROTTLE_SECS = 30
AFTER_SUCCESS_THROTTLE_SECS = 300


class Worker:
    def __init__(self, location: int, start_date: date, end_date: date) -> None:
        self.watcher = Watcher(location, start_date, end_date)
        self.heartbeat_interval = int(
            os.environ.get("HEARTBEAT_INTERVAL", HEARTBEAT_INTERVAL)
        )
        self.last_hearbeat = time.time()

    def run(self) -> None:
        while True:
            result = self._process()
            self._hearbeat(result)

    def _sleep(self, duration: float) -> None:
        time.sleep(duration)

    def _process(self) -> bool:
        start_time = time.time()
        result = self.watcher.process()
        elapsed = time.time() - start_time

        throttle_secs = float(
            os.environ.get("PROCESS_THROTTLE_SECS", PROCESS_THROTTLE_SECS)
        )
        after_success_throttle_secs = float(
            os.environ.get("AFTER_SUCCESS_THROTTLE_SECS", AFTER_SUCCESS_THROTTLE_SECS)
        )

        duration = (after_success_throttle_secs if result else throttle_secs) - elapsed
        self._sleep(duration)
        return result

    def _hearbeat(self, last_result: bool) -> None:
        if last_result:
            self.last_hearbeat = time.time()
            return

        if self.heartbeat_interval:
            elapsed = time.time() - self.last_hearbeat
            if elapsed >= self.heartbeat_interval:
                self.watcher.heartbeat()
                self.last_hearbeat = time.time()
