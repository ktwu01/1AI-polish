# AI Footprint Configuration

To configure AI Footprint settings in this repository, you should primarily use the `app/core/config.py` file and environment variables.

## 1. Define Configuration Parameters in `app/core/config.py`

You would add new settings related to AI Footprint detection within the `Settings` class in `app/core/config.py`. For example:

```python
# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ... existing settings ...

    AI_FOOTPRINT_ENABLED: bool = False
    AI_FOOTPRINT_KEYWORDS: list[str] = ["LLM_GENERATED", "AI_ASSISTED"]
    AI_FOOTPRINT_SCAN_DEPTH: int = 3 # Example: how many subdirectories to scan

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

```

## 2. Configure via Environment Variables

The `Settings` class in `app/core/config.py` is designed to load values from environment variables (and `.env` files). This is the recommended way to manage sensitive or deployment-specific configurations.

You can set these environment variables directly in your deployment environment or by creating a `.env` file in the project root (e.g., `.env_example` is provided as a template).

Example `.env` entry:

```
# .env
AI_FOOTPRINT_ENABLED=True
AI_FOOTPRINT_KEYWORDS=["AI_GENERATED", "GPT_OUTPUT"]
AI_FOOTPRINT_SCAN_DEPTH=5
```

## 3. Accessing Configuration in Your Code

You can access these configuration settings throughout your application by importing the `settings` object:

```python
# Example: In app/services/llm_footprint_finder.py or app/api/v1/endpoints.py

from app.core.config import settings

if settings.AI_FOOTPRINT_ENABLED:
    print(f"AI Footprint scanning is enabled. Keywords: {settings.AI_FOOTPRINT_KEYWORDS}")
    # Use settings.AI_FOOTPRINT_SCAN_DEPTH in your logic
```

This approach ensures that your AI Footprint configuration is centralized, easily modifiable, and follows the project's existing configuration patterns.