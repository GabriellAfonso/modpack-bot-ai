"""Dataclasses that replace the former module-level globals.

Passing these explicitly (instead of reading globals at import time) is what
makes the renderers in spawns/evolutions/card unit-testable with fixtures.
"""

from dataclasses import dataclass, field

# A parsed JSON object (a species file or a single spawn entry).
Json = dict[str, object]

DEFAULT_MAX_SPAWN_LINES = 6
DEFAULT_MAX_BIOMES = 5


@dataclass(frozen=True)
class RenderOptions:
    """Truncation knobs. full=True emits the untruncated 'full' card."""

    full: bool = False
    max_spawn_lines: int = DEFAULT_MAX_SPAWN_LINES
    max_biomes: int = DEFAULT_MAX_BIOMES


@dataclass(frozen=True)
class RenderContext:
    """What the biome/spawn/evolution renderers need: the biome map + options."""

    biomes: dict[str, str]
    options: RenderOptions = field(default_factory=RenderOptions)


@dataclass(frozen=True)
class BuildContext:
    """Everything build_card needs, assembled once by builder.load_context()."""

    render: RenderContext
    spawn_index: dict[str, list[Json]]
    pre_evolutions: dict[str, list[tuple[str, str]]]
