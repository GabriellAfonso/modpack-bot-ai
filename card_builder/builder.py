"""Load the source data into a BuildContext and write every card to disk."""

import glob
import json
import os
from dataclasses import dataclass

from card_builder.biomes import load_biomes
from card_builder.card import build_card
from card_builder.context import BuildContext, Json, RenderContext, RenderOptions
from card_builder.evolutions import index_pre_evolutions
from card_builder.spawns import index_spawns


@dataclass(frozen=True)
class Paths:
    """Filesystem layout under a pokemons-db base directory."""

    species_dir: str
    spawn_dir: str
    biome_map: str
    slim_out: str
    full_out: str


def paths_for(base_dir: str) -> Paths:
    """Resolve the standard pokemons-db layout under `base_dir`."""
    return Paths(
        species_dir=os.path.join(base_dir, "species"),
        spawn_dir=os.path.join(base_dir, "spawn_pool_world"),
        biome_map=os.path.join(base_dir, "biome_map.md"),
        slim_out=os.path.join(base_dir, "species_cards"),
        full_out=os.path.join(base_dir, "species_cards_full"),
    )


def _load_species(species_dir: str) -> list[tuple[str, Json]]:
    """[(card_key, species_json)] for every species file."""
    files = glob.glob(os.path.join(species_dir, "*.json"))
    return [(os.path.basename(f)[:-5], json.load(open(f, encoding="utf-8"))) for f in files]


def build_all(base_dir: str) -> None:
    """Generate the slim and full card sets from the source data in `base_dir`."""
    paths = paths_for(base_dir)
    biomes = load_biomes(paths.biome_map)
    spawn_index = index_spawns(paths.spawn_dir)
    species = _load_species(paths.species_dir)
    species_keys = {key for key, _ in species}

    # Pre-evolution text is computed once with SLIM options and reused by both
    # builds — preserving the original (PRE_EVOLUTIONS frozen at import) behavior.
    slim_render = RenderContext(biomes, RenderOptions(full=False))
    pre_evolutions = index_pre_evolutions(paths.species_dir, species_keys, slim_render)

    for options, dest in [(RenderOptions(full=False), paths.slim_out),
                          (RenderOptions(full=True), paths.full_out)]:
        ctx = BuildContext(RenderContext(biomes, options), spawn_index, pre_evolutions)
        _write_cards(species, dest, ctx)
    print(f"Biome tags loaded: {len(biomes)}")


def _write_cards(species: list[tuple[str, Json]], dest: str, ctx: BuildContext) -> None:
    """Render and write every card into `dest`."""
    os.makedirs(dest, exist_ok=True)
    for key, data in species:
        with open(os.path.join(dest, key + ".md"), "w", encoding="utf-8") as out:
            out.write(build_card(data, key, ctx))
    label = "full" if ctx.render.options.full else "slim"
    print(f"Generated {len(species)} {label} cards in {dest}")
