from modpack_bot.prompts import (
    build_system_prompt,
    facts_listing_message,
    fallback_message,
    non_pokemon_instruction,
    pokemon_instruction,
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


def test_system_prompt_constrains_scope_to_the_question():
    # guards the "answer only what was asked" rule (faq.md over-answered with the
    # neighbouring port/launcher entries when asked just the modpack version).
    assert "SOMENTE o que foi perguntado" in build_system_prompt("G", "I", "pt")
    assert "ONLY what was asked" in build_system_prompt("G", "I", "en")
