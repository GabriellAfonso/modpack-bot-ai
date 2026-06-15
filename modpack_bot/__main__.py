"""Entrypoint: load config, wire dependencies, run the bot."""

import os

from dotenv import load_dotenv

from index_builder.build import build_index
from modpack_bot.config import Settings, load_settings
from modpack_bot.conversation import ConversationStore
from modpack_bot.discord_app import DiscordAdminResolver, build_client
from modpack_bot.guides import CardRepository, GuideRepository
from modpack_bot.llm import GroqCompleter
from modpack_bot.responder import Responder
from modpack_bot.retrieval import LlamaIndexRetriever


def build_responder(settings: Settings, admins: DiscordAdminResolver) -> Responder:
    """Compose the runtime dependency graph from settings."""
    completer = GroqCompleter(settings.groq_api_key)
    guides = GuideRepository(settings.content_dir)
    cards = CardRepository(settings.content_dir)
    retriever = _load_retriever(settings)
    conversations = ConversationStore(settings.history_turns, settings.history_ttl_seconds)
    return Responder(
        retriever, completer, guides, cards, admins, settings.show_token_usage, conversations
    )


def _load_retriever(settings: Settings) -> LlamaIndexRetriever:
    """Load the persisted RAG index, building it once if it is absent.

    The index is not committed (plan.md §13.3); on a fresh deploy the .md files
    and the embedding model are enough to regenerate it, so we do that lazily on
    first startup instead of failing.
    """
    if not os.path.isdir(settings.index_dir):
        build_index(settings.content_dir, settings.index_dir)
    return LlamaIndexRetriever(settings.index_dir, settings.embed_model, settings.top_k)


def main() -> None:
    load_dotenv()
    settings = load_settings()
    admins = DiscordAdminResolver(settings.channel_id, settings.admin_role)
    client = build_client(settings.channel_id, build_responder(settings, admins))
    admins.bind(client)  # client exists only now; fill the resolver's reference.
    client.run(settings.discord_token)


if __name__ == "__main__":
    main()
