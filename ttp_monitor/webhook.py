import os
from typing import Any

import requests

from ttp_monitor.ttp import Slot


def notify_slots(slots: list[Slot]) -> bool:
    url = os.environ.get("NOTIFY_WEBHOOK_URL", "")
    json = [s.to_json() for s in slots]
    response = requests.post(url, json=json)
    return response.ok


def heartbeat(attr: dict[str, Any]) -> bool:
    url = os.environ.get("HEARTBEAT_WEBHOOK_URL", "")
    response = requests.post(url, json=attr)
    return response.ok
