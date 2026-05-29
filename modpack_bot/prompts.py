"""Builds the player-facing prompts and product messages (pt/en).

The strings here are deliberately Portuguese/English product copy and prompt
instructions written for the LLM to read — kept in their own module so the
wording lives in one place and the logic around it stays testable.
"""

# Shown to the player when no guide fits, or when the wiki gate rejects.
_FALLBACK = {
    "pt": "Não tenho essa informação, pergunta num canal de suporte!",
    "en": "I don't have that information, please ask in a support channel!",
}


def fallback_message(language: str) -> str:
    """The 'I don't know, ask support' line, in the routed language."""
    return _FALLBACK.get(language, _FALLBACK["pt"])


def pokemon_instruction(pokemon: str, language: str) -> str:
    """Directive used when a Pokémon card replaces wiki.md as the guide."""
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
    """Directive used on wiki.md when the question is NOT about a Pokémon."""
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


def build_system_prompt(guide: str, instruction: str, language: str) -> str:
    """Assemble the answer-model system prompt around a guide and directive."""
    if language == "en":
        return (
            "You are the assistant for a Minecraft server. Answer simply and directly, like an "
            "experienced player helping another, using only the guide below. If the answer isn't "
            f"in the guide, say '{_FALLBACK['en']}'. {instruction} Keep biome, item and move "
            "names EXACTLY as written in the guide (do not translate them). When listing, list "
            "each name once and never repeat. Break the answer into short paragraphs: put each "
            "distinct topic (e.g. how to evolve vs. where to find it in the wild) in its own "
            "paragraph, separated by a blank line. Output ONLY the final message for the player "
            "— plain text, no internal notes, no labels like [System], no meta commentary, no "
            f"made-up follow-up questions. Always respond in English.\n\n--- GUIA ---\n{guide}"
        )
    return (
        "Você é o assistente do servidor de Minecraft. Responda de forma simples e direta, como "
        "um jogador experiente ajudando outro, usando só o guia abaixo. Se a resposta não "
        f"estiver no guia, diga '{_FALLBACK['pt']}'. {instruction} Mantenha os nomes de bioma, "
        "item e golpe EXATAMENTE como estão no guia (não traduza). Ao listar, cite cada nome só "
        "uma vez e nunca repita. Quebre a resposta em parágrafos curtos: coloque cada assunto "
        "distinto (ex.: como evoluir vs. onde encontrar no mundo) num parágrafo próprio, "
        "separado por uma linha em branco. Devolva APENAS a mensagem final pro jogador — texto "
        "puro, sem notas internas, sem rótulos tipo [Sistema], sem comentários meta, sem "
        f"inventar perguntas de acompanhamento. Responda sempre em português.\n\n--- GUIA ---\n{guide}"
    )
