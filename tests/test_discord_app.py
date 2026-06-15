import asyncio

from modpack_bot.discord_app import (
    DiscordAdminResolver,
    _handle_token_toggle,
)


class FakeMember:
    """Discord member stand-in: a mention string and a bot flag."""

    def __init__(self, mention: str, bot: bool = False) -> None:
        self.mention = mention
        self.bot = bot


class FakeRole:
    """Discord role stand-in: matched by name, holds members."""

    def __init__(self, name: str, members: list[FakeMember]) -> None:
        self.name = name
        self.members = members


class FakeGuild:
    """Discord guild stand-in: just its roles."""

    def __init__(self, roles: list[FakeRole]) -> None:
        self.roles = roles


class FakeChannel:
    """Discord channel stand-in: points at its guild."""

    def __init__(self, guild: FakeGuild) -> None:
        self.guild = guild


class FakeClient:
    """Discord client stand-in: resolves one channel id to one channel."""

    def __init__(self, channel_id: int, channel: FakeChannel) -> None:
        self._channel_id = channel_id
        self._channel = channel

    def get_channel(self, channel_id: int) -> "FakeChannel | None":
        return self._channel if channel_id == self._channel_id else None


def _resolver_with(members: list[FakeMember]) -> DiscordAdminResolver:
    guild = FakeGuild([FakeRole("Admin", members)])
    resolver = DiscordAdminResolver("42", "Admin")
    resolver.bind(FakeClient(42, FakeChannel(guild)))
    return resolver


def test_mentions_excludes_bots():
    resolver = _resolver_with([FakeMember("<@1>"), FakeMember("<@bot>", bot=True), FakeMember("<@2>")])
    assert resolver.mentions() == ["<@1>", "<@2>"]


def test_mentions_empty_when_unbound():
    assert DiscordAdminResolver("42", "Admin").mentions() == []


def test_mentions_empty_when_role_missing():
    guild = FakeGuild([FakeRole("Mod", [FakeMember("<@1>")])])
    resolver = DiscordAdminResolver("42", "Admin")
    resolver.bind(FakeClient(42, FakeChannel(guild)))
    assert resolver.mentions() == []


class FakePermissions:
    """Discord permissions stand-in: only the administrator flag matters here."""

    def __init__(self, administrator: bool) -> None:
        self.administrator = administrator


class FakeAuthor:
    """Message author stand-in carrying guild permissions."""

    def __init__(self, administrator: bool) -> None:
        self.guild_permissions = FakePermissions(administrator)


class FakeMessage:
    """Discord message stand-in: records the text replied back."""

    def __init__(self, content: str, administrator: bool) -> None:
        self.content = content
        self.author = FakeAuthor(administrator)
        self.replies: list[str] = []

    async def reply(self, text: str) -> None:
        self.replies.append(text)


class FakeUsageResponder:
    """Responder stand-in: records the last set_show_usage value."""

    def __init__(self) -> None:
        self.show_usage: bool | None = None

    def set_show_usage(self, enabled: bool) -> None:
        self.show_usage = enabled


def test_token_command_enables_usage_for_admin():
    message = FakeMessage("!token true", administrator=True)
    responder = FakeUsageResponder()
    asyncio.run(_handle_token_toggle(message, responder))
    assert responder.show_usage is True
    assert message.replies and "✅" in message.replies[0]


def test_token_command_disables_usage_for_admin():
    message = FakeMessage("!token false", administrator=True)
    responder = FakeUsageResponder()
    asyncio.run(_handle_token_toggle(message, responder))
    assert responder.show_usage is False


def test_token_command_rejected_for_non_admin():
    message = FakeMessage("!token true", administrator=False)
    responder = FakeUsageResponder()
    asyncio.run(_handle_token_toggle(message, responder))
    # the flag is never touched and the player is told off.
    assert responder.show_usage is None
    assert message.replies == ["Você não tem permissão!"]
