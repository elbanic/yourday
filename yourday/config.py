"""Configuration management for YourDay application."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

from yourday.exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration for YourDay application."""

    news_api_key: str
    bedrock_model_id: str
    location: str
    obsidian_api_key: str
    obsidian_base_url: str = "http://localhost:27123"
    aws_region: str = "us-east-1"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables.

        Returns:
            Config: Configuration instance with values from environment

        Raises:
            ConfigurationError: If required environment variables are missing
        """
        required_vars = {
            "NEWS_API_KEY": "news_api_key",
            "BEDROCK_MODEL_ID": "bedrock_model_id",
            "LOCATION": "location",
            "OBSIDIAN_API_KEY": "obsidian_api_key",
        }

        missing = [var for var in required_vars.keys() if not os.getenv(var)]
        if missing:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return cls(
            news_api_key=os.getenv("NEWS_API_KEY"),
            bedrock_model_id=os.getenv("BEDROCK_MODEL_ID"),
            location=os.getenv("LOCATION"),
            obsidian_api_key=os.getenv("OBSIDIAN_API_KEY"),
            obsidian_base_url=os.getenv("OBSIDIAN_BASE_URL", "http://localhost:27123"),
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
