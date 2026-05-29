"""Discord wiring: the thin edge that turns events into Responder calls."""

import discord

from modpack_bot.responder import Responder

_CLEAR_COMMAND = "!clear"
_NO_PERMISSION = "Você não tem permissão!"
_GENERIC_ERROR = "Ocorreu um erro, tenta de novo!"


def build_client(channel_id: str, responder: Responder) -> discord.Client:
    """Build the Discord client wired to answer in a single channel."""
    intents = discord.Intents.default()
    intents.message_content = True
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
