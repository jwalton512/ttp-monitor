import json
import urllib.parse
from datetime import UTC, date, datetime
from typing import Any

import requests
from pytz import timezone


class Slot:
    def __init__(
        self, active: int, timestamp: str, timezone: str | None = None
    ) -> None:
        self.active = active
        self.timestamp = timestamp
        self.timezone = timezone

    def is_active(self, use_time: bool = True) -> bool:
        if self.active == 0:
            return False

        if use_time and self.timezone:
            now = (
                datetime.now(UTC)
                .astimezone(timezone(self.timezone))
                .replace(tzinfo=None)
            )
            slot_time = datetime.fromisoformat(self.timestamp)
            if now > slot_time:
                return False

        return True

    def to_json(self) -> dict:
        return self.__dict__


def get_location_tz(location_id: int) -> str | None:
    url = "https://ttp.cbp.dhs.gov/schedulerapi/locations/"
    response = requests.get(url)
    if response.ok:
        location = next((l for l in response.json() if l["id"] == location_id), {})
        return location.get("tzData")


def get_slots(
    location: int, start_date: date, end_date: date, timezone: str | None = None
) -> list[Slot]:
    start_ts = urllib.parse.quote(start_date.strftime("%Y-%m-%dT%H:%M:%S"))
    end_ts = urllib.parse.quote(end_date.strftime("%Y-%m-%dT%H:%M:%S"))
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/locations/{location}/slots?startTimestamp={start_ts}&endTimestamp={end_ts}"

    slots = []
    response = requests.get(url)
    if response.ok:
        for slot in response.json():
            slots.append(Slot(int(slot["active"]), slot["timestamp"], timezone))

    return slots
