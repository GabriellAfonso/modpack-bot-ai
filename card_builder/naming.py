"""Pure helpers that turn raw ids into human labels."""

# PT phrasing for a time-of-day range (shared by spawns and evolutions).
TIME_PT = {"day": "de dia", "night": "de noite", "dusk": "ao entardecer"}


def item_name(item_id: str) -> str:
    """'cobblemon:water_stone' -> 'Water Stone'.

    Example:
        >>> item_name("cobblemon:water_stone")
        'Water Stone'
    """
    return item_id.split(":")[-1].replace("_", " ").title()


def titleize(text: str) -> str:
    """'level_up' -> 'Level Up'."""
    return text.replace("_", " ").title()
