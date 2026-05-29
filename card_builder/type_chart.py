"""Pokémon type chart: PT names and defensive weakness computation."""

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


def _mult(attacker: str, defender: str) -> float:
    """Single-type damage multiplier of `attacker` hitting `defender`."""
    strong, weak, immune = _OFFENSIVE[attacker]
    if defender in immune:
        return 0.0
    if defender in strong:
        return 2.0
    if defender in weak:
        return 0.5
    return 1.0


def weaknesses(types: list[str]) -> dict[str, float]:
    """Return {attacking_type: multiplier} only for multipliers > 1.

    Example:
        >>> weaknesses(["fire", "flying"])["rock"]
        4.0
    """
    result: dict[str, float] = {}
    for attacker in _OFFENSIVE:
        multiplier = 1.0
        for defender in types:
            multiplier *= _mult(attacker, defender)
        if multiplier > 1:
            result[attacker] = multiplier
    return result
