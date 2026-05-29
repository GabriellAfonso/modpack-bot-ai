"""Entrypoint: load config, wire dependencies, run the bot."""

from dotenv import load_dotenv

from modpack_bot.config import Settings, load_settings
from modpack_bot.discord_app import build_client
from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.llm import GroqCompleter
from modpack_bot.responder import Responder
from modpack_bot.router import Router


def build_responder(settings: Settings) -> Responder:
    """Compose the runtime dependency graph from settings."""
    completer = GroqCompleter(settings.groq_api_key)
    guides = GuideRepository(settings.guide_dir)
    cards = CardRepository(settings.guide_dir)
    router = Router(completer, guides)
    return Responder(router, completer, guides, cards)


def main() -> None:
    load_dotenv()
    settings = load_settings()
    client = build_client(settings.channel_id, build_responder(settings))
    client.run(settings.discord_token)


if __name__ == "__main__":
    main()
