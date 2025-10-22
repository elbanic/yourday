"""News client for fetching data from GNews API."""

import requests
from yourday.exceptions import NewsAPIError


class NewsClient:
    """Client for fetching top news headlines from GNews API."""

    BASE_URL = "https://gnews.io/api/v4/top-headlines"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_top_news(self, limit: int = 10) -> list[dict]:
        """Fetch top news headlines.

        Args:
            limit: Number of articles to fetch (default: 10)

        Returns:
            list[dict]: List of news articles with title, description, url, source, published_at

        Raises:
            NewsAPIError: If API request fails
        """
        params = {"token": self.api_key, "lang": "en", "max": limit}

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = []
            for article in data.get("articles", []):
                articles.append(
                    {
                        "title": article["title"],
                        "description": article["description"],
                        "url": article["url"],
                        "source": article["source"]["name"],
                        "published_at": article["publishedAt"],
                    }
                )

            return articles
        except requests.exceptions.RequestException as e:
            raise NewsAPIError(f"Failed to fetch news data: {str(e)}")
        except (KeyError, IndexError) as e:
            raise NewsAPIError(f"Invalid API response format: {str(e)}")
