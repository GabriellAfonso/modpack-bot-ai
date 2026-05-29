"""Gera 'cartas' compactas por Pokémon a partir do banco consolidado.

Roda OFFLINE, 1x (e de novo só quando os dados mudarem: addon, novos mons,
ou edição do biome_map.md). O bot nunca chama isto — em runtime ele só lê a
carta pronta em species_cards/<nome>.md.

Lê:  guia/pokemons-db/species/*.json
     guia/pokemons-db/spawn_pool_world/*.json
     guia/pokemons-db/biome_map.md
Gera: guia/pokemons-db/species_cards/<nome>.md
"""

import json
import glob
import os
import re

BASE = os.path.join("guia", "pokemons-db")
SPECIES_DIR = os.path.join(BASE, "species")
SPAWN_DIR = os.path.join(BASE, "spawn_pool_world")
BIOME_MAP = os.path.join(BASE, "biome_map.md")
OUT_DIR = os.path.join(BASE, "species_cards")        # versão enxuta (padrão)
OUT_FULL_DIR = os.path.join(BASE, "species_cards_full")  # versão completa (sob pedido)

MAX_SPAWN_LINHAS = 6
MAX_BIOMAS = 5

# Quando True, não trunca biomas nem linhas de spawn (gera a versão completa).
COMPLETO = False

# ---------------------------------------------------------------- tipos / PT

TIPO_PT = {
    "normal": "Normal", "fire": "Fogo", "water": "Água", "electric": "Elétrico",
    "grass": "Grama", "ice": "Gelo", "fighting": "Lutador", "poison": "Veneno",
    "ground": "Terra", "flying": "Voador", "psychic": "Psíquico", "bug": "Inseto",
    "rock": "Pedra", "ghost": "Fantasma", "dragon": "Dragão", "dark": "Sombrio",
    "steel": "Aço", "fairy": "Fada",
}

# Eficácia ofensiva: atacante -> (super-eficaz 2x, pouco-eficaz 0.5x, sem efeito 0x)
_OFENSIVA = {
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

def _mult(atacante, defensor):
    sup, fraco, zero = _OFENSIVA[atacante]
    if defensor in zero:
        return 0.0
    if defensor in sup:
        return 2.0
    if defensor in fraco:
        return 0.5
    return 1.0

def fraquezas(tipos):
    """Devolve {tipo_atacante: multiplicador} só pros multiplicadores > 1."""
    out = {}
    for atk in _OFENSIVA:
        m = 1.0
        for d in tipos:
            m *= _mult(atk, d)
        if m > 1:
            out[atk] = m
    return out

# ---------------------------------------------------------------- biome_map

def carregar_biomas():
    """Tag (#mod:is_x) -> string curta de biomas vanilla (ou rótulo especial)."""
    mapa = {}
    if not os.path.exists(BIOME_MAP):
        return mapa
    bloco = None
    especial = None
    with open(BIOME_MAP, encoding="utf-8") as f:
        for linha in f:
            m = re.match(r"^## (#\S+)", linha)
            if m:
                bloco = m.group(1)
                especial = None
                continue
            if bloco is None:
                continue
            if "TODOS os biomas" in linha:
                mapa[bloco] = "qualquer bioma da superfície"
            mv = re.match(r"^- \*\*Vanilla:\*\* (.+)", linha)
            if mv and bloco not in mapa:
                mapa[bloco] = mv.group(1).strip()
    return mapa

BIOMAS = carregar_biomas()

def resolver_bioma(tag):
    if tag in BIOMAS:
        v = BIOMAS[tag]
        if v == "qualquer bioma da superfície":
            return v
        partes = [p.strip() for p in v.split(",")]
        if COMPLETO or len(partes) <= MAX_BIOMAS:
            return ", ".join(partes)
        return ", ".join(partes[:MAX_BIOMAS]) + "…"
    # tag de mod externo não mapeada -> nome limpo
    limpo = tag.split(":")[-1].replace("is_", "").replace("_", " ")
    return limpo

def resolver_biomas(tags):
    return "; ".join(resolver_bioma(t) for t in tags)

# ---------------------------------------------------------------- utils

def nome_item(item_id):
    return item_id.split(":")[-1].replace("_", " ").title()

def titulo(s):
    return s.replace("_", " ").title()

# ---------------------------------------------------------------- spawns

def indexar_spawns():
    """nome_da_especie -> lista de entradas de spawn (agrupadas de todos os arquivos)."""
    idx = {}
    for f in glob.glob(os.path.join(SPAWN_DIR, "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        if not d.get("enabled", True):
            continue
        for s in d.get("spawns", []):
            nome = str(s.get("pokemon", "")).split()[0].lower()
            if nome:
                idx.setdefault(nome, []).append(s)
    return idx

SPAWN_IDX = indexar_spawns()

def render_spawn(s):
    cond = s.get("condition", {})
    bucket = s.get("bucket", "?")

    partes = []
    if cond.get("biomes"):
        # só onde NASCE; biomas de anticondition são ruído pra essa pergunta.
        partes.append(resolver_biomas(cond["biomes"]))

    tr = cond.get("timeRange")
    if tr:
        partes.append({"day": "de dia", "night": "de noite", "dusk": "ao entardecer"}.get(tr, tr))

    if cond.get("canSeeSky") is False:
        partes.append("sem ver o céu")
    if cond.get("isRaining") is True:
        partes.append("chovendo")
    if cond.get("structures"):
        partes.append("perto de " + ", ".join(titulo(x.split(":")[-1]) for x in cond["structures"]))
    if cond.get("neededNearbyBlocks"):
        partes.append("perto de " + ", ".join(nome_item(x) for x in cond["neededNearbyBlocks"]))
    if cond.get("moonPhase") is not None:
        partes.append(f"lua fase {cond['moonPhase']}")

    nivel = s.get("level", "?")
    corpo = ", ".join(partes) if partes else "condições variadas"
    return f"- [{bucket}] {corpo} — nível {nivel}"

def bloco_spawn(nome):
    spawns = SPAWN_IDX.get(nome, [])
    if not spawns:
        return None
    linhas = []
    vistos = set()
    for s in spawns:
        l = render_spawn(s)
        if l not in vistos:
            vistos.add(l)
            linhas.append(l)
    extra = ""
    if not COMPLETO and len(linhas) > MAX_SPAWN_LINHAS:
        extra = f"\n- … (+{len(linhas) - MAX_SPAWN_LINHAS} condições; veja `/pwiki {nome}` → Biome Spawns)"
        linhas = linhas[:MAX_SPAWN_LINHAS]
    return "\n".join(linhas) + extra

# ---------------------------------------------------------------- evoluções

def render_req(r):
    v = r.get("variant")
    if v == "level":
        return f"nível {r.get('minLevel', r.get('amount', '?'))}+"
    if v == "friendship":
        return f"amizade ≥{r.get('amount', '?')}"
    if v == "time_range":
        return {"day": "de dia", "night": "de noite", "dusk": "ao entardecer"}.get(r.get("range"), r.get("range", ""))
    if v == "biome":
        # tag de bioma real (#mod:is_x) -> biomas; tag interna de evolução
        # (#cobblemon:evolution/...) não é bioma de verdade -> "certos biomas".
        def _leg(tag):
            if not tag:
                return None
            if tag in BIOMAS:
                return resolver_bioma(tag)
            if "is_" in tag and "/" not in tag:
                return resolver_bioma(tag)
            return "certos biomas"
        cond = _leg(r.get("biomeCondition"))
        anti = _leg(r.get("biomeAnticondition"))
        if cond:
            return "em " + cond
        if anti and anti != "certos biomas":
            return "fora de " + anti
        return None  # anti em bioma interno: pouco informativo, omite
    if v == "held_item":
        return "segurando " + nome_item(r.get("itemCondition", ""))
    if v == "structure":
        return "perto de " + titulo(str(r.get("structureCondition", r.get("structure", ""))).split(":")[-1])
    if v == "has_move":
        return "conhecendo " + titulo(r.get("move", ""))
    if v == "has_move_type":
        return "com golpe do tipo " + TIPO_PT.get(r.get("type"), r.get("type", ""))
    if v == "moon_phase":
        return f"lua fase {r.get('moonPhase', '?')}"
    if v == "weather":
        return "com tempo específico"
    if v == "properties":
        alvo = r.get("target", "")
        return {"gender=male": "sendo macho", "gender=female": "sendo fêmea"}.get(alvo, alvo)
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

def render_metodo(e):
    """Só o método da evolução, ex.: 'usar Water Stone' / 'subir de nível (…)'."""
    variant = e.get("variant", "")
    reqs = [render_req(r) for r in e.get("requirements", [])]
    reqs = [r for r in reqs if r]
    if variant == "item_interact":
        base = "usar " + nome_item(e.get("requiredContext", "item"))
    elif variant == "trade":
        base = "trocar"
    else:  # level_up / level
        base = "subir de nível"
    if reqs:
        base += " (" + ", ".join(reqs) + ")"
    return base

def render_evo(e):
    return f"- {titulo(e.get('result', '?'))} — {render_metodo(e)}"

# Índice reverso: nome_base -> [(quem_evolui_nele, método)]. Pra carta do alvo
# (ex.: Vaporeon) dizer "Evolui de: Eevee — usar Water Stone".
SPECIES_FILES = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(SPECIES_DIR, "*.json"))}

def indexar_pre_evolucoes():
    pre = {}
    for f in glob.glob(os.path.join(SPECIES_DIR, "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        origem = d["name"]
        for e in d.get("evolutions", []):
            bruto = re.sub(r"[^a-z0-9]", "", e.get("result", "").lower())
            alvo = bruto if bruto in SPECIES_FILES else e.get("result", "").split()[0].lower()
            pre.setdefault(alvo, []).append((origem, render_metodo(e)))
    return pre

PRE_EVO = indexar_pre_evolucoes()

# ---------------------------------------------------------------- carta

def construir_carta(d, chave):
    nome = d["name"]
    tipos = [d["primaryType"]] + ([d["secondaryType"]] if d.get("secondaryType") else [])
    tipos_pt = "/".join(TIPO_PT.get(t, t) for t in tipos)

    L = [f"# {nome}  (#{d['nationalPokedexNumber']} · {tipos_pt})"]

    bs = d["baseStats"]
    L.append(
        f"Stats base: HP {bs['hp']} / Atk {bs['attack']} / Def {bs['defence']} / "
        f"SpA {bs['special_attack']} / SpD {bs['special_defence']} / Spd {bs['speed']}"
    )

    # fraquezas
    fr = fraquezas(tipos)
    if fr:
        x4 = [TIPO_PT.get(t, t) for t, m in fr.items() if m >= 4]
        x2 = [TIPO_PT.get(t, t) for t, m in fr.items() if m == 2]
        ps = []
        if x4:
            ps.append("4x " + ", ".join(x4))
        if x2:
            ps.append("2x " + ", ".join(x2))
        L.append("Fraco contra: " + " · ".join(ps))

    # habilidades
    habs = []
    for a in d.get("abilities", []):
        if a.startswith("h:"):
            habs.append(titulo(a[2:]) + " (oculta)")
        else:
            habs.append(titulo(a))
    if habs:
        L.append("Habilidades: " + ", ".join(habs))

    EV_LABEL = {"hp": "HP", "attack": "Atk", "defence": "Def",
                "special_attack": "SpA", "special_defence": "SpD", "speed": "Spd"}
    ev = ", ".join(f"{v} {EV_LABEL.get(k, k)}"
                   for k, v in d.get("evYield", {}).items() if v)
    metainfo = [f"Catch rate: {d.get('catchRate', '?')}"]
    if ev:
        metainfo.append(f"EV yield: {ev}")
    if d.get("eggGroups"):
        metainfo.append("Egg groups: " + ", ".join(titulo(g) for g in d["eggGroups"]))
    L.append(" · ".join(metainfo))

    # drops
    drops = d.get("drops", {}).get("entries", [])
    if drops:
        def _drop(e):
            nm = nome_item(e["item"])
            if "percentage" in e:
                return f"{nm} ({e['percentage']}%)"
            if "quantityRange" in e:
                return f"{nm} (qtd {e['quantityRange']})"
            return nm
        L.append("Drops: " + ", ".join(_drop(e) for e in drops))

    # spawn
    sb = bloco_spawn(chave)
    if sb:
        L.append("\n## Spawn\n" + sb)
    else:
        L.append("\n## Spawn\n- Não nasce naturalmente (sem spawn no mundo; obtido por evolução/troca/ovo).")

    # evolução (pra frente)
    evos = d.get("evolutions", [])
    if evos:
        L.append("\n## Evolui em\n" + "\n".join(render_evo(e) for e in evos))

    # pré-evolução (de onde vem) — resolve "como obtenho/evoluo pra X"
    pre = PRE_EVO.get(chave, [])
    if pre:
        L.append("\n## Evolui de\n" + "\n".join(f"- {src} — {met}" for src, met in pre))

    # formas / gmax
    formas = [f.get("name") for f in d.get("forms", []) if f.get("name")]
    gmax = any("gmax" in f.get("aspects", []) for f in d.get("forms", []))
    rodape = []
    if formas:
        rodape.append("Formas: " + ", ".join(formas))
    if gmax:
        rodape.append("Gigantamax: sim")
    if rodape:
        L.append("\n" + " · ".join(rodape))

    L.append(f"\n_Mais detalhes (golpes, TMs, EVs completos): `/pwiki {chave}`._")
    return "\n".join(L)

# ---------------------------------------------------------------- main

def main():
    global COMPLETO
    arquivos = glob.glob(os.path.join(SPECIES_DIR, "*.json"))
    dados = [(os.path.basename(f)[:-5], json.load(open(f, encoding="utf-8"))) for f in arquivos]

    for modo, destino in [(False, OUT_DIR), (True, OUT_FULL_DIR)]:
        COMPLETO = modo
        os.makedirs(destino, exist_ok=True)
        for chave, d in dados:
            carta = construir_carta(d, chave)
            with open(os.path.join(destino, chave + ".md"), "w", encoding="utf-8") as out:
                out.write(carta)
        rotulo = "completas" if modo else "enxutas"
        print(f"Geradas {len(dados)} cartas {rotulo} em {destino}")
    print(f"Tags de bioma carregadas: {len(BIOMAS)}")


if __name__ == "__main__":
    main()
