"""Entrypoint: load config, wire dependencies, run the bot."""

from dotenv import load_dotenv

from modpack_bot.config import Settings, load_settings
from modpack_bot.discord_app import DiscordAdminResolver, build_client
from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.llm import GroqCompleter
from modpack_bot.responder import Responder
from modpack_bot.router import Router


def build_responder(settings: Settings, admins: DiscordAdminResolver) -> Responder:
    """Compose the runtime dependency graph from settings."""
    completer = GroqCompleter(settings.groq_api_key)
    guides = GuideRepository(settings.content_dir)
    cards = CardRepository(settings.content_dir)
    router = Router(completer, guides)
    return Responder(router, completer, guides, cards, admins)


def main() -> None:
    load_dotenv()
    settings = load_settings()
    admins = DiscordAdminResolver(settings.channel_id, settings.admin_role)
    client = build_client(settings.channel_id, build_responder(settings, admins))
    admins.bind(client)  # client exists only now; fill the resolver's reference.
    client.run(settings.discord_token)


if __name__ == "__main__":
    main()
