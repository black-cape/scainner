"""
Scan MoCo Public Safety.
"""

import os
import re
import time
from datetime import datetime, timezone

import requests

from scainner import Scainner

ENDPOINT = os.getenv("ENDPOINT")
ENDPOINT = (
    ENDPOINT
    if ENDPOINT
    else "https://api.openmhz.com/mocomdps/calls"
)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLEEP_INTERVAL = os.getenv("SLEEP_INTERVAL")
SLEEP_INTERVAL = int(SLEEP_INTERVAL) if SLEEP_INTERVAL else 60


def main():
    scainner = Scainner(
        endpoint=ENDPOINT, model_size="distil-large-v3", compute_type="int8"
    )

    last_call_time = datetime.now(tz=timezone.utc)
    try:
        while True:
            print(f"Fetching calls at {last_call_time}")
            for speaker, call in scainner.scan(last_call_time):
                # could limit to TKPK which is talkgroup 6375
                print(f"{speaker}: {call}")
                normalized = call.lower()
                # if call_contains_area_5xx(
                #     normalized
                # ) or call_contains_area_five_then_number(normalized):
                #     resp = requests.post(SLACK_WEBHOOK_URL, json={"text": call})
                #     print(f"Sent webhook msg and got {resp.status_code}")
            last_call_time = datetime.now(tz=timezone.utc)
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping scan.")


main()
