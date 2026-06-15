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


def spawn_help_message(language: str) -> str:
    """Reply to a nameless 'where does a Pokémon spawn' question (no LLM).

    Points the player at the two ways to get spawn data: ask here with the
    species name (answered from the card), or use `/pwiki <species>` in game.

    Example:
        >>> spawn_help_message("en").startswith("Tell me which")
        True
    """
    if language == "en":
        return (
            "Tell me which Pokémon and I'll show where it spawns — e.g. \"where does "
            "Pikachu spawn?\". In game you can also open `/pwiki <species>`."
        )
    return (
        "Me diz qual Pokémon que eu te falo onde ele spawna — ex.: \"onde o Pikachu "
        "spawna?\". No jogo também dá pra abrir `/pwiki <species>`."
    )


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


def pokemon_obtain_instruction(pokemon: str, language: str) -> str:
    """Directive when {pokemon} has no natural spawn and the card is followed by
    RAG passages: let the model use those passages to explain how to obtain it
    (mod summon, evolution, trade, egg), instead of dead-ending on the card."""
    if language == "en":
        return (
            f"The guide below is the data sheet for {pokemon}, followed by passages from the "
            f"server wiki. {pokemon} has no natural spawn, so use the passages to explain how to "
            f"obtain it (mod summon ritual, evolution, trade or egg). If the passages don't say "
            f"how to get it, tell them to use `/pwiki {pokemon}`. For moves/TMs use `/pwiki "
            f"{pokemon}`. Do not invent data."
        )
    return (
        f"O guia abaixo é a ficha do Pokémon {pokemon}, seguida de trechos da wiki do servidor. "
        f"{pokemon} não tem spawn natural, então use os trechos pra explicar como obtê-lo "
        f"(ritual de invocação de mod, evolução, troca ou ovo). Se os trechos não disserem como "
        f"conseguir, diga pra usar `/pwiki {pokemon}`. Pra golpes/TMs, use `/pwiki {pokemon}`. "
        f"Não invente dados."
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


def claim_instruction(language: str) -> str:
    """Directive used on the Flan land-protection guide (the claim gate)."""
    if language == "en":
        return (
            "The guide below is the Flan land-protection (claim) system. The player wants to keep "
            "others from stealing from their chests or base. Explain concretely how to claim the "
            "area with the Golden Hoe and how that stops outsiders from opening chests or breaking "
            "blocks. Do not mention `/pwiki`."
        )
    return (
        "O guia abaixo é o sistema de proteção de terreno (claim) do Flan. O jogador quer impedir "
        "que roubem os baús ou a base dele. Explique de forma concreta como clamar a área com a "
        "Enxada Dourada e como isso impede que outros abram baús ou quebrem blocos. Não mencione "
        "`/pwiki`."
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


def condense_system_prompt(transcript: str, language: str) -> str:
    """System prompt that rewrites a follow-up into a standalone question.

    The player's new message is sent as the user turn; the recent transcript is
    embedded here so the model can resolve references ("ele", "isso", "esse")
    into explicit terms — making the rewritten question safe to feed the gates
    and retrieval, which see one message at a time.

    Example:
        >>> "HISTÓRICO" in condense_system_prompt("Jogador: x\\nBot: y", "pt")
        True
    """
    if language == "en":
        return (
            "Rewrite the player's latest message as a standalone question that makes sense on its "
            "own, without the history. Use the history ONLY to resolve references (it, that, this "
            "Pokémon, and then). If the message already stands on its own, return it unchanged. Do "
            "NOT answer it. Output ONLY the rewritten question, nothing else, in the same language "
            f"as the player.\n\n--- HISTORY ---\n{transcript}"
        )
    return (
        "Reescreva a última mensagem do jogador como uma pergunta independente, que faça sentido "
        "sozinha, sem o histórico. Use o histórico APENAS para resolver referências (ele, isso, "
        "esse Pokémon, e aí). Se a mensagem já fizer sentido sozinha, devolva ela igual. NÃO "
        "responda a pergunta. Devolva APENAS a pergunta reescrita, nada mais, na mesma língua do "
        f"jogador.\n\n--- HISTÓRICO ---\n{transcript}"
    )


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
