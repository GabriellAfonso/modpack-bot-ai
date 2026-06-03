"""Cross-criteria Pokémon filter, exposed to the answer model as a tool.

The deterministic facts lists answer one axis at a time (a type, a category, an
item). Questions that cross axes — "quais lendários do tipo elétrico" — have no
precomputed line. This gives the answer model one tool, `filtrar_pokemon`: it
picks the filters, this code intersects the name sets parsed straight from
facts.md and returns the exact list, so names are never invented.
"""

from card_builder.categories import CATEGORIES
from card_builder.type_chart import TYPE_PT
from modpack_bot.facts_index import _split_sections
from modpack_bot.llm import ToolDispatch, ToolSpec
from modpack_bot.text import normalize_tokens

FILTER_TOOL_NAME = "filtrar_pokemon"


class PokemonFilter:
    """Name sets per type / category / item, with cross-axis intersection."""

    def __init__(
        self,
        types: dict[str, frozenset[str]],
        categories: dict[str, frozenset[str]],
        items: dict[str, frozenset[str]],
    ) -> None:
        self._types = types
        self._categories = categories
        self._items = items

    def query(
        self, types: list[str], categories: list[str], items: list[str]
    ) -> list[str]:
        """Display names matching ALL provided axes (union of terms within an axis).

        Example:
            >>> f = PokemonFilter(
            ...     {"electric": frozenset({"Zapdos", "Pikachu"})},
            ...     {"legendary": frozenset({"Zapdos", "Mewtwo"})}, {})
            >>> f.query(["electric"], ["legendary"], [])
            ['Zapdos']
        """
        axes = [
            _resolve(types, self._types),
            _resolve(categories, self._categories),
            self._resolve_items(items),
        ]
        constraining = [axis for axis in axes if axis is not None]
        if not constraining:
            return []
        return sorted(set.intersection(*constraining), key=_sort_key)

    def _resolve_items(self, terms: list[str]) -> "set[str] | None":
        """Union of droppers for every item term, or None when no terms (axis off)."""
        if not terms:
            return None
        matched: set[str] = set()
        for term in terms:
            matched |= self._item_match(term)
        return matched

    def _item_match(self, term: str) -> set[str]:
        """Droppers for one item term: exact label first, else any label whose
        tokens are a superset of the term's.

        The answer model translates the item before calling, but may stop at the
        base word — "slime" instead of the actual item "Slime Ball". The token
        fallback maps "slime" -> "Slime Ball" while an exact term like "bone"
        still resolves to "Bone" alone (it never widens to "Bone Meal").
        """
        key = _key(term)
        if key in self._items:
            return set(self._items[key])
        wanted = set(key.split())
        if not wanted:
            return set()
        matched: set[str] = set()
        for label, droppers in self._items.items():
            if wanted <= set(label.split()):
                matched |= droppers
        return matched


def build_pokemon_filter(facts_md: str) -> PokemonFilter:
    """Parse facts.md's type/item/category lists into a queryable filter."""
    sections = _split_sections(facts_md)
    if sections is None:
        return PokemonFilter({}, {}, {})
    _, type_lines, item_lines, category_lines = sections
    return PokemonFilter(
        _type_index(type_lines), _category_index(category_lines), _item_index(item_lines)
    )


def filter_tool_spec() -> ToolSpec:
    """The Groq tool definition the answer model sees for facts questions."""
    return {
        "type": "function",
        "function": {
            "name": FILTER_TOOL_NAME,
            "description": (
                "Filtra os Pokémon do modpack cruzando critérios e devolve a lista exata. "
                "Use para perguntas que combinam tipo, categoria (lendário/mítico) e/ou item "
                "dropado — ex.: 'quais lendários do tipo elétrico'. Os filtros são combinados "
                "por interseção (precisa bater em todos)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tipos em inglês: electric, fire, water, grass, ...",
                    },
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Categorias: legendary e/ou mythical.",
                    },
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Nome do item dropado em inglês, ex.: Bone, Leather.",
                    },
                },
            },
        },
    }


def make_dispatch(pokemon_filter: PokemonFilter) -> ToolDispatch:
    """Bind a filter to a dispatch callable the completer runs on a tool call."""

    def dispatch(name: str, arguments: dict[str, object]) -> str:
        if name != FILTER_TOOL_NAME:
            raise ValueError(f"unknown tool {name!r}, expected {FILTER_TOOL_NAME!r}")
        names = pokemon_filter.query(
            _string_list(arguments.get("types")),
            _string_list(arguments.get("categories")),
            _string_list(arguments.get("items")),
        )
        return _format_names(names)

    return dispatch


def _resolve(terms: list[str], index: dict[str, frozenset[str]]) -> "set[str] | None":
    """Union of the name sets for every term, or None when no terms (axis is off)."""
    if not terms:
        return None
    matched: set[str] = set()
    for term in terms:
        matched |= index.get(_key(term), frozenset())
    return matched


def _type_index(type_lines: dict[str, str]) -> dict[str, frozenset[str]]:
    """{english id and PT label -> names} for every type that has a facts line."""
    index: dict[str, frozenset[str]] = {}
    for english, pt_name in TYPE_PT.items():
        label = _key(pt_name)
        if label in type_lines:
            names = _line_names(type_lines[label])
            index[english] = names
            index[label] = names
    return index


def _category_index(category_lines: dict[str, str]) -> dict[str, frozenset[str]]:
    """{english label, PT label and every synonym -> names} per surfaced category."""
    index: dict[str, frozenset[str]] = {}
    for label, category in CATEGORIES.items():
        pt_key = _key(category.pt_name)
        if pt_key not in category_lines:
            continue
        names = _line_names(category_lines[pt_key])
        for term in (label, pt_key, *category.synonyms):
            index[_key(term)] = names
    return index


def _item_index(item_lines: dict[str, str]) -> dict[str, frozenset[str]]:
    """{normalized item label -> dropper names} for every item facts line."""
    return {label: _line_names(line) for label, line in item_lines.items()}


def _line_names(line: str) -> frozenset[str]:
    """The display names from a '- Label (n): A, B, C' facts line.

    Splits on ', ' so multi-word names ('Tapu Koko', 'Type: Null') stay intact.
    """
    _, _, names = line.partition(": ")
    return frozenset(name.strip() for name in names.split(", ") if name.strip())


def _format_names(names: list[str]) -> str:
    """The tool's text result the model reads to compose its reply."""
    if not names:
        return "Nenhum Pokémon corresponde a esses filtros."
    return f"{len(names)} Pokémon: " + ", ".join(names)


def _string_list(value: object) -> list[str]:
    """Coerce a tool argument into a list of strings (the model may omit it)."""
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _key(term: str) -> str:
    """Normalized lookup key: lowercase, accent-stripped, single-spaced."""
    return " ".join(normalize_tokens(term))


def _sort_key(name: str) -> str:
    """Accent-insensitive ordering key so 'Água' sorts before 'Zapdos'."""
    return " ".join(normalize_tokens(name))
