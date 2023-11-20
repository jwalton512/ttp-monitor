from datetime import date

from ttp_monitor import webhook
from ttp_monitor.ttp import get_location_tz, get_slots


class Watcher:
    def __init__(self, location: int, start_date: date, end_date: date) -> None:
        self.location = location
        self.location_tz = get_location_tz(location)
        self.start_date = start_date
        self.end_date = end_date

    def process(self) -> bool:
        slots = get_slots(
            location=self.location,
            start_date=self.start_date,
            end_date=self.end_date,
            timezone=self.location_tz,
        )
        active = [s for s in slots if s.is_active(use_time=True)]
        if active:
            webhook.notify_slots(active)
            return True

        return False

    def heartbeat(self) -> None:
        webhook.heartbeat(
            {
                "location": self.location,
                "start_date": str(self.start_date),
                "end_date": str(self.end_date),
            }
        )
