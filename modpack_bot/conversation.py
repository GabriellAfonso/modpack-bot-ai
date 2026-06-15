"""Per-user conversation memory: a sliding window of recent turns with idle TTL.

The bot is otherwise stateless; this is the only place a player's previous
messages survive between calls, so a follow-up ("e onde ele spawna?") can be
rewritten into a standalone question before it hits the gates and retrieval.
Kept tiny on purpose: a few turns per user, dropped after a short idle gap, so
one player's context can never leak into another's and old context can't pile up.
"""

import time
from collections import deque
from dataclasses import dataclass
from typing import Callable

_DEFAULT_MAX_TURNS = 3
_DEFAULT_TTL_SECONDS = 600.0  # 10 min idle -> the session is forgotten.


@dataclass(frozen=True)
class Turn:
    """One question/answer exchange kept for follow-up resolution."""

    question: str
    answer: str


@dataclass
class _Session:
    """A single key's recent turns plus the last time it was touched."""

    turns: "deque[Turn]"
    last_seen: float


class ConversationStore:
    """Per-key (per-user) recent turns, pruned by idle TTL on every access.

    Example:
        >>> store = ConversationStore(max_turns=2, ttl_seconds=60, clock=lambda: 0.0)
        >>> store.record("u1", Turn("oi", "ola"))
        >>> [turn.question for turn in store.history("u1")]
        ['oi']
    """

    def __init__(
        self,
        max_turns: int = _DEFAULT_MAX_TURNS,
        ttl_seconds: float = _DEFAULT_TTL_SECONDS,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if max_turns < 1:
            raise ValueError(f"max_turns must be >= 1, got {max_turns!r}")
        if ttl_seconds <= 0:
            raise ValueError(f"ttl_seconds must be > 0, got {ttl_seconds!r}")
        self._max_turns = max_turns
        self._ttl_seconds = ttl_seconds
        self._clock = clock
        self._sessions: dict[str, _Session] = {}

    def history(self, key: str) -> list[Turn]:
        """Recent turns for the key, oldest first; empty if expired or unknown."""
        session = self._live_session(key)
        return list(session.turns) if session else []

    def record(self, key: str, turn: Turn) -> None:
        """Append a turn, evicting the oldest beyond the window and refreshing TTL."""
        session = self._live_session(key)
        if session is None:
            session = _Session(deque(maxlen=self._max_turns), self._clock())
            self._sessions[key] = session
        session.turns.append(turn)
        session.last_seen = self._clock()

    def _live_session(self, key: str) -> "_Session | None":
        """The key's session if it exists and hasn't idled out; else drop and None."""
        session = self._sessions.get(key)
        if session is None:
            return None
        if self._clock() - session.last_seen > self._ttl_seconds:
            del self._sessions[key]
            return None
        return session
