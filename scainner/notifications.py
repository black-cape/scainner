import re

import requests


class SlackNotificationsClient:
    """
    Send notifications to a Slack webhook if the transcription matches a regex pattern.
    """

    def __init__(self, webhook_url: str, regex_patterns: list[str] = None):
        self.webhook_url = webhook_url
        self.regex_patterns = regex_patterns

    def send_notification(self, transcription: str) -> bool:
        """
        Send a notification to the Slack webhook with the transcription.

        Args:
            transcription: The transcription to send to the Slack webhook.

        Returns:
            True if the notification was sent successfully, False otherwise.
        """
        try:
            resp = requests.post(self.webhook_url, json={"text": transcription})
            print(f"DEBUG: Posted to webhook and got {resp.status_code} back.")
            return True
        except Exception as e:
            print(f"ERROR: Failed to post to webhook {e}")
            return False

    def notify_if_matches(self, transcription: str) -> bool:
        """
        Notify if the transcription matches a regex pattern.

        Args:
            transcription: The transcription to check for matches.

        Returns:
            True if a notification was sent, False otherwise.
        """
        if not self.regex_patterns:
            return self.send_notification(transcription)
        for pattern in self.regex_patterns:
            if re.search(pattern, transcription, re.IGNORECASE):
                return self.send_notification(transcription)
        return False
