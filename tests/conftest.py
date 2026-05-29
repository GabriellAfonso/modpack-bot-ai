"""Shared named fakes for the bot-runtime tests (no inline stubs)."""

from modpack_bot.llm import Message, ROUTER_MODELS, TokenUsage, ToolDispatch, ToolSpec

# Fixed per-call cost so usage-footer assertions are deterministic.
_USAGE_PER_CALL = TokenUsage(10, 5)


class FakeCompleter:
    """ModelCompleter that returns canned text and records every call.

    Distinguishes the router stage from the answer stage by the model list,
    so one fake drives a whole Responder pipeline. `tool_call`, when set to a
    (name, arguments) pair, makes complete_with_tools run the dispatch once so a
    test can assert what the real tool would return.
    """

    def __init__(
        self,
        route_reply: str = "market.md|pt",
        answer_reply: str = "ANSWER",
        tool_call: "tuple[str, dict[str, object]] | None" = None,
    ) -> None:
        self.route_reply = route_reply
        self.answer_reply = answer_reply
        self.tool_call = tool_call
        self.tool_result: str | None = None
        self.calls: list[tuple[list[Message], list[str]]] = []
        self._usage = TokenUsage()

    @property
    def usage(self) -> TokenUsage:
        return self._usage

    def reset_usage(self) -> None:
        self._usage = TokenUsage()

    def complete(self, messages: list[Message], models: list[str], **kwargs: object) -> str:
        self.calls.append((messages, models))
        self._usage += _USAGE_PER_CALL
        return self.route_reply if models == ROUTER_MODELS else self.answer_reply

    def complete_with_tools(
        self,
        messages: list[Message],
        models: list[str],
        *,
        tools: list[ToolSpec],
        dispatch: ToolDispatch,
        **kwargs: object,
    ) -> str:
        self.calls.append((messages, models))
        self._usage += _USAGE_PER_CALL
        if self.tool_call is not None:
            self.tool_result = dispatch(*self.tool_call)
        return self.answer_reply

    @property
    def last_system_prompt(self) -> str:
        """The system message of the most recent completion."""
        return self.calls[-1][0][0]["content"]


class FakeGuideRepository:
    """In-memory stand-in for GuideRepository."""

    def __init__(self, core: str = "CORE", guides: dict[str, str] | None = None) -> None:
        self._core = core
        self._guides = guides or {}

    def load_core(self) -> str:
        return self._core

    def load_guide(self, name: str) -> str:
        return self._guides[name]


class FakeCardRepository:
    """In-memory stand-in for CardRepository."""

    def __init__(self, cards: dict[str, str] | None = None) -> None:
        self._cards = cards or {}

    def pokemon_names(self) -> frozenset[str]:
        return frozenset(self._cards)

    def load_card(self, name: str, full: bool = False) -> str | None:
        return self._cards.get(name)


class FakeAdminResolver:
    """In-memory AdminResolver returning canned Discord mentions."""

    def __init__(self, mentions: list[str] | None = None) -> None:
        self._mentions = mentions or []

    def mentions(self) -> list[str]:
        return self._mentions
