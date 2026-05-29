"""LLM client behind a narrow protocol so callers can be tested with fakes.

`GroqCompleter` is the only place that imports `groq`. Everything else depends
on the `ModelCompleter` protocol, so tests inject a fake returning canned text.
"""

import json
from dataclasses import dataclass
from typing import Callable, Protocol

from groq import Groq, RateLimitError

# A single chat message, e.g. {"role": "system", "content": "..."}.
Message = dict[str, str]

# A Groq/OpenAI tool definition and the callable that runs a requested tool.
ToolSpec = dict[str, object]
ToolDispatch = Callable[[str, dict[str, object]], str]

# Cap on assistant<->tool round-trips before forcing a plain answer, so a model
# that keeps re-requesting tools can never spin forever.
_MAX_TOOL_ROUNDS = 4

# Models per stage, in priority order (falls through to the next on rate limit).
# Router = trivial classification, a cheap model is enough.
# Answer = quality matters (must not degenerate/hallucinate): 70b primary, scout
# (500K/day quota) takes the overflow, 8b is the last resort. All pure instruct
# (no reasoning models, which could leak <think> tokens into the answer).
ROUTER_MODELS = [
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]
ANSWER_MODELS = [
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.1-8b-instant",
]


@dataclass(frozen=True)
class TokenUsage:
    """Prompt/completion token counts, summable across calls.

    Example:
        >>> (TokenUsage(10, 5) + TokenUsage(2, 3)).total
        20
    """

    prompt: int = 0
    completion: int = 0

    @property
    def total(self) -> int:
        return self.prompt + self.completion

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(self.prompt + other.prompt, self.completion + other.completion)


class ModelCompleter(Protocol):
    """Completes a chat across a model fallback list, returning the text."""

    @property
    def usage(self) -> TokenUsage: ...

    def reset_usage(self) -> None: ...

    def complete(
        self,
        messages: list[Message],
        models: list[str],
        *,
        max_tokens: int,
        temperature: float,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ) -> str: ...

    def complete_with_tools(
        self,
        messages: list[Message],
        models: list[str],
        *,
        tools: list[ToolSpec],
        dispatch: ToolDispatch,
        max_tokens: int,
        temperature: float,
    ) -> str: ...


class GroqCompleter:
    """ModelCompleter backed by the Groq API.

    Accumulates token usage across every call since the last reset_usage(), so a
    caller can report the cost of one whole pipeline (router + answer + tools).
    """

    def __init__(self, api_key: str, client: "Groq | None" = None) -> None:
        self._groq = client or Groq(api_key=api_key)
        self._usage = TokenUsage()

    @property
    def usage(self) -> TokenUsage:
        return self._usage

    def reset_usage(self) -> None:
        self._usage = TokenUsage()

    def complete(
        self,
        messages: list[Message],
        models: list[str],
        *,
        max_tokens: int,
        temperature: float,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ) -> str:
        """Try the models in order; on a rate limit, fall through to the next."""
        last_error: RateLimitError | None = None
        for model in models:
            try:
                response = self._groq.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                )
                self._usage += _usage_of(response)
                return response.choices[0].message.content
            except RateLimitError as error:
                last_error = error
        raise last_error if last_error else RuntimeError(f"no models given: {models!r}")

    def complete_with_tools(
        self,
        messages: list[Message],
        models: list[str],
        *,
        tools: list[ToolSpec],
        dispatch: ToolDispatch,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Like complete, but the model may call `tools`; the loop runs them and
        feeds results back until it returns text. Rate limit restarts on the next
        model (a tool conversation can't migrate mid-flight)."""
        last_error: RateLimitError | None = None
        for model in models:
            try:
                return self._run_tool_loop(model, messages, tools, dispatch, max_tokens, temperature)
            except RateLimitError as error:
                last_error = error
        raise last_error if last_error else RuntimeError(f"no models given: {models!r}")

    def _run_tool_loop(
        self,
        model: str,
        messages: list[Message],
        tools: list[ToolSpec],
        dispatch: ToolDispatch,
        max_tokens: int,
        temperature: float,
    ) -> str:
        conversation: list[dict[str, object]] = list(messages)
        for _ in range(_MAX_TOOL_ROUNDS):
            reply = self._chat(model, conversation, max_tokens, temperature, tools)
            if not reply.tool_calls:
                return reply.content
            _record_tool_round(conversation, reply, dispatch)
        # Out of rounds: force a plain answer so we never return without text.
        return self._chat(model, conversation, max_tokens, temperature, tools=None).content

    def _chat(
        self,
        model: str,
        messages: list[dict[str, object]],
        max_tokens: int,
        temperature: float,
        tools: "list[ToolSpec] | None",
    ) -> object:
        """One Groq call (optionally tool-enabled); tracks usage, returns the message."""
        extra: dict[str, object] = {"tools": tools, "tool_choice": "auto"} if tools else {}
        response = self._groq.chat.completions.create(
            model=model, messages=messages, max_tokens=max_tokens, temperature=temperature, **extra
        )
        self._usage += _usage_of(response)
        return response.choices[0].message


def _usage_of(response: object) -> TokenUsage:
    """Read prompt/completion token counts off a Groq response."""
    usage = response.usage
    return TokenUsage(usage.prompt_tokens, usage.completion_tokens)


def _record_tool_round(
    conversation: list[dict[str, object]], reply: object, dispatch: ToolDispatch
) -> None:
    """Append the assistant's tool request and each tool's result to the chat."""
    conversation.append(
        {
            "role": "assistant",
            "content": reply.content or "",
            "tool_calls": [_echo_tool_call(call) for call in reply.tool_calls],
        }
    )
    for call in reply.tool_calls:
        arguments = json.loads(call.function.arguments or "{}")
        result = dispatch(call.function.name, arguments)
        conversation.append({"role": "tool", "tool_call_id": call.id, "content": result})


def _echo_tool_call(call: object) -> dict[str, object]:
    """Re-encode a returned tool call into the request shape Groq expects back."""
    return {
        "id": call.id,
        "type": "function",
        "function": {"name": call.function.name, "arguments": call.function.arguments},
    }
