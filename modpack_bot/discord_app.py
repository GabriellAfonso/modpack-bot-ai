"""Discord wiring: the thin edge that turns events into Responder calls."""

import discord

from modpack_bot.responder import Responder

_CLEAR_COMMAND = "!clear"
_NO_PERMISSION = "Você não tem permissão!"
_GENERIC_ERROR = "Ocorreu um erro, tenta de novo!"


class DiscordAdminResolver:
    """Resolve the admin role to member mentions in the bot's guild.

    Bound to the live client after it is built (the client is created after the
    Responder, so the reference is filled in via bind()). Implements the
    AdminResolver Protocol the Responder depends on. Reading `role.members`
    needs the Server Members privileged intent (enabled in build_client).
    """

    def __init__(self, channel_id: str, role_name: str) -> None:
        self._channel_id = channel_id
        self._role_name = role_name
        self._client: discord.Client | None = None

    def bind(self, client: discord.Client) -> None:
        """Attach the live client once it exists."""
        self._client = client

    def mentions(self) -> list[str]:
        role = self._admin_role()
        if role is None:
            return []
        # Skip bots (the bot itself carries the Admin role) — only humans.
        return [member.mention for member in role.members if not member.bot]

    def _admin_role(self) -> "discord.Role | None":
        if self._client is None:
            return None
        channel = self._client.get_channel(int(self._channel_id))
        guild = getattr(channel, "guild", None)
        if guild is None:
            return None
        return discord.utils.get(guild.roles, name=self._role_name)


def build_client(channel_id: str, responder: Responder) -> discord.Client:
    """Build the Discord client wired to answer in a single channel."""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True  # required to read role.members for the admins tool.
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        print(f"Bot online as {client.user}")

    @client.event
    async def on_message(message: discord.Message) -> None:
        if message.content == _CLEAR_COMMAND:
            await _handle_clear(message)
            return
        if message.author.bot or str(message.channel.id) != channel_id:
            return
        await _reply_answer(message, responder)

    return client


async def _handle_clear(message: discord.Message) -> None:
    """Admin-only channel purge."""
    if message.author.guild_permissions.administrator:
        await message.channel.purge()
    else:
        await message.reply(_NO_PERMISSION)


async def _reply_answer(message: discord.Message, responder: Responder) -> None:
    """Run the pipeline while showing the typing indicator; reply or error."""
    async with message.channel.typing():
        try:
            await message.reply(responder.answer(message.content))
        except Exception as error:  # noqa: BLE001 — last-resort guard, logged below
            print(error)
            await message.reply(_GENERIC_ERROR)
