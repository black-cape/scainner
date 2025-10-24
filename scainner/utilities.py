from datetime import datetime, timezone

import ffmpeg
import numpy as np


def load_audio(file_bytes: bytes, sr: int = 16_000) -> np.ndarray:
    """
    Use file's bytes and transform to mono waveform, resampling as necessary.
    Copied from https://github.com/openai/whisper/blob/main/whisper/audio.py#L25

    Parameters

    param file_bytes: The bytes of the audio file
    param sr: The sample rate to resample the audio if necessary

    return: A NumPy array containing the audio waveform, in float32 dtype.
    """
    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input("pipe:", threads=0)
            .output(
                "pipe:",
                format="s16le",
                acodec="pcm_s16le",
                ac=1,
                ar=sr,
                loglevel="quiet",
            )
            .run_async(pipe_stdin=True, pipe_stdout=True)
        ).communicate(input=file_bytes)

    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def extract_time(time_string: str) -> datetime:
    return datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc
    )
