from datetime import datetime

import cloudscraper
from faster_whisper import WhisperModel

from scainner.utilities import extract_time, load_audio


class Scainner:
    def __init__(self, endpoint: str, model_size: str, compute_type: str) -> None:
        self.endpoint = endpoint
        self.model = WhisperModel(model_size, compute_type=compute_type)
        self.scraper = cloudscraper.create_scraper()

    def get_calls(self):
        resp = self.scraper.get(self.endpoint)
        return resp.json()["calls"]

    def scan(self, minimum_call_time: datetime | None = None):
        calls = self.get_calls()
        if minimum_call_time:
            calls = [
                call for call in calls if extract_time(call["time"]) > minimum_call_time
            ]
        for call in calls[::-1]:
            audio = self.scraper.get(call["url"])
            audio_buffer = load_audio(audio.content)
            segments, _ = self.model.transcribe(audio_buffer)
            text = ""
            for segment in segments:
                text += segment.text
            yield text
