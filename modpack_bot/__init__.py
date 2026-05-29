"""Runtime package for the Minecraft-server Discord assistant.

Splits the former flat bot.py into single-responsibility modules: config,
text utils, Pokémon detection, the LLM client, filesystem repositories,
routing, prompt building, the orchestrating Responder and the Discord wiring.
All I/O (Discord, Groq, filesystem) lives at the edges behind injected
dependencies so the core logic stays pure and testable.
"""
