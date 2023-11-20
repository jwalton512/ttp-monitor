import os
from typing import Any

import requests


def notify_slots(slots: list[dict[str, Any]]) -> bool:
    url = os.environ.get("NOTIFY_WEBHOOK_URL", "")
    response = requests.post(url, json=slots)
    return response.ok


def heartbeat(attr: dict[str, Any]) -> bool:
    url = os.environ.get("HEARTBEAT_WEBHOOK_URL", "")
    response = requests.post(url, json=attr)
    return response.ok
