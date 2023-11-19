import os
import time
from datetime import date
from typing import Any, Callable

from ttp_monitor.watcher import Watcher

PROCESS_THROTTLE_SECS = 30
PROCESS_AFTER_NOTIFY_THROTTLE_SECS = 300


class Worker:
    def __init__(self, location: int, start_date: date, end_date: date) -> None:
        self.watcher = Watcher(location, start_date, end_date)
        self.last_result = False

    def run(self) -> None:
        while True:
            self.last_result = self._throttle(
                self._process_running, self._throttle_secs
            )

    @property
    def _throttle_secs(self) -> int:
        throttle = int(os.environ.get("PROCESS_THROTTLE_SECS", PROCESS_THROTTLE_SECS))
        after_notify_throttle = int(
            os.environ.get(
                "PROCESS_AFTER_NOTIFY_THROTTLE_SECS", PROCESS_AFTER_NOTIFY_THROTTLE_SECS
            )
        )
        return after_notify_throttle if self.last_result else throttle

    def _throttle(
        self, func: Callable[..., Any], throttle_secs: float, *args, **kwargs
    ) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        sleep_duration = throttle_secs - elapsed

        self._sleep(sleep_duration)
        return result

    def _sleep(self, duration: float) -> None:
        time.sleep(duration)

    def _process_running(self) -> bool:
        return self.watcher.process()
