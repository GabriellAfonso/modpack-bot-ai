"""Environment-backed settings for the bot runtime."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """All external configuration the bot needs to run.

    Example:
        >>> settings = load_settings()
        >>> settings.guide_dir
        'guide'
    """

    discord_token: str
    groq_api_key: str
    channel_id: str
    guide_dir: str = "guide"


def _require(name: str) -> str:
    """Read an env var, raising a clear error that names the missing one."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"missing required env var {name!r} (expected a non-empty string)")
    return value


def load_settings() -> Settings:
    """Build Settings from the process environment (.env already loaded)."""
    return Settings(
        discord_token=_require("DISCORD_TOKEN"),
        groq_api_key=_require("GROQ_API_KEY"),
        channel_id=_require("CANAL_ID"),
    )
