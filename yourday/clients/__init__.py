"""Client modules for external API integrations."""

from yourday.clients.weather_client import WeatherClient
from yourday.clients.news_client import NewsClient

__all__ = ["WeatherClient", "NewsClient"]
