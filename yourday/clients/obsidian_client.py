"""Obsidian client for posting content via REST API."""

import requests
from yourday.exceptions import ObsidianAPIError


class ObsidianClient:
    """Client for posting content to Obsidian vault via REST API."""

    def __init__(self, api_key: str, base_url: str = "http://localhost:27123"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def put_content(self, file_path: str, content: str) -> None:
        """Post content to Obsidian vault.

        Args:
            file_path: Path within vault (e.g., "YourDayStart/Daily Summary-2025-01-01.md")
            content: Markdown content to write

        Raises:
            ObsidianAPIError: If API request fails
        """
        url = f"{self.base_url}/vault/{file_path}"

        try:
            response = requests.put(
                url,
                headers={**self.headers, "Content-Type": "text/markdown"},
                data=content.encode("utf-8"),
                timeout=10,
            )
            response.raise_for_status()
            print(f"Obsidian API response: {response.status_code}")
            if response.text:
                print(f"Response body: {response.text}")
        except requests.exceptions.RequestException as e:
            raise ObsidianAPIError(f"Failed to post to Obsidian: {str(e)}")
