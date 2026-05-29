"""Evolution rendering: methods, requirements, and the reverse 'evolui de' index."""

import glob
import json
import os
import re
from typing import Callable

from card_builder.biomes import resolve_biome
from card_builder.context import Json, RenderContext
from card_builder.naming import TIME_PT, item_name, titleize
from card_builder.type_chart import TYPE_PT

# Variants whose label is a fixed phrase (detail intentionally elided).
_STATIC_REQUIREMENTS = {
    "weather": "com tempo específico",
    "use_move": "usando um golpe X vezes",
    "defeat": "derrotando Pokémon específicos",
    "blocks_traveled": "após andar uma distância",
    "stat_compare": "com relação específica de stats",
    "stat_equal": "com relação específica de stats",
    "party_member": "com certo Pokémon no time",
    "advancement": "após um avanço (advancement)",
}

_PROPERTY_TARGETS = {"gender=male": "sendo macho", "gender=female": "sendo fêmea"}


def render_requirement(requirement: Json, ctx: RenderContext) -> str | None:
    """One evolution requirement -> a short PT phrase (None if not informative)."""
    variant = requirement.get("variant")
    if variant in _STATIC_REQUIREMENTS:
        return _STATIC_REQUIREMENTS[variant]
    handler = _DYNAMIC_REQUIREMENTS.get(variant)
    if handler:
        return handler(requirement, ctx)
    return variant or ""


def _level(r: Json, _: RenderContext) -> str:
    return f"nível {r.get('minLevel', r.get('amount', '?'))}+"


def _friendship(r: Json, _: RenderContext) -> str:
    return f"amizade ≥{r.get('amount', '?')}"


def _time_range(r: Json, _: RenderContext) -> str:
    return TIME_PT.get(r.get("range"), r.get("range", ""))


def _biome(r: Json, ctx: RenderContext) -> str | None:
    cond = _biome_label(r.get("biomeCondition"), ctx)
    anti = _biome_label(r.get("biomeAnticondition"), ctx)
    if cond:
        return "em " + cond
    if anti and anti != "certos biomas":
        return "fora de " + anti
    return None  # anti on an internal biome: not very informative, omit


def _biome_label(tag: str | None, ctx: RenderContext) -> str | None:
    """Real biome tag (#mod:is_x) -> biomes; internal evolution tag -> generic."""
    if not tag:
        return None
    if tag in ctx.biomes or ("is_" in tag and "/" not in tag):
        return resolve_biome(tag, ctx)
    return "certos biomas"


def _held_item(r: Json, _: RenderContext) -> str:
    return "segurando " + item_name(r.get("itemCondition", ""))


def _structure(r: Json, _: RenderContext) -> str:
    raw = str(r.get("structureCondition", r.get("structure", ""))).split(":")[-1]
    return "perto de " + titleize(raw)


def _has_move(r: Json, _: RenderContext) -> str:
    return "conhecendo " + titleize(r.get("move", ""))


def _has_move_type(r: Json, _: RenderContext) -> str:
    return "com golpe do tipo " + TYPE_PT.get(r.get("type"), r.get("type", ""))


def _moon_phase(r: Json, _: RenderContext) -> str:
    return f"lua fase {r.get('moonPhase', '?')}"


def _properties(r: Json, _: RenderContext) -> str:
    target = r.get("target", "")
    return _PROPERTY_TARGETS.get(target, target)


def _property_range(r: Json, _: RenderContext) -> str:
    return f"{r.get('feature', '')} {r.get('range', '')}".strip()


_DYNAMIC_REQUIREMENTS: dict[str, Callable[[Json, RenderContext], str | None]] = {
    "level": _level,
    "friendship": _friendship,
    "time_range": _time_range,
    "biome": _biome,
    "held_item": _held_item,
    "structure": _structure,
    "has_move": _has_move,
    "has_move_type": _has_move_type,
    "moon_phase": _moon_phase,
    "properties": _properties,
    "property_range": _property_range,
}


def render_method(evolution: Json, ctx: RenderContext) -> str:
    """The evolution method, e.g. 'usar Water Stone' / 'subir de nível (…)'."""
    reqs = [r for r in (render_requirement(req, ctx) for req in evolution.get("requirements", [])) if r]
    base = _method_base(evolution)
    if reqs:
        base += " (" + ", ".join(reqs) + ")"
    return base


def _method_base(evolution: Json) -> str:
    variant = evolution.get("variant", "")
    if variant == "item_interact":
        return "usar " + item_name(evolution.get("requiredContext", "item"))
    if variant == "trade":
        return "trocar"
    return "subir de nível"  # level_up / level


def render_evolution(evolution: Json, ctx: RenderContext) -> str:
    """A forward '## Evolui em' line: '- Result — method'."""
    return f"- {titleize(evolution.get('result', '?'))} — {render_method(evolution, ctx)}"


def index_pre_evolutions(
    species_dir: str, species_files: set[str], ctx: RenderContext
) -> dict[str, list[tuple[str, str]]]:
    """Reverse index: target_name -> [(who_evolves_into_it, method)].

    Lets a target's card (e.g. Vaporeon) say 'Evolui de: Eevee — usar Water Stone'.
    """
    pre: dict[str, list[tuple[str, str]]] = {}
    for path in glob.glob(os.path.join(species_dir, "*.json")):
        species = json.load(open(path, encoding="utf-8"))
        source = species["name"]
        for evolution in species.get("evolutions", []):
            target = _evolution_target(evolution, species_files)
            pre.setdefault(target, []).append((source, render_method(evolution, ctx)))
    return pre


def _evolution_target(evolution: Json, species_files: set[str]) -> str:
    """Map an evolution result to a card key (alnum-normalized when it exists)."""
    raw = re.sub(r"[^a-z0-9]", "", evolution.get("result", "").lower())
    return raw if raw in species_files else evolution.get("result", "").split()[0].lower()
