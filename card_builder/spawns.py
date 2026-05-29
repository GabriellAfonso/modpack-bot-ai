"""Spawn-pool indexing and the '## Spawn' card section."""

import glob
import json
import os

from card_builder.biomes import resolve_biomes
from card_builder.context import Json, RenderContext
from card_builder.naming import TIME_PT, item_name, titleize


def index_spawns(spawn_dir: str) -> dict[str, list[Json]]:
    """species_name -> list of spawn entries (grouped from all pool files)."""
    index: dict[str, list[Json]] = {}
    for path in glob.glob(os.path.join(spawn_dir, "*.json")):
        pool = json.load(open(path, encoding="utf-8"))
        if not pool.get("enabled", True):
            continue
        for spawn in pool.get("spawns", []):
            name = str(spawn.get("pokemon", "")).split()[0].lower()
            if name:
                index.setdefault(name, []).append(spawn)
    return index


def render_spawn(spawn: Json, ctx: RenderContext) -> str:
    """One spawn entry -> a '- [bucket] conditions — nível N' line."""
    condition = spawn.get("condition", {})
    parts = _condition_parts(condition, ctx)
    body = ", ".join(parts) if parts else "condições variadas"
    return f"- [{spawn.get('bucket', '?')}] {body} — nível {spawn.get('level', '?')}"


def _condition_parts(condition: Json, ctx: RenderContext) -> list[str]:
    """Human-readable fragments for a spawn condition, in display order."""
    parts: list[str] = []
    if condition.get("biomes"):
        # only where it SPAWNS; anticondition biomes are noise for this question.
        parts.append(resolve_biomes(condition["biomes"], ctx))
    time_range = condition.get("timeRange")
    if time_range:
        parts.append(TIME_PT.get(time_range, time_range))
    if condition.get("canSeeSky") is False:
        parts.append("sem ver o céu")
    if condition.get("isRaining") is True:
        parts.append("chovendo")
    if condition.get("structures"):
        parts.append("perto de " + ", ".join(titleize(x.split(":")[-1]) for x in condition["structures"]))
    if condition.get("neededNearbyBlocks"):
        parts.append("perto de " + ", ".join(item_name(x) for x in condition["neededNearbyBlocks"]))
    if condition.get("moonPhase") is not None:
        parts.append(f"lua fase {condition['moonPhase']}")
    return parts


def spawn_block(name: str, spawn_index: dict[str, list[Json]], ctx: RenderContext) -> str | None:
    """The full '## Spawn' body for one Pokémon, deduped and truncated."""
    spawns = spawn_index.get(name, [])
    if not spawns:
        return None
    lines = _dedupe([render_spawn(spawn, ctx) for spawn in spawns])
    limit = ctx.options.max_spawn_lines
    if not ctx.options.full and len(lines) > limit:
        extra = f"\n- … (+{len(lines) - limit} condições; veja `/pwiki {name}` → Biome Spawns)"
        return "\n".join(lines[:limit]) + extra
    return "\n".join(lines)


def _dedupe(lines: list[str]) -> list[str]:
    """Drop duplicate lines, preserving first-seen order."""
    seen: set[str] = set()
    unique: list[str] = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique.append(line)
    return unique
