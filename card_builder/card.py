"""Assemble one Pokémon card from its species JSON + a BuildContext.

build_card is pure: given the species data and a context (biome map, spawn
index, pre-evolution index, options) it returns the exact markdown string the
bot reads at runtime. Each section is its own small function.
"""

from card_builder.context import BuildContext, Json
from card_builder.evolutions import render_evolution
from card_builder.naming import item_name, titleize
from card_builder.spawns import spawn_block
from card_builder.type_chart import TYPE_PT, weaknesses

_EV_LABEL = {"hp": "HP", "attack": "Atk", "defence": "Def",
             "special_attack": "SpA", "special_defence": "SpD", "speed": "Spd"}

# Detection substring shared with the runtime (modpack_bot.responder): a card
# carrying this line has no natural spawn, so the responder augments the answer
# with RAG to surface a mod-based acquisition method (e.g. Legendary Monuments
# pedestals). The old line also asserted "obtido por evolução/troca/ovo", which
# is false for summon-only legendaries (zekrom et al.) — dropped so the model
# can't parrot it.
NO_NATURAL_SPAWN = "Não nasce naturalmente"
_NO_NATURAL_SPAWN = f"- {NO_NATURAL_SPAWN} (sem spawn natural no mundo)."


def build_card(species: Json, key: str, ctx: BuildContext) -> str:
    """Render the full card markdown for one species."""
    types = _types(species)
    sections = [
        _header(species, types),
        _stats_line(species),
        _weakness_line(types),
        _abilities_line(species),
        _meta_line(species),
        _drops_line(species),
        _spawn_section(key, ctx),
        _evolutions_section(species, ctx),
        _pre_evolutions_section(key, ctx),
        _footer_line(species),
        f"\n_Mais detalhes (golpes, TMs, EVs completos): `/pwiki {key}`._",
    ]
    return "\n".join(s for s in sections if s is not None)


def _types(species: Json) -> list[str]:
    secondary = [species["secondaryType"]] if species.get("secondaryType") else []
    return [species["primaryType"]] + secondary


def _header(species: Json, types: list[str]) -> str:
    types_pt = "/".join(TYPE_PT.get(t, t) for t in types)
    return f"# {species['name']}  (#{species['nationalPokedexNumber']} · {types_pt})"


def _stats_line(species: Json) -> str:
    s = species["baseStats"]
    return (
        f"Stats base: HP {s['hp']} / Atk {s['attack']} / Def {s['defence']} / "
        f"SpA {s['special_attack']} / SpD {s['special_defence']} / Spd {s['speed']}"
    )


def _weakness_line(types: list[str]) -> str | None:
    weak_map = weaknesses(types)
    if not weak_map:
        return None
    x4 = [TYPE_PT.get(t, t) for t, m in weak_map.items() if m >= 4]
    x2 = [TYPE_PT.get(t, t) for t, m in weak_map.items() if m == 2]
    parts = []
    if x4:
        parts.append("4x " + ", ".join(x4))
    if x2:
        parts.append("2x " + ", ".join(x2))
    return "Fraco contra: " + " · ".join(parts)


def _abilities_line(species: Json) -> str | None:
    abilities = []
    for ability in species.get("abilities", []):
        if ability.startswith("h:"):
            abilities.append(titleize(ability[2:]) + " (oculta)")
        else:
            abilities.append(titleize(ability))
    return "Habilidades: " + ", ".join(abilities) if abilities else None


def _meta_line(species: Json) -> str:
    meta = [f"Catch rate: {species.get('catchRate', '?')}"]
    ev = ", ".join(f"{v} {_EV_LABEL.get(k, k)}" for k, v in species.get("evYield", {}).items() if v)
    if ev:
        meta.append(f"EV yield: {ev}")
    if species.get("eggGroups"):
        meta.append("Egg groups: " + ", ".join(titleize(g) for g in species["eggGroups"]))
    return " · ".join(meta)


def _drops_line(species: Json) -> str | None:
    drops = species.get("drops", {}).get("entries", [])
    if not drops:
        return None
    return "Drops: " + ", ".join(_drop(entry) for entry in drops)


def _drop(entry: Json) -> str:
    name = item_name(entry["item"])
    if "percentage" in entry:
        return f"{name} ({entry['percentage']}%)"
    if "quantityRange" in entry:
        return f"{name} (qtd {entry['quantityRange']})"
    return name


def _spawn_section(key: str, ctx: BuildContext) -> str:
    spawn_text = spawn_block(key, ctx.spawn_index, ctx.render)
    return "\n## Spawn\n" + (spawn_text if spawn_text else _NO_NATURAL_SPAWN)


def _evolutions_section(species: Json, ctx: BuildContext) -> str | None:
    evolutions = species.get("evolutions", [])
    if not evolutions:
        return None
    return "\n## Evolui em\n" + "\n".join(render_evolution(e, ctx.render) for e in evolutions)


def _pre_evolutions_section(key: str, ctx: BuildContext) -> str | None:
    pre_evos = ctx.pre_evolutions.get(key, [])
    if not pre_evos:
        return None
    return "\n## Evolui de\n" + "\n".join(f"- {src} — {method}" for src, method in pre_evos)


def _footer_line(species: Json) -> str | None:
    forms = [f.get("name") for f in species.get("forms", []) if f.get("name")]
    gmax = any("gmax" in f.get("aspects", []) for f in species.get("forms", []))
    footer = []
    if forms:
        footer.append("Formas: " + ", ".join(forms))
    if gmax:
        footer.append("Gigantamax: sim")
    return "\n" + " · ".join(footer) if footer else None
