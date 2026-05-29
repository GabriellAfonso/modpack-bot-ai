"""Offline generator for the compact per-Pokémon cards the bot reads at runtime.

Runs OFFLINE, once (and again only when the data changes: addon, new mons, or
an edit to biome_map.md). The bot never calls this — at runtime it only reads
the ready-made card at species_cards/<name>.md.

The former build_cards.py drove everything through module-level globals (FULL,
BIOMES, SPAWN_INDEX, ...). Here those become an explicit BuildContext passed
into pure renderers, so each piece is unit-testable with hand-built fixtures.

Reads:  guide/pokemons-db/species/*.json
        guide/pokemons-db/spawn_pool_world/*.json
        guide/pokemons-db/biome_map.md
Writes: guide/pokemons-db/species_cards/<name>.md (+ species_cards_full/)
"""
