"""
Scan Fairfax County PD's Reston Dispatch and send alerts for calls in area 5xx.
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
    else "https://api.openmhz.com/ffxco/calls?filter-type=talkgroup&filter-code=1083%2C1077"
)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLEEP_INTERVAL = os.getenv("SLEEP_INTERVAL")
SLEEP_INTERVAL = int(SLEEP_INTERVAL) if SLEEP_INTERVAL else 60


def call_contains_area_5xx(text):
    """
    Incidents that occur in my neighborhood are announced to be in "area 5xx"
    """
    pattern = r"\barea[ ,;-]*5\d{2}\b"
    return re.search(pattern, text)


def call_contains_area_five_then_number(text):
    """
    Sometimes the model transcribes the area codes in words instead of numbers.
    """
    pattern = r"\barea[ ,;-]*five[ ,;-]*(zero|ten|eleven|twenty|thirty|hundred)([ ,;-]*(one))?\b"
    return re.search(pattern, text)


def main():
    scainner = Scainner(
        endpoint=ENDPOINT, model_size="distil-medium.en", compute_type="int8"
    )
    last_call_time = datetime.now(tz=timezone.utc)
    try:
        while True:
            print(f"Fetching calls at {last_call_time}")
            for call in scainner.scan(last_call_time):
                print(call)
                normalized = call.lower()
                if call_contains_area_5xx(
                    normalized
                ) or call_contains_area_five_then_number(normalized):
                    resp = requests.post(SLACK_WEBHOOK_URL, json={"text": call})
                    print(f"Sent webhook msg and got {resp.status_code}")
            last_call_time = datetime.now(tz=timezone.utc)
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping scan.")


main()
