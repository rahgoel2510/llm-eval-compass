"""Chatbot Arena ELO score scraper."""

import requests


class ArenaScoreScraper:
    """Fetches latest Chatbot Arena ELO rankings."""

    # TODO: Update with current LMSYS Chatbot Arena API/data URL
    URL = "https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard"

    def fetch_latest(self) -> dict:
        """Fetch latest ELO scores. Returns dict of model_name -> elo_score."""
        response = requests.get(self.URL, timeout=30)
        response.raise_for_status()
        # TODO: Parse the response HTML/JSON to extract ELO scores
        # Return format: {"gpt-4o": 1287, "claude-sonnet": 1275, ...}
        raise NotImplementedError("Parser not yet implemented — see TODO above")
