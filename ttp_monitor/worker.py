import os
import time
from datetime import date
from typing import Any, Callable

from ttp_monitor.watcher import Watcher

PROCESS_THROTTLE_SECS = 30
AFTER_SUCCESS_THROTTLE_SECS = 300


class Worker:
    def __init__(self, location: int, start_date: date, end_date: date) -> None:
        self.watcher = Watcher(location, start_date, end_date)

    def run(self) -> None:
        while True:
            self._process()

    def _sleep(self, duration: float) -> None:
        time.sleep(duration)

    def _process(self) -> None:
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
