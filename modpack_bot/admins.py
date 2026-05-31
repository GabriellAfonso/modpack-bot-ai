"""The 'who are the admins' tool: resolve the Discord admin role to mentions.

This is live data — staff changes over time and the mention IDs (`<@123>`) are
per-guild, non-human strings that cannot be written into faq.md. So it is
resolved at answer time. The resolver is an interface (Protocol) so the
Responder stays decoupled from discord.py and is testable with a named fake.
"""

from typing import Protocol

_NO_ADMINS = {
    "pt": "Não consegui pegar a lista de admins agora. Procura alguém com o cargo Admin no Discord!",
    "en": "I couldn't fetch the admin list right now. Look for someone with the Admin role on Discord!",
}


class AdminResolver(Protocol):
    """Returns the current admin-role members as Discord mention strings."""

    def mentions(self) -> list[str]:
        ...


def admins_message(mentions: list[str], language: str) -> str:
    """Player-facing reply listing the admins, or a fallback if none resolved.

    Returned verbatim (never through the answer LLM) so the `<@id>` mentions
    survive intact.

    Example:
        >>> admins_message(["<@1>"], "pt")
        'Você pode falar com a staff aqui: <@1>'
    """
    if not mentions:
        return _NO_ADMINS.get(language, _NO_ADMINS["pt"])
    listed = ", ".join(mentions)
    if language == "en":
        return f"You can reach the staff here: {listed}"
    return f"Você pode falar com a staff aqui: {listed}"
