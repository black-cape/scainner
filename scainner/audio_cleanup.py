import threading
import time

from mongo import clear_audio_older_than_30_days


def audio_cleanup():
    print("Audio cleanup thread started")
    while True:
        print("Cleaning up audio files over 30 days old...")
        clear_audio_older_than_30_days()
        time.sleep(24 * 60 * 60)  # Run every 24 hours


def start_audio_cleanup_thread():
    cleanup_thread = threading.Thread(target=audio_cleanup, daemon=True)
    cleanup_thread.start()
    return cleanup_thread
