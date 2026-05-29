"""LLM client behind a narrow protocol so callers can be tested with fakes.

`GroqCompleter` is the only place that imports `groq`. Everything else depends
on the `ModelCompleter` protocol, so tests inject a fake returning canned text.
"""

from typing import Protocol

from groq import Groq, RateLimitError

# A single chat message, e.g. {"role": "system", "content": "..."}.
Message = dict[str, str]

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


class ModelCompleter(Protocol):
    """Completes a chat across a model fallback list, returning the text."""

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


class GroqCompleter:
    """ModelCompleter backed by the Groq API."""

    def __init__(self, api_key: str) -> None:
        self._groq = Groq(api_key=api_key)

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
                return response.choices[0].message.content
            except RateLimitError as error:
                last_error = error
                continue
        raise last_error if last_error else RuntimeError(f"no models given: {models!r}")
