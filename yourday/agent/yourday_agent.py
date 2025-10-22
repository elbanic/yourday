"""YourDay Agent using Strands SDK with AWS Bedrock."""

import asyncio
from datetime import datetime
from strands import Agent
from yourday.clients.weather_client import WeatherClient
from yourday.clients.news_client import NewsClient
from yourday.clients.obsidian_client import ObsidianClient
from yourday.exceptions import AgentExecutionError


class YourDayAgent:
    """Strands SDK agent for generating daily summaries."""

    def __init__(
        self,
        weather_client: WeatherClient,
        news_client: NewsClient,
        obsidian_client: ObsidianClient,
        model_id: str,
    ):
        self.weather_client = weather_client
        self.news_client = news_client
        self.obsidian_client = obsidian_client
        self.model_id = model_id
        self.agent = self._initialize_agent()

    def _initialize_agent(self) -> Agent:
        """Initialize Strands agent with Bedrock model."""
        return Agent(model=self.model_id)

    def run(self) -> str:
        """Execute the daily summary workflow (sync wrapper)."""
        return asyncio.run(self._run_async())

    async def _run_async(self) -> str:
        """Execute the daily summary workflow.

        Returns:
            str: File path where content was posted in Obsidian

        Raises:
            AgentExecutionError: If workflow fails
        """
        try:
            # Collect data
            weather_data = self.weather_client.fetch_weather()
            news_data = self.news_client.fetch_top_news(limit=10)

            # Generate filename and content
            today = datetime.now().strftime("%Y-%m-%d")
            file_path = f"YourDayStart/Daily Summary-{today}.md"

            # Generate summary using Bedrock
            prompt = self._create_summary_prompt(weather_data, news_data, today)
            result = await self.agent.invoke_async(prompt=prompt)

            # Extract content from result (use __str__ to get text)
            content = str(result)

            print(f"\nGenerated content ({len(content)} chars):")
            print(content[:200] + "..." if len(content) > 200 else content)

            # Post to Obsidian
            self.obsidian_client.put_content(file_path, content)

            return file_path

        except Exception as e:
            raise AgentExecutionError(f"Agent workflow failed: {str(e)}")

    def _create_summary_prompt(
        self, weather_data: dict, news_data: list[dict], date: str
    ) -> str:
        """Create prompt for agent to generate formatted summary."""
        weather_info = f"Temperature: {weather_data['temperature']}°C, Condition: {weather_data['condition']}, Humidity: {weather_data['humidity']}%, Wind: {weather_data['wind_speed']} m/s"

        news_list = "\n".join(
            [
                f"{i}. {article['title']} ({article['source']}) - {article['description'][:100]}... URL: {article['url']}"
                for i, article in enumerate(news_data, 1)
            ]
        )

        return f"""Generate a well-formatted daily summary in Markdown format for {date}.

Weather data: {weather_info}

Top 10 news headlines:
{news_list}

Format the output as:
# Daily Weather & News

## 🌤 Weather
- Temperature: [value]°C
- Condition: [value]
- Humidity: [value]%
- Wind Speed: [value] m/s

## 📰 Top 10 News
1. **[Headline]** ([Source])
   [Brief description]
   [News Link]([url])

Keep descriptions concise and well-formatted. Return ONLY the markdown content, no additional text."""
