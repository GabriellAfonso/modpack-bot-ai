"""Environment-backed settings for the bot runtime."""

import os
from dataclasses import dataclass

from modpack_bot.embedding import DEFAULT_EMBED_MODEL

_DEFAULT_INDEX_DIR = os.path.join("content", "index")
_DEFAULT_TOP_K = 4


@dataclass(frozen=True)
class Settings:
    """All external configuration the bot needs to run.

    Example:
        >>> settings = load_settings()
        >>> settings.content_dir
        'content'
    """

    discord_token: str
    groq_api_key: str
    channel_id: str
    content_dir: str = "content"
    admin_role: str = "Admin"  # Discord role whose members the admins tool lists.
    show_token_usage: bool = True  # append the per-message token cost footer.
    # RAG retrieval: where the persisted index lives, which local model embeds
    # the query, and how many passages to retrieve (plan.md §6/§7).
    index_dir: str = _DEFAULT_INDEX_DIR
    embed_model: str = DEFAULT_EMBED_MODEL
    top_k: int = _DEFAULT_TOP_K


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
        admin_role=os.getenv("ADMIN_ROLE", "Admin"),
        show_token_usage=os.getenv("SHOW_TOKEN_USAGE", "true").lower() == "true",
        index_dir=os.getenv("INDEX_DIR", _DEFAULT_INDEX_DIR),
        embed_model=os.getenv("EMBED_MODEL", DEFAULT_EMBED_MODEL),
        top_k=int(os.getenv("TOP_K", str(_DEFAULT_TOP_K))),
    )
