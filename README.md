# YourDay - Daily Summary Automation

An AI-powered daily summary agent that automatically fetches weather and news, generates a formatted report using AWS Bedrock Claude Sonnet 4, and posts it to your Obsidian vault.

## Features

- 🌤 **Weather Data** - Fetches current weather from Open-Meteo (free, no API key needed)
- 📰 **Top 10 News** - Gets latest headlines from GNews API
- 🤖 **AI Summarization** - Uses AWS Bedrock Claude Sonnet 4 for formatting
- 📝 **Obsidian Integration** - Automatically posts to your vault via MCP server

## Prerequisites

- Python 3.10 or higher
- AWS account with Bedrock access (Claude Sonnet 4.5)
- GNews API key ([Get one here](https://gnews.io/))
- Obsidian with MCP server running ([mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian))

## Installation

### 1. Clone and Setup Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -e .
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Location Configuration
LOCATION=Seattle

# GNews API Configuration
NEWS_API_KEY=your_gnews_api_key_here

# AWS Bedrock Configuration
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
AWS_REGION=us-east-1

# Obsidian API Configuration
OBSIDIAN_API_KEY=your_obsidian_api_key_here
OBSIDIAN_BASE_URL=http://localhost:27123

# Optional Configuration
LOG_LEVEL=INFO
```

### 4. Setup Obsidian MCP Server

Install and run the Obsidian MCP server:

```bash
# Follow instructions at: https://github.com/MarkusPfundstein/mcp-obsidian
# The server should be running on port 27123 (default)
```

### 5. Configure AWS Credentials

Ensure your AWS credentials are configured for Bedrock access:

```bash
aws configure
```

Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

## Usage

### Run Daily Summary

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the agent
yourday run
```

This will:
1. Fetch current weather for your location
2. Get top 10 news headlines
3. Generate a formatted Markdown summary using Claude
4. Post the summary to Obsidian at `YourDayStart/Daily Summary-YYYY-MM-DD.md`

### Output Format

The generated summary looks like this:

```markdown
# Daily Summary - 2025-10-22

## 🌤 Weather
- Temperature: 13°C
- Condition: Cloudy
- Humidity: 65%
- Wind Speed: 3.5 m/s

## 📰 Top 10 News
1. **Headline Title** (Source Name)
   Brief description of the article...
   [Read more](https://article-url.com)

2. **Another Headline** (Source Name)
   Brief description...
   [Read more](https://article-url.com)
```

## Project Structure

```
yourday/
├── agent/
│   └── yourday_agent.py      # Main Strands SDK agent
├── clients/
│   ├── weather_client.py     # Open-Meteo API client
│   ├── news_client.py        # GNews API client
│   └── obsidian_client.py    # Obsidian MCP client
├── cli.py                    # Command-line interface
├── config.py                 # Configuration management
└── exceptions.py             # Custom exceptions
```

## Troubleshooting

### Weather API Issues
- Open-Meteo is free and requires no API key
- Check your internet connection
- Verify the location name is valid

### News API Issues
- Verify your GNews API key is valid
- Check API rate limits (free tier: 100 requests/day)
- Get a new key at https://gnews.io/

### Obsidian Connection Issues
- Ensure MCP server is running on port 27123
- Check `OBSIDIAN_API_KEY` matches your server configuration
- Verify `OBSIDIAN_BASE_URL` is correct

### AWS Bedrock Issues
- Confirm you have Bedrock access in your AWS account
- Verify Claude Sonnet 4 model is available in your region
- Check AWS credentials are properly configured

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black yourday/
```

### Type Checking

```bash
mypy yourday/
```

## License

MIT

## Contributing

This is a personal project. Feel free to fork and adapt for your own use.
