"""Biome tag resolution: read biome_map.md, turn tags into short labels."""

import os
import re

from card_builder.context import RenderContext

# Special label kept identical on both the load and resolve sides.
ANY_SURFACE_BIOME = "qualquer bioma da superfície"


def load_biomes(biome_map_path: str) -> dict[str, str]:
    """Tag (#mod:is_x) -> short vanilla biome string (or a special label)."""
    mapping: dict[str, str] = {}
    if not os.path.exists(biome_map_path):
        return mapping
    current_tag: str | None = None
    with open(biome_map_path, encoding="utf-8") as file:
        for line in file:
            current_tag = _read_biome_line(line, current_tag, mapping)
    return mapping


def _read_biome_line(line: str, current_tag: str | None, mapping: dict[str, str]) -> str | None:
    """Fold one biome_map.md line into `mapping`; return the active tag."""
    header = re.match(r"^## (#\S+)", line)
    if header:
        return header.group(1)
    if current_tag is None:
        return None
    if "TODOS os biomas" in line:
        mapping[current_tag] = ANY_SURFACE_BIOME
    vanilla = re.match(r"^- \*\*Vanilla:\*\* (.+)", line)
    if vanilla and current_tag not in mapping:
        mapping[current_tag] = vanilla.group(1).strip()
    return current_tag


def resolve_biome(tag: str, ctx: RenderContext) -> str:
    """One tag -> a short label, truncated to options.max_biomes unless full."""
    if tag not in ctx.biomes:
        # unmapped external-mod tag -> clean name
        return tag.split(":")[-1].replace("is_", "").replace("_", " ")
    value = ctx.biomes[tag]
    if value == ANY_SURFACE_BIOME:
        return value
    parts = [p.strip() for p in value.split(",")]
    if ctx.options.full or len(parts) <= ctx.options.max_biomes:
        return ", ".join(parts)
    return ", ".join(parts[: ctx.options.max_biomes]) + "…"


def resolve_biomes(tags: list[str], ctx: RenderContext) -> str:
    """Join several tags into one '; '-separated label string."""
    return "; ".join(resolve_biome(t, ctx) for t in tags)
