import time
from dataclasses import dataclass
from datetime import datetime
from json.decoder import JSONDecodeError

from cloudscraper import create_scraper
from faster_whisper import WhisperModel
from requests.exceptions import ConnectionError
from utilities import date_string_to_datetime, load_audio


@dataclass
class Call:
    src_id: str
    url: str
    star_count: int
    length: int
    timestamp: datetime
    frequency: int
    talkgroup_number: int
    model_size: str
    transcription: str = None
    transcription_time: float = None
    audio: bytes | None = None


class Scainner:
    """
    Scan OpenMHz for calls and transcribe them using a Whisper model.
    """

    def __init__(self, endpoint: str, model_size: str, compute_type: str):
        self.endpoint = endpoint
        self.model_size = model_size
        self.model = WhisperModel(self.model_size, compute_type=compute_type)
        self.http_client = create_scraper()

    def fetch_calls(self):
        """
        Fetch calls from the OpenMHz API.

        Returns:
            A list of Call objects.

        Raises:
            JSONDecodeError: If the response is not valid JSON.
            ConnectionError: If a connection error occurs when fetching calls.
            Exception: If an unspecified error occurs when fetching calls.
        """
        try:
            resp = self.http_client.get(self.endpoint)
            calls = resp.json()["calls"]
            return [
                Call(
                    src_id=call["_id"],
                    url=call["url"],
                    star_count=call["star"],
                    length=call["len"],
                    timestamp=date_string_to_datetime(call["time"]),
                    frequency=call["freq"],
                    talkgroup_number=call["talkgroupNum"],
                    model_size=self.model_size,
                )
                for call in calls[::-1]
            ]
        except JSONDecodeError:
            print(
                f"ERROR: Failed to decode call JSON. Response code: {resp.status_code} Response test: {resp.text}"
            )
            return []
        except ConnectionError as e:
            print(f"ERROR: A connection error occurred when fetching calls. {e}")
            return []
        except Exception as e:
            print(f"ERROR: An unspecified error occurred when fetching calls. {e}")
            return []

    def transcribe_calls(self, min_call_time: datetime | None = None):
        """
        Transcribe calls from the OpenMHz API.

        Args:
            min_call_time: The minimum call time to transcribe.

        Returns:
            A generator of Call objects.
        """
        calls = self.fetch_calls()
        for call in calls:
            if call.timestamp <= min_call_time:
                continue
            try:
                audio = self.http_client.get(call.url).content
            except ConnectionError as e:
                print(
                    f"ERROR: A connection error occurred when fetching audio. Call  {call.frequency}@{call.timestamp} will be skipped. {e}"
                )
                continue
            audio_waveform = load_audio(audio)
            start_time = time.time()
            segments, _ = self.model.transcribe(audio_waveform)
            transcription = ""
            for segment in segments:
                transcription += segment.text
            call.transcription_time = time.time() - start_time
            call.transcription = transcription
            call.audio = audio
            yield call
