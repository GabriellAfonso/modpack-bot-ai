import pytest

from modpack_bot.conversation import ConversationStore, Turn


class FakeClock:
    """A movable clock so TTL behaviour is tested without real time."""

    def __init__(self, now: float = 0.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now


def test_history_empty_for_unknown_key():
    store = ConversationStore(clock=FakeClock())
    assert store.history("nobody") == []


def test_records_and_returns_turns_oldest_first():
    store = ConversationStore(clock=FakeClock())
    store.record("u1", Turn("q1", "a1"))
    store.record("u1", Turn("q2", "a2"))
    assert store.history("u1") == [Turn("q1", "a1"), Turn("q2", "a2")]


def test_window_evicts_oldest_beyond_max_turns():
    store = ConversationStore(max_turns=2, clock=FakeClock())
    store.record("u1", Turn("q1", "a1"))
    store.record("u1", Turn("q2", "a2"))
    store.record("u1", Turn("q3", "a3"))
    assert store.history("u1") == [Turn("q2", "a2"), Turn("q3", "a3")]


def test_keys_are_isolated():
    store = ConversationStore(clock=FakeClock())
    store.record("u1", Turn("q1", "a1"))
    store.record("u2", Turn("q2", "a2"))
    assert store.history("u1") == [Turn("q1", "a1")]
    assert store.history("u2") == [Turn("q2", "a2")]


def test_session_expires_after_idle_ttl():
    clock = FakeClock()
    store = ConversationStore(ttl_seconds=60, clock=clock)
    store.record("u1", Turn("q1", "a1"))
    clock.now = 61  # past the idle window
    assert store.history("u1") == []


def test_activity_refreshes_the_idle_ttl():
    clock = FakeClock()
    store = ConversationStore(ttl_seconds=60, clock=clock)
    store.record("u1", Turn("q1", "a1"))
    clock.now = 50
    store.record("u1", Turn("q2", "a2"))  # resets last_seen to t=50
    clock.now = 100  # only 50s since the last touch -> still alive
    assert store.history("u1") == [Turn("q1", "a1"), Turn("q2", "a2")]


def test_rejects_non_positive_max_turns():
    with pytest.raises(ValueError, match="max_turns must be >= 1, got 0"):
        ConversationStore(max_turns=0)


def test_rejects_non_positive_ttl():
    with pytest.raises(ValueError, match="ttl_seconds must be > 0, got 0"):
        ConversationStore(ttl_seconds=0)
