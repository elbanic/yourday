"""Weather client for fetching data from Open-Meteo API."""

import requests
from yourday.exceptions import WeatherAPIError


class WeatherClient:
    """Client for fetching weather data from Open-Meteo API."""

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, location: str):
        self.location = location
        self.latitude, self.longitude = self._geocode_location()

    def _geocode_location(self) -> tuple[float, float]:
        """Convert location name to coordinates using Open-Meteo geocoding API."""
        params = {"name": self.location, "count": 1, "language": "en", "format": "json"}

        try:
            response = requests.get(self.GEOCODING_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                raise WeatherAPIError(f"Location not found: {self.location}")

            result = data["results"][0]
            return result["latitude"], result["longitude"]
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Failed to geocode location: {str(e)}")

    def fetch_weather(self) -> dict:
        """Fetch current weather data.

        Returns:
            dict: Weather data with temperature, condition, humidity, wind_speed

        Raises:
            WeatherAPIError: If API request fails
        """
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto",
        }

        try:
            response = requests.get(self.WEATHER_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data["current"]
            return {
                "temperature": current["temperature_2m"],
                "condition": self._weather_code_to_condition(current["weather_code"]),
                "humidity": current["relative_humidity_2m"],
                "wind_speed": current["wind_speed_10m"],
            }
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Failed to fetch weather data: {str(e)}")
        except KeyError as e:
            raise WeatherAPIError(f"Invalid API response format: {str(e)}")

    def _weather_code_to_condition(self, code: int) -> str:
        """Convert WMO weather code to readable condition."""
        conditions = {
            0: "Clear",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light Drizzle",
            53: "Drizzle",
            55: "Heavy Drizzle",
            61: "Light Rain",
            63: "Rain",
            65: "Heavy Rain",
            71: "Light Snow",
            73: "Snow",
            75: "Heavy Snow",
            80: "Light Showers",
            81: "Showers",
            82: "Heavy Showers",
            95: "Thunderstorm",
            96: "Thunderstorm",
            99: "Thunderstorm",
        }
        return conditions.get(code, "Unknown")
