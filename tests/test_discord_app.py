from modpack_bot.discord_app import DiscordAdminResolver


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
