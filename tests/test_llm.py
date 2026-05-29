"""GroqCompleter behaviour, driven by a named fake Groq client (no network)."""

from modpack_bot.llm import GroqCompleter, TokenUsage


class _Usage:
    def __init__(self, prompt: int, completion: int) -> None:
        self.prompt_tokens = prompt
        self.completion_tokens = completion


class _Function:
    def __init__(self, name: str, arguments: str) -> None:
        self.name = name
        self.arguments = arguments


class _ToolCall:
    def __init__(self, call_id: str, name: str, arguments: str) -> None:
        self.id = call_id
        self.function = _Function(name, arguments)


class _ReplyMessage:
    def __init__(self, content: str, tool_calls: "list[_ToolCall] | None" = None) -> None:
        self.content = content
        self.tool_calls = tool_calls


class _Choice:
    def __init__(self, message: _ReplyMessage) -> None:
        self.message = message


class _Response:
    def __init__(self, message: _ReplyMessage, usage: _Usage) -> None:
        self.choices = [_Choice(message)]
        self.usage = usage


class _FakeCompletions:
    """Hands back scripted responses in order and records each create() call."""

    def __init__(self, responses: list[_Response]) -> None:
        self._responses = list(responses)
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> _Response:
        self.calls.append(kwargs)
        return self._responses.pop(0)


class FakeGroqClient:
    """Stand-in for groq.Groq exposing the .chat.completions.create surface."""

    def __init__(self, responses: list[_Response]) -> None:
        self.completions = _FakeCompletions(responses)
        self.chat = type("Chat", (), {"completions": self.completions})()


def test_token_usage_total_and_sum():
    assert TokenUsage(10, 5).total == 15
    assert TokenUsage(1, 2) + TokenUsage(3, 4) == TokenUsage(4, 6)


def test_complete_returns_content_and_tracks_usage():
    client = FakeGroqClient([_Response(_ReplyMessage("oi"), _Usage(7, 3))])
    completer = GroqCompleter("key", client=client)
    text = completer.complete([{"role": "user", "content": "x"}], ["m"], max_tokens=10, temperature=0)
    assert text == "oi"
    assert completer.usage.total == 10


def test_reset_usage_clears_counter():
    client = FakeGroqClient([_Response(_ReplyMessage("a"), _Usage(1, 1))])
    completer = GroqCompleter("key", client=client)
    completer.complete([{"role": "user", "content": "x"}], ["m"], max_tokens=1, temperature=0)
    completer.reset_usage()
    assert completer.usage.total == 0


def test_complete_with_tools_runs_tool_then_returns_text():
    first = _Response(
        _ReplyMessage("", [_ToolCall("c1", "filtrar_pokemon", '{"types": ["electric"]}')]),
        _Usage(10, 2),
    )
    final = _Response(_ReplyMessage("é o Zapdos"), _Usage(5, 4))
    client = FakeGroqClient([first, final])
    completer = GroqCompleter("key", client=client)
    captured: list[tuple[str, dict[str, object]]] = []

    def dispatch(name: str, arguments: dict[str, object]) -> str:
        captured.append((name, arguments))
        return "1 Pokémon: Zapdos"

    out = completer.complete_with_tools(
        [{"role": "system", "content": "s"}],
        ["m"],
        tools=[{"type": "function"}],
        dispatch=dispatch,
        max_tokens=10,
        temperature=0,
    )
    assert out == "é o Zapdos"
    assert captured == [("filtrar_pokemon", {"types": ["electric"]})]
    assert completer.usage.total == 21  # 12 + 9 across both calls
    # the tool's result was fed back into the second request's conversation.
    second_messages = client.completions.calls[1]["messages"]
    assert any(
        message.get("role") == "tool" and message["content"] == "1 Pokémon: Zapdos"
        for message in second_messages
    )
