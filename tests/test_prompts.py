from modpack_bot.prompts import (
    build_system_prompt,
    facts_filter_instruction,
    facts_listing_message,
    fallback_message,
    non_pokemon_instruction,
    pokemon_instruction,
    pokemon_obtain_instruction,
)


def test_fallback_message_per_language():
    assert "suporte" in fallback_message("pt")
    assert "support channel" in fallback_message("en")
    assert fallback_message("xx") == fallback_message("pt")  # default


def test_pokemon_instruction_names_the_pokemon_and_pwiki():
    pt = pokemon_instruction("pikachu", "pt")
    assert "pikachu" in pt and "/pwiki pikachu" in pt and "Não invente" in pt
    en = pokemon_instruction("pikachu", "en")
    assert "Do not invent" in en


def test_pokemon_obtain_instruction_directs_model_to_the_passages():
    pt = pokemon_obtain_instruction("zekrom", "pt")
    assert "zekrom" in pt and "não tem spawn natural" in pt and "/pwiki zekrom" in pt
    en = pokemon_obtain_instruction("zekrom", "en")
    assert "no natural spawn" in en and "Do not invent" in en


def test_pokemon_obtain_instruction_asks_for_the_structure_location():
    # "como acho" is a WHERE question: the answer must name the structure/local
    # (e.g. the monument) where the obtain ritual happens, not just the items.
    assert "estrutura" in pokemon_obtain_instruction("zekrom", "pt")
    assert "structure" in pokemon_obtain_instruction("zekrom", "en")


def test_pokemon_obtain_instruction_does_not_defer_item_sourcing_to_pwiki():
    # /pwiki is the Cobblemon Pokédex; it has no data on Legendary Monuments mod
    # items/structures, so the obtain path must route missing info to support,
    # not to /pwiki (regression for the zekrom "use /pwiki for the items" reply).
    pt = pokemon_obtain_instruction("zekrom", "pt")
    assert "canal de suporte" in pt and "NUNCA" in pt
    en = pokemon_obtain_instruction("zekrom", "en")
    assert "support channel" in en and "NEVER" in en


def test_non_pokemon_instruction_forbids_pwiki():
    assert "Não mencione `/pwiki`" in non_pokemon_instruction("pt")
    assert "Do not mention `/pwiki`" in non_pokemon_instruction("en")


def test_facts_listing_message_leads_then_lists_per_language():
    assert facts_listing_message(["- Fogo (1): X"], "pt") == "Aqui está:\n- Fogo (1): X"
    assert facts_listing_message(["- Fogo (1): X"], "en") == "Here it is:\n- Fogo (1): X"


def test_system_prompt_embeds_guide_and_instruction():
    prompt = build_system_prompt("GUIDE BODY", "INSTRUCTION X", "pt")
    assert "GUIDE BODY" in prompt and "INSTRUCTION X" in prompt
    assert "português" in prompt


def test_system_prompt_english_variant():
    prompt = build_system_prompt("G", "I", "en")
    assert "Always respond in English" in prompt


def test_facts_filter_instruction_translates_items_and_owns_empty_result():
    # "quais pokemons dropam lagrima de gast" used to hit the generic "don't have
    # info" fallback while the English "ghast tear" answered "none drop it". The
    # instruction now tells the model to translate the item and treat an empty
    # tool result as "no Pokémon drops it", never the fallback.
    pt = facts_filter_instruction("pt")
    assert "Ghast Tear" in pt and "traduza" in pt
    assert "NENHUM Pokémon" in pt and "nunca diga que não tem a informação" in pt
    en = facts_filter_instruction("en")
    assert "Ghast Tear" in en and "translate" in en
    assert "NO Pokémon" in en and "never say you don't have" in en


def test_system_prompt_constrains_scope_to_the_question():
    # guards the "answer only what was asked" rule (faq.md over-answered with the
    # neighbouring port/launcher entries when asked just the modpack version).
    assert "SOMENTE o que foi perguntado" in build_system_prompt("G", "I", "pt")
    assert "ONLY what was asked" in build_system_prompt("G", "I", "en")
