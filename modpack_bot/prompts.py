"""Builds the player-facing prompts and product messages (pt/en).

The strings here are deliberately Portuguese/English product copy and prompt
instructions written for the LLM to read — kept in their own module so the
wording lives in one place and the logic around it stays testable.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modpack_bot.llm import TokenUsage

# Shown to the player when no guide fits, or when the wiki gate rejects.
_FALLBACK = {
    "pt": "Não tenho essa informação, pergunta num canal de suporte!",
    "en": "I don't have that information, please ask in a support channel!",
}


def fallback_message(language: str) -> str:
    """The 'I don't know, ask support' line, in the routed language."""
    return _FALLBACK.get(language, _FALLBACK["pt"])


def facts_listing_message(lines: list[str], language: str) -> str:
    """Deterministic big-list reply: a short lead-in plus the Python-built data.

    Used for "liste todos os Pokémon do tipo X" — the list comes straight from
    facts.md so it is never truncated (answer model caps at 500 tokens) nor
    reworded/hallucinated, and costs 0 answer-model tokens.

    Example:
        >>> facts_listing_message(["- Fogo (1): Charizard"], "pt")
        'Aqui está:\\n- Fogo (1): Charizard'
    """
    lead = "Here it is:" if language == "en" else "Aqui está:"
    return lead + "\n" + "\n".join(lines)


def pokemon_instruction(pokemon: str, language: str) -> str:
    """Directive used when a Pokémon card replaces wikigui.md as the guide."""
    if language == "en":
        return (
            f"The guide below is the data sheet for the Pokémon {pokemon}. Answer using only "
            f"this data. For moves/TMs or anything not in the sheet, tell them to use "
            f"`/pwiki {pokemon}`. Do not invent data."
        )
    return (
        f"O guia abaixo é a ficha de dados do Pokémon {pokemon}. Responda à pergunta usando só "
        f"esses dados. Pra golpes/TMs ou algo que não esteja na ficha, diga pra usar "
        f"`/pwiki {pokemon}`. Não invente dados."
    )


def non_pokemon_instruction(language: str) -> str:
    """Directive used on wikigui.md when the question is NOT about a Pokémon."""
    if language == "en":
        return (
            "This question is not about a Pokémon (stronghold, village, items, blocks are "
            "Minecraft things). Do not mention `/pwiki`. If it's about how to use the wiki tool "
            "itself, explain from the guide; otherwise reply with exactly: "
            f'"{_FALLBACK["en"]}"'
        )
    return (
        "Esta pergunta não é sobre um Pokémon (stronghold, vila, itens e blocos são do "
        "Minecraft). Não mencione `/pwiki`. Se for sobre como usar a própria wiki, explique com "
        f'base no guia; senão responda exatamente: "{_FALLBACK["pt"]}"'
    )


def facts_filter_instruction(language: str) -> str:
    """Directive used on facts.md: point the model at the `filtrar_pokemon` tool."""
    if language == "en":
        return (
            "You have the `filtrar_pokemon` tool: it filters the modpack's Pokémon by type, "
            "category (legendary/mythical) and/or dropped item and returns the exact list with its "
            "count. ALWAYS call it for any question about which/how many Pokémon match a type, "
            "category or item — including crossed criteria (e.g. legendary Electric-types). Item "
            "names are in English: translate the item in the question before calling (e.g. 'lágrima "
            "de ghast' -> 'Ghast Tear'). LIST every name it returns, do not summarize or omit them. "
            "The drop data is COMPLETE: if the tool returns no Pokémon, answer that NO Pokémon in "
            "the modpack drops/matches that — never say you don't have the information. Use the "
            "guide only for the modpack's general totals. Never invent names."
        )
    return (
        "Você tem a ferramenta `filtrar_pokemon`: filtra os Pokémon do modpack por tipo, categoria "
        "(lendário/mítico) e/ou item dropado e devolve a lista exata com a contagem. SEMPRE chame a "
        "ferramenta para qualquer pergunta sobre quais/quantos Pokémon batem num tipo, categoria ou "
        "item — inclusive cruzando critérios (ex.: lendários do tipo Elétrico). Os nomes de itens são "
        "em inglês: traduza o item da pergunta antes de chamar (ex.: 'lágrima de ghast' -> 'Ghast "
        "Tear'). LISTE todos os nomes que ela retornar, sem resumir nem omitir. A lista de drops é "
        "COMPLETA: se a ferramenta não devolver nenhum Pokémon, responda que NENHUM Pokémon do "
        "modpack dropa/corresponde a isso — nunca diga que não tem a informação. Use o guia apenas "
        "para os totais gerais do modpack. Nunca invente nomes."
    )


def usage_suffix(usage: "TokenUsage") -> str:
    """Small footer showing the token cost of producing the answer.

    Example:
        >>> usage_suffix(TokenUsage(120, 30))
        '\\n\\n`⚙ 150 tokens (entrada 120 / saída 30)`'
    """
    return f"\n\n`⚙ {usage.total} tokens (entrada {usage.prompt} / saída {usage.completion})`"


def build_system_prompt(guide: str, instruction: str, language: str) -> str:
    """Assemble the answer-model system prompt around a guide and directive."""
    if language == "en":
        return (
            "You are the assistant for a Minecraft server. Answer simply and directly, like an "
            "experienced player helping another, using only the guide below. Answer ONLY what was "
            "asked — do not tack on neighbouring facts from the guide the player did not ask for. "
            f"If the answer isn't in the guide, say '{_FALLBACK['en']}'. {instruction} Keep biome, item and move "
            "names EXACTLY as written in the guide (do not translate them). When listing, list "
            "each name once and never repeat. Break the answer into short paragraphs: put each "
            "distinct topic (e.g. how to evolve vs. where to find it in the wild) in its own "
            "paragraph, separated by a blank line. Output ONLY the final message for the player "
            "— plain text, no internal notes, no labels like [System], no meta commentary, no "
            f"made-up follow-up questions. Always respond in English.\n\n--- GUIA ---\n{guide}"
        )
    return (
        "Você é o assistente do servidor de Minecraft. Responda de forma simples e direta, como "
        "um jogador experiente ajudando outro, usando só o guia abaixo. Responda SOMENTE o que foi "
        "perguntado — não acrescente fatos vizinhos do guia que o jogador não pediu. Se a resposta não "
        f"estiver no guia, diga '{_FALLBACK['pt']}'. {instruction} Mantenha os nomes de bioma, "
        "item e golpe EXATAMENTE como estão no guia (não traduza). Ao listar, cite cada nome só "
        "uma vez e nunca repita. Quebre a resposta em parágrafos curtos: coloque cada assunto "
        "distinto (ex.: como evoluir vs. onde encontrar no mundo) num parágrafo próprio, "
        "separado por uma linha em branco. Devolva APENAS a mensagem final pro jogador — texto "
        "puro, sem notas internas, sem rótulos tipo [Sistema], sem comentários meta, sem "
        f"inventar perguntas de acompanhamento. Responda sempre em português.\n\n--- GUIA ---\n{guide}"
    )
