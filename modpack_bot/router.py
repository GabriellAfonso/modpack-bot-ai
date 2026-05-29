"""Classify an incoming message into (guide_file, language)."""

from modpack_bot.admins import TOOL_ADMINS
from modpack_bot.guides import VALID_GUIDES, GuideRepository
from modpack_bot.llm import ROUTER_MODELS, ModelCompleter

# A routed result: the guide file OR a tool label to answer from (None when
# nothing fits) + language.
Route = tuple[str | None, str]

# Tool labels the router may emit instead of a guide file (live data, not files).
VALID_TOOLS = frozenset({TOOL_ADMINS})

_LANGUAGES = ("pt", "en")
_DEFAULT_LANGUAGE = "pt"


def parse_route(raw: str) -> Route:
    """Parse the router model's "guide|lang" line into a validated Route.

    Unknown guides collapse to None; unknown languages default to pt.

    Example:
        >>> parse_route("wiki.md | en")
        ('wiki.md', 'en')
        >>> parse_route("nonsense")
        (None, 'pt')
    """
    guide_part, _, language_part = raw.strip().lower().partition("|")
    guide_file = guide_part.strip()
    language = language_part.strip()
    routable = guide_file in VALID_GUIDES or guide_file in VALID_TOOLS
    guide_file = guide_file if routable else None
    language = language if language in _LANGUAGES else _DEFAULT_LANGUAGE
    return guide_file, language


class Router:
    """Asks the cheap router model which guide fits and in what language."""

    def __init__(self, completer: ModelCompleter, guides: GuideRepository) -> None:
        self._completer = completer
        self._guides = guides

    def route(self, message: str) -> Route:
        raw = self._completer.complete(
            messages=[
                {"role": "system", "content": self._guides.load_core()},
                {"role": "user", "content": message},
            ],
            models=ROUTER_MODELS,
            max_tokens=15,
            temperature=0,
        )
        return parse_route(raw)
