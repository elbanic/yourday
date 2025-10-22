"""Custom exceptions for YourDay application."""


class YourDayError(Exception):
    """Base exception for YourDay application."""


class WeatherAPIError(YourDayError):
    """Raised when OpenWeatherMap API fails."""


class NewsAPIError(YourDayError):
    """Raised when GNews API fails."""


class AgentExecutionError(YourDayError):
    """Raised when agent workflow fails."""


class ObsidianMCPError(YourDayError):
    """Raised when Obsidian MCP posting fails."""


class ObsidianAPIError(YourDayError):
    """Raised when Obsidian API request fails."""


class ConfigurationError(YourDayError):
    """Raised when required environment variables are missing."""
