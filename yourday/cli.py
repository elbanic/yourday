"""CLI interface for YourDay application."""

import sys
from yourday.config import Config
from yourday.clients.weather_client import WeatherClient
from yourday.clients.news_client import NewsClient
from yourday.clients.obsidian_client import ObsidianClient
from yourday.agent.yourday_agent import YourDayAgent
from yourday.exceptions import YourDayError


def run_command() -> None:
    """Execute the daily summary generation workflow."""
    try:
        print("Loading configuration...")
        config = Config.from_env()

        print("Initializing clients...")
        weather_client = WeatherClient(config.location)
        news_client = NewsClient(config.news_api_key)
        obsidian_client = ObsidianClient(
            config.obsidian_api_key, config.obsidian_base_url
        )

        print("Initializing YourDay Agent...")
        agent = YourDayAgent(
            weather_client, news_client, obsidian_client, config.bedrock_model_id
        )

        print("Generating daily summary...")
        file_path = agent.run()

        print(f"\n✓ Success! Daily summary posted to: {file_path}")

    except YourDayError as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_command()
    else:
        print("Usage: yourday run")
        sys.exit(1)


if __name__ == "__main__":
    main()
