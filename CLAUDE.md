# CLAUDE.md

## Project Overview

YourDay is a Python CLI application that generates AI-powered daily summaries. It fetches weather data and top news headlines, uses AWS Bedrock (Claude Sonnet) to generate a formatted Markdown summary, and posts it to an Obsidian vault via REST API.

**Version:** 0.1.0
**Python:** >= 3.10
**License:** MIT

## Quick Reference

```bash
# Install
pip install -e .           # Standard install
pip install -e ".[dev]"    # With dev dependencies (pytest, black, mypy)

# Run
yourday run                # Generate and post daily summary

# Dev tools
black .                    # Format code (line length: 88)
mypy yourday/              # Type check (strict: disallow_untyped_defs)
pytest                     # Run tests
```

## Project Structure

```
yourday/
├── pyproject.toml              # Build config, dependencies, tool settings
├── .env.example                # Required environment variables template
├── tests/
│   └── __init__.py
└── yourday/                    # Main package
    ├── __init__.py             # Package root, exports __version__
    ├── cli.py                  # CLI entry point (yourday command)
    ├── config.py               # Dataclass-based config from env vars
    ├── exceptions.py           # Custom exception hierarchy
    ├── agent/
    │   └── yourday_agent.py    # Strands SDK agent orchestrating the workflow
    └── clients/
        ├── weather_client.py   # Open-Meteo API (geocoding + weather)
        ├── news_client.py      # GNews API (top headlines)
        └── obsidian_client.py  # Obsidian vault REST API
```

## Architecture

### Data Flow

```
CLI (cli.py)
  → Config.from_env()           # Load + validate env vars
  → Initialize clients          # WeatherClient, NewsClient, ObsidianClient
  → YourDayAgent.run()          # Orchestrate workflow
    → WeatherClient.fetch_weather()     # Geocode location, fetch current weather
    → NewsClient.fetch_top_news(10)     # Fetch top 10 headlines
    → Agent.invoke_async(prompt)        # Generate summary via Bedrock
    → ObsidianClient.put_content()      # POST markdown to Obsidian vault
  → Return file path: YourDayStart/Daily Summary-YYYY-MM-DD.md
```

### Key Components

- **cli.py** - Entry point registered as `yourday` command. Parses `run` subcommand, orchestrates initialization, handles errors.
- **config.py** - `Config` dataclass loaded via `Config.from_env()`. Validates required env vars, raises `ConfigurationError` if missing.
- **agent/yourday_agent.py** - `YourDayAgent` class using Strands SDK `Agent`. Sync `run()` wraps async `_run_async()` via `asyncio.run()`.
- **clients/weather_client.py** - `WeatherClient` uses Open-Meteo (no API key). Geocodes location on init, maps WMO weather codes to readable conditions.
- **clients/news_client.py** - `NewsClient` wraps GNews API. Normalizes article responses into `{title, description, url, source, published_at}` dicts.
- **clients/obsidian_client.py** - `ObsidianClient` uses Bearer token auth. `put_content()` sends markdown via PUT to `/vault/{path}`.

### Exception Hierarchy

```
YourDayError (base)
├── WeatherAPIError
├── NewsAPIError
├── AgentExecutionError
├── ObsidianMCPError
├── ObsidianAPIError
└── ConfigurationError
```

All client errors inherit from `YourDayError`. The CLI catches `YourDayError` for clean error messages and generic `Exception` as a fallback.

## Environment Configuration

Required (loaded from `.env` via `python-dotenv`):

| Variable | Description |
|---|---|
| `LOCATION` | City name for weather (e.g., `Seattle`) |
| `NEWS_API_KEY` | GNews API key |
| `BEDROCK_MODEL_ID` | AWS Bedrock model ID (e.g., `us.anthropic.claude-sonnet-4-5-20250929-v1:0`) |
| `OBSIDIAN_API_KEY` | Obsidian REST API bearer token |

Optional with defaults:

| Variable | Default | Description |
|---|---|---|
| `OBSIDIAN_BASE_URL` | `http://localhost:27123` | Obsidian REST API base URL |
| `AWS_REGION` | `us-east-1` | AWS region for Bedrock |
| `LOG_LEVEL` | `INFO` | Logging level |

AWS credentials must also be configured (`aws configure` or `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` env vars).

## Code Conventions

### Style

- **Formatter:** Black, line length 88, target Python 3.10
- **Type checking:** mypy with `disallow_untyped_defs = true` (all functions must have type annotations)
- **All functions** must have explicit return type annotations
- **Docstrings** on all classes and public methods with Args/Returns/Raises sections where applicable

### Patterns

- **Configuration:** `@dataclass` with `@classmethod` factory (`Config.from_env()`)
- **Clients:** Each external API gets its own client class in `yourday/clients/`. Clients raise domain-specific exceptions inheriting from `YourDayError`.
- **HTTP requests:** Use `requests` library with explicit `timeout=10` on all calls
- **Async:** Agent workflow uses `asyncio.run()` as sync wrapper around async internals
- **Type hints:** Modern Python syntax (`list[dict]`, `tuple[float, float]`, `dict[str, Any]`) — no `typing.List`/`typing.Dict`

### Adding a New Client

1. Create `yourday/clients/new_client.py` with a class following the existing pattern
2. Add a corresponding exception in `yourday/exceptions.py` inheriting from `YourDayError`
3. Wire it up in `cli.py` (initialization) and `yourday_agent.py` (usage in workflow)

## Dependencies

### Runtime

| Package | Purpose |
|---|---|
| `strands-agents` (>=1.13, <2) | AI agent framework for orchestrating tasks |
| `boto3` (>=1.26, <2) | AWS SDK for Bedrock model invocation |
| `requests` (>=2.31) | HTTP client for all external API calls |
| `python-dotenv` (>=1.0) | Load `.env` files into environment |

### Development

| Package | Purpose |
|---|---|
| `pytest` (>=7.4) | Test framework |
| `pytest-mock` (>=3.11) | Mocking support for tests |
| `black` (>=23.7) | Code formatter |
| `mypy` (>=1.5) | Static type checker |

## Build System

- **PEP 517/518** via `pyproject.toml` with `setuptools` backend
- **Entry point:** `yourday = "yourday.cli:main"` registers the `yourday` CLI command
- No CI/CD pipeline currently configured
