"""Discord wiring: the thin edge that turns events into Responder calls."""

import discord

from modpack_bot.errors import error_reply
from modpack_bot.intent import detect_language
from modpack_bot.responder import Responder

_CLEAR_COMMAND = "!clear"
_FLAN_COMMAND = "!flan"
_TOKEN_ON_COMMAND = "!token true"
_TOKEN_OFF_COMMAND = "!token false"
_TOKEN_ON_REPLY = "Tokens visíveis a cada mensagem ✅"
_TOKEN_OFF_REPLY = "Tokens ocultos 🙈"
_NO_PERMISSION = "Você não tem permissão!"

_FLAN_CHEATSHEET = """**🏠 Flan — Proteção de Terreno**

**Criar claim**
Segure a **Enxada Dourada** → clique direito no 1º canto → clique no 2º canto
Ou: `/flan add rect <largura> <comprimento>` (cria em volta de você)

**Comandos essenciais**
`/flan menu` — abre o menu visual do claim
`/flan list` — lista todos os seus claims
`/flan claimBlocks` — mostra seus blocos disponíveis
`/flan expand <n>` — expande o claim na direção que você olha
`/flan name <nome>` — dá um nome ao claim onde você está
`/flan delete` — deleta o claim onde você está

**Adicionar amigo**
`/flan group players add Co-Owner <jogador>` — acesso total
`/flan group players add Visitor <jogador>` — acesso básico

**Inspecionar terreno**
Segure um **Graveto** e clique no chão para ver o dono do claim

**Blocos de claim**
Você começa com **5.000** e ganha +1 a cada 30 segundos (máx 10.000).
Cada bloco de área consome 1 bloco de claim (ex: 20×20 = 200).

Dúvidas? Só perguntar! 😄"""


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
        if message.content.strip() == _FLAN_COMMAND:
            await message.reply(_FLAN_CHEATSHEET)
            return
        if message.content.strip() in (_TOKEN_ON_COMMAND, _TOKEN_OFF_COMMAND):
            await _handle_token_toggle(message, responder)
            return
        await _reply_answer(message, responder)

    return client


async def _handle_clear(message: discord.Message) -> None:
    """Admin-only channel purge."""
    if message.author.guild_permissions.administrator:
        await message.channel.purge()
    else:
        await message.reply(_NO_PERMISSION)


async def _handle_token_toggle(message: discord.Message, responder: Responder) -> None:
    """Admin-only runtime switch for the per-message token footer (global flag)."""
    if not message.author.guild_permissions.administrator:
        await message.reply(_NO_PERMISSION)
        return
    enabled = message.content.strip() == _TOKEN_ON_COMMAND
    responder.set_show_usage(enabled)
    await message.reply(_TOKEN_ON_REPLY if enabled else _TOKEN_OFF_REPLY)


async def _reply_answer(message: discord.Message, responder: Responder) -> None:
    """Run the pipeline while showing the typing indicator; reply or error."""
    async with message.channel.typing():
        try:
            # Per-author session key: one player's history never leaks into another's.
            await message.reply(responder.answer(message.content, str(message.author.id)))
        except Exception as error:  # noqa: BLE001 — last-resort guard, logged below
            print(error)
            # Turn the failure into actionable copy (too long / rate-limited / down).
            await message.reply(error_reply(error, detect_language(message.content)))
