import urllib.parse
from datetime import date
from typing import Any

import requests


def get_slots(location: int, start_date: date, end_date: date) -> list[dict[str, Any]]:
    start_ts = urllib.parse.quote(start_date.strftime("%Y-%m-%dT%H:%M:%S"))
    end_ts = urllib.parse.quote(end_date.strftime("%Y-%m-%dT%H:%M:%S"))
    url = f"https://ttp.cbp.dhs.gov/schedulerapi/locations/{location}/slots?startTimestamp={start_ts}&endTimestamp={end_ts}"

    response = requests.get(url)
    return response.json() if response.ok else []
