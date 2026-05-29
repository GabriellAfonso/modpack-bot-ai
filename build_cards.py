"""Generate compact per-Pokémon 'cards' from the consolidated database.

Runs OFFLINE, once (and again only when the data changes: addon, new mons,
or an edit to biome_map.md). The bot never calls this — at runtime it only
reads the ready-made card at species_cards/<name>.md.

Reads:  guia/pokemons-db/species/*.json
        guia/pokemons-db/spawn_pool_world/*.json
        guia/pokemons-db/biome_map.md
Writes: guia/pokemons-db/species_cards/<name>.md
"""

import json
import glob
import os
import re

BASE = os.path.join("guia", "pokemons-db")
SPECIES_DIR = os.path.join(BASE, "species")
SPAWN_DIR = os.path.join(BASE, "spawn_pool_world")
BIOME_MAP = os.path.join(BASE, "biome_map.md")
OUT_DIR = os.path.join(BASE, "species_cards")        # slim version (default)
OUT_FULL_DIR = os.path.join(BASE, "species_cards_full")  # full version (on request)

MAX_SPAWN_LINES = 6
MAX_BIOMES = 5

# When True, neither biomes nor spawn lines are truncated (generates the full version).
FULL = False

# ---------------------------------------------------------------- types / PT

TYPE_PT = {
    "normal": "Normal", "fire": "Fogo", "water": "Água", "electric": "Elétrico",
    "grass": "Grama", "ice": "Gelo", "fighting": "Lutador", "poison": "Veneno",
    "ground": "Terra", "flying": "Voador", "psychic": "Psíquico", "bug": "Inseto",
    "rock": "Pedra", "ghost": "Fantasma", "dragon": "Dragão", "dark": "Sombrio",
    "steel": "Aço", "fairy": "Fada",
}

# Offensive effectiveness: attacker -> (super-effective 2x, not-very-effective 0.5x, no effect 0x)
_OFFENSIVE = {
    "normal": ([], ["rock", "steel"], ["ghost"]),
    "fire": (["grass", "ice", "bug", "steel"], ["fire", "water", "rock", "dragon"], []),
    "water": (["fire", "ground", "rock"], ["water", "grass", "dragon"], []),
    "electric": (["water", "flying"], ["electric", "grass", "dragon"], ["ground"]),
    "grass": (["water", "ground", "rock"], ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"], []),
    "ice": (["grass", "ground", "flying", "dragon"], ["fire", "water", "ice", "steel"], []),
    "fighting": (["normal", "ice", "rock", "dark", "steel"], ["poison", "flying", "psychic", "bug", "fairy"], ["ghost"]),
    "poison": (["grass", "fairy"], ["poison", "ground", "rock", "ghost"], ["steel"]),
    "ground": (["fire", "electric", "poison", "rock", "steel"], ["grass", "bug"], ["flying"]),
    "flying": (["grass", "fighting", "bug"], ["electric", "rock", "steel"], []),
    "psychic": (["fighting", "poison"], ["psychic", "steel"], ["dark"]),
    "bug": (["grass", "psychic", "dark"], ["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"], []),
    "rock": (["fire", "ice", "flying", "bug"], ["fighting", "ground", "steel"], []),
    "ghost": (["psychic", "ghost"], ["dark"], ["normal"]),
    "dragon": (["dragon"], ["steel"], ["fairy"]),
    "dark": (["psychic", "ghost"], ["fighting", "dark", "fairy"], []),
    "steel": (["ice", "rock", "fairy"], ["fire", "water", "electric", "steel"], []),
    "fairy": (["fighting", "dragon", "dark"], ["fire", "poison", "steel"], []),
}

def _mult(attacker, defender):
    strong, weak, immune = _OFFENSIVE[attacker]
    if defender in immune:
        return 0.0
    if defender in strong:
        return 2.0
    if defender in weak:
        return 0.5
    return 1.0

def weaknesses(types):
    """Return {attacking_type: multiplier} only for multipliers > 1."""
    result = {}
    for atk in _OFFENSIVE:
        m = 1.0
        for d in types:
            m *= _mult(atk, d)
        if m > 1:
            result[atk] = m
    return result

# ---------------------------------------------------------------- biome_map

def load_biomes():
    """Tag (#mod:is_x) -> short vanilla biome string (or a special label)."""
    mapping = {}
    if not os.path.exists(BIOME_MAP):
        return mapping
    current_tag = None
    with open(BIOME_MAP, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^## (#\S+)", line)
            if m:
                current_tag = m.group(1)
                continue
            if current_tag is None:
                continue
            if "TODOS os biomas" in line:
                mapping[current_tag] = "qualquer bioma da superfície"
            vanilla_match = re.match(r"^- \*\*Vanilla:\*\* (.+)", line)
            if vanilla_match and current_tag not in mapping:
                mapping[current_tag] = vanilla_match.group(1).strip()
    return mapping

BIOMES = load_biomes()

def resolve_biome(tag):
    if tag in BIOMES:
        value = BIOMES[tag]
        if value == "qualquer bioma da superfície":
            return value
        parts = [p.strip() for p in value.split(",")]
        if FULL or len(parts) <= MAX_BIOMES:
            return ", ".join(parts)
        return ", ".join(parts[:MAX_BIOMES]) + "…"
    # unmapped external-mod tag -> clean name
    clean = tag.split(":")[-1].replace("is_", "").replace("_", " ")
    return clean

def resolve_biomes(tags):
    return "; ".join(resolve_biome(t) for t in tags)

# ---------------------------------------------------------------- utils

def item_name(item_id):
    return item_id.split(":")[-1].replace("_", " ").title()

def titleize(s):
    return s.replace("_", " ").title()

# ---------------------------------------------------------------- spawns

def index_spawns():
    """species_name -> list of spawn entries (grouped from all files)."""
    index = {}
    for f in glob.glob(os.path.join(SPAWN_DIR, "*.json")):
        pool = json.load(open(f, encoding="utf-8"))
        if not pool.get("enabled", True):
            continue
        for spawn in pool.get("spawns", []):
            name = str(spawn.get("pokemon", "")).split()[0].lower()
            if name:
                index.setdefault(name, []).append(spawn)
    return index

SPAWN_INDEX = index_spawns()

def render_spawn(spawn):
    condition = spawn.get("condition", {})
    bucket = spawn.get("bucket", "?")

    parts = []
    if condition.get("biomes"):
        # only where it SPAWNS; anticondition biomes are noise for this question.
        parts.append(resolve_biomes(condition["biomes"]))

    time_range = condition.get("timeRange")
    if time_range:
        parts.append({"day": "de dia", "night": "de noite", "dusk": "ao entardecer"}.get(time_range, time_range))

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

    level = spawn.get("level", "?")
    body = ", ".join(parts) if parts else "condições variadas"
    return f"- [{bucket}] {body} — nível {level}"

def spawn_block(name):
    spawns = SPAWN_INDEX.get(name, [])
    if not spawns:
        return None
    lines = []
    seen = set()
    for spawn in spawns:
        line = render_spawn(spawn)
        if line not in seen:
            seen.add(line)
            lines.append(line)
    extra = ""
    if not FULL and len(lines) > MAX_SPAWN_LINES:
        extra = f"\n- … (+{len(lines) - MAX_SPAWN_LINES} condições; veja `/pwiki {name}` → Biome Spawns)"
        lines = lines[:MAX_SPAWN_LINES]
    return "\n".join(lines) + extra

# ---------------------------------------------------------------- evolutions

def render_requirement(r):
    v = r.get("variant")
    if v == "level":
        return f"nível {r.get('minLevel', r.get('amount', '?'))}+"
    if v == "friendship":
        return f"amizade ≥{r.get('amount', '?')}"
    if v == "time_range":
        return {"day": "de dia", "night": "de noite", "dusk": "ao entardecer"}.get(r.get("range"), r.get("range", ""))
    if v == "biome":
        # real biome tag (#mod:is_x) -> biomes; internal evolution tag
        # (#cobblemon:evolution/...) is not a real biome -> "certos biomas".
        def _label(tag):
            if not tag:
                return None
            if tag in BIOMES:
                return resolve_biome(tag)
            if "is_" in tag and "/" not in tag:
                return resolve_biome(tag)
            return "certos biomas"
        cond = _label(r.get("biomeCondition"))
        anti = _label(r.get("biomeAnticondition"))
        if cond:
            return "em " + cond
        if anti and anti != "certos biomas":
            return "fora de " + anti
        return None  # anti on an internal biome: not very informative, omit
    if v == "held_item":
        return "segurando " + item_name(r.get("itemCondition", ""))
    if v == "structure":
        return "perto de " + titleize(str(r.get("structureCondition", r.get("structure", ""))).split(":")[-1])
    if v == "has_move":
        return "conhecendo " + titleize(r.get("move", ""))
    if v == "has_move_type":
        return "com golpe do tipo " + TYPE_PT.get(r.get("type"), r.get("type", ""))
    if v == "moon_phase":
        return f"lua fase {r.get('moonPhase', '?')}"
    if v == "weather":
        return "com tempo específico"
    if v == "properties":
        target = r.get("target", "")
        return {"gender=male": "sendo macho", "gender=female": "sendo fêmea"}.get(target, target)
    if v == "property_range":
        return f"{r.get('feature', '')} {r.get('range', '')}".strip()
    if v == "use_move":
        return "usando um golpe X vezes"
    if v == "defeat":
        return "derrotando Pokémon específicos"
    if v == "blocks_traveled":
        return "após andar uma distância"
    if v in ("stat_compare", "stat_equal"):
        return "com relação específica de stats"
    if v == "party_member":
        return "com certo Pokémon no time"
    if v == "advancement":
        return "após um avanço (advancement)"
    return v or ""

def render_method(e):
    """Only the evolution method, e.g. 'usar Water Stone' / 'subir de nível (…)'."""
    variant = e.get("variant", "")
    reqs = [render_requirement(r) for r in e.get("requirements", [])]
    reqs = [r for r in reqs if r]
    if variant == "item_interact":
        base = "usar " + item_name(e.get("requiredContext", "item"))
    elif variant == "trade":
        base = "trocar"
    else:  # level_up / level
        base = "subir de nível"
    if reqs:
        base += " (" + ", ".join(reqs) + ")"
    return base

def render_evolution(e):
    return f"- {titleize(e.get('result', '?'))} — {render_method(e)}"

# Reverse index: base_name -> [(who_evolves_into_it, method)]. For the target's
# card (e.g. Vaporeon) to say "Evolui de: Eevee — usar Water Stone".
SPECIES_FILES = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(SPECIES_DIR, "*.json"))}

def index_pre_evolutions():
    pre = {}
    for f in glob.glob(os.path.join(SPECIES_DIR, "*.json")):
        species = json.load(open(f, encoding="utf-8"))
        source = species["name"]
        for e in species.get("evolutions", []):
            raw = re.sub(r"[^a-z0-9]", "", e.get("result", "").lower())
            target = raw if raw in SPECIES_FILES else e.get("result", "").split()[0].lower()
            pre.setdefault(target, []).append((source, render_method(e)))
    return pre

PRE_EVOLUTIONS = index_pre_evolutions()

# ---------------------------------------------------------------- card

def build_card(species, key):
    name = species["name"]
    types = [species["primaryType"]] + ([species["secondaryType"]] if species.get("secondaryType") else [])
    types_pt = "/".join(TYPE_PT.get(t, t) for t in types)

    lines = [f"# {name}  (#{species['nationalPokedexNumber']} · {types_pt})"]

    stats = species["baseStats"]
    lines.append(
        f"Stats base: HP {stats['hp']} / Atk {stats['attack']} / Def {stats['defence']} / "
        f"SpA {stats['special_attack']} / SpD {stats['special_defence']} / Spd {stats['speed']}"
    )

    # weaknesses
    weak_map = weaknesses(types)
    if weak_map:
        x4 = [TYPE_PT.get(t, t) for t, m in weak_map.items() if m >= 4]
        x2 = [TYPE_PT.get(t, t) for t, m in weak_map.items() if m == 2]
        parts = []
        if x4:
            parts.append("4x " + ", ".join(x4))
        if x2:
            parts.append("2x " + ", ".join(x2))
        lines.append("Fraco contra: " + " · ".join(parts))

    # abilities
    abilities = []
    for a in species.get("abilities", []):
        if a.startswith("h:"):
            abilities.append(titleize(a[2:]) + " (oculta)")
        else:
            abilities.append(titleize(a))
    if abilities:
        lines.append("Habilidades: " + ", ".join(abilities))

    EV_LABEL = {"hp": "HP", "attack": "Atk", "defence": "Def",
                "special_attack": "SpA", "special_defence": "SpD", "speed": "Spd"}
    ev = ", ".join(f"{v} {EV_LABEL.get(k, k)}"
                   for k, v in species.get("evYield", {}).items() if v)
    meta = [f"Catch rate: {species.get('catchRate', '?')}"]
    if ev:
        meta.append(f"EV yield: {ev}")
    if species.get("eggGroups"):
        meta.append("Egg groups: " + ", ".join(titleize(g) for g in species["eggGroups"]))
    lines.append(" · ".join(meta))

    # drops
    drops = species.get("drops", {}).get("entries", [])
    if drops:
        def _drop(entry):
            nm = item_name(entry["item"])
            if "percentage" in entry:
                return f"{nm} ({entry['percentage']}%)"
            if "quantityRange" in entry:
                return f"{nm} (qtd {entry['quantityRange']})"
            return nm
        lines.append("Drops: " + ", ".join(_drop(entry) for entry in drops))

    # spawn
    spawn_text = spawn_block(key)
    if spawn_text:
        lines.append("\n## Spawn\n" + spawn_text)
    else:
        lines.append("\n## Spawn\n- Não nasce naturalmente (sem spawn no mundo; obtido por evolução/troca/ovo).")

    # evolution (forward)
    evolutions = species.get("evolutions", [])
    if evolutions:
        lines.append("\n## Evolui em\n" + "\n".join(render_evolution(e) for e in evolutions))

    # pre-evolution (where it comes from) — answers "how do I get/evolve into X"
    pre_evos = PRE_EVOLUTIONS.get(key, [])
    if pre_evos:
        lines.append("\n## Evolui de\n" + "\n".join(f"- {src} — {met}" for src, met in pre_evos))

    # forms / gmax
    forms = [f.get("name") for f in species.get("forms", []) if f.get("name")]
    gmax = any("gmax" in f.get("aspects", []) for f in species.get("forms", []))
    footer = []
    if forms:
        footer.append("Formas: " + ", ".join(forms))
    if gmax:
        footer.append("Gigantamax: sim")
    if footer:
        lines.append("\n" + " · ".join(footer))

    lines.append(f"\n_Mais detalhes (golpes, TMs, EVs completos): `/pwiki {key}`._")
    return "\n".join(lines)

# ---------------------------------------------------------------- main

def main():
    global FULL
    files = glob.glob(os.path.join(SPECIES_DIR, "*.json"))
    species_data = [(os.path.basename(f)[:-5], json.load(open(f, encoding="utf-8"))) for f in files]

    for full, dest in [(False, OUT_DIR), (True, OUT_FULL_DIR)]:
        FULL = full
        os.makedirs(dest, exist_ok=True)
        for key, species in species_data:
            card = build_card(species, key)
            with open(os.path.join(dest, key + ".md"), "w", encoding="utf-8") as out:
                out.write(card)
        label = "full" if full else "slim"
        print(f"Generated {len(species_data)} {label} cards in {dest}")
    print(f"Biome tags loaded: {len(BIOMES)}")


if __name__ == "__main__":
    main()
