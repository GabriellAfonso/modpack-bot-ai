"""Offline generator for the compact per-Pokémon cards the bot reads at runtime.

Runs OFFLINE, once (and again only when the data changes: addon, new mons, or
an edit to biome_map.md). The bot never calls this — at runtime it only reads
the ready-made card at species_cards/<name>.md.

The former build_cards.py drove everything through module-level globals (FULL,
BIOMES, SPAWN_INDEX, ...). Here those become an explicit BuildContext passed
into pure renderers, so each piece is unit-testable with hand-built fixtures.

Reads:  content/pokemons-db/species/*.json
        content/pokemons-db/spawn_pool_world/*.json
        content/pokemons-db/biome_map.md
Writes: content/pokemons-db/species_cards/<name>.md (+ species_cards_full/)
"""
