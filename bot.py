import discord
import os
import re
import unicodedata
import difflib
from groq import Groq, RateLimitError
from dotenv import load_dotenv

load_dotenv()

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Models per stage, in priority order (falls through to the next on rate limit).
# Router = trivial classification, a cheap model is enough.
# Answer = quality matters (must not degenerate/hallucinate): 70b primary, scout
# (500K/day quota) takes the overflow, 8b is the last resort. All pure instruct
# (no reasoning models, which could leak <think> tokens into the answer).
ROUTER_MODELS = [
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]
ANSWER_MODELS = [
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.1-8b-instant",
]

def complete(messages, models, **kwargs):
    """Try the models in order; on a rate limit, fall through to the next one."""
    last_error = None
    for model in models:
        try:
            return groq.chat.completions.create(model=model, messages=messages, **kwargs)
        except RateLimitError as e:
            last_error = e
            continue
    raise last_error

GUIDE_DIR = "guia"

with open(os.path.join(GUIDE_DIR, "core.md"), "r", encoding="utf-8") as f:
    CORE = f.read()

VALID_GUIDES = {"market.md", "rules.md", "wiki.md"}

# Canonical Pokémon dictionary: the names of the pre-generated cards in
# species_cards/ are the source of truth for what is (and isn't) a Pokémon.
# (species/ is only build_cards.py input — it stays out of the repo/runtime.)
# In-memory lookup, 0 tokens.
CARDS_DIR = os.path.join(GUIDE_DIR, "pokemons-db", "species_cards")
CARDS_FULL_DIR = os.path.join(GUIDE_DIR, "pokemons-db", "species_cards_full")
POKEMON_NAMES = {f[:-3] for f in os.listdir(CARDS_DIR) if f.endswith(".md")}

def _tokens(text: str) -> list[str]:
    """Lowercase, accent-stripped, alphanumeric chunks only."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", text.lower())

def detect_pokemon(message: str) -> str | None:
    """Find a Pokémon name in the message, or None if there isn't one.

    Normalizes the same way as the file names (mrmime, hooh, tapukoko...). Joins
    adjacent word pairs ('mr mime' -> 'mrmime') and, as a last step, tries a
    conservative fuzzy match for typos ('pikachuu' -> 'pikachu')."""
    tokens = _tokens(message)
    bigrams = [a + b for a, b in zip(tokens, tokens[1:])]
    for candidate in bigrams + tokens:  # bigram first (longest match)
        if candidate in POKEMON_NAMES:
            return candidate
    for t in tokens:
        if len(t) >= 4:
            m = difflib.get_close_matches(t, POKEMON_NAMES, n=1, cutoff=0.85)
            if m:
                return m[0]
    return None

def route(message: str) -> tuple[str | None, str]:
    """Return (guide_file, language). guide_file is None if none fits."""
    routing = complete(
        models=ROUTER_MODELS,
        max_tokens=15,
        temperature=0,
        messages=[
            {"role": "system", "content": CORE},
            {"role": "user", "content": message}
        ]
    )
    output = routing.choices[0].message.content.strip().lower()

    guide_file, _, language = output.partition("|")
    guide_file = guide_file.strip()
    language = language.strip()

    guide_file = guide_file if guide_file in VALID_GUIDES else None
    language = language if language in ("pt", "en") else "pt"

    return guide_file, language

def load_guide(name: str) -> str:
    with open(os.path.join(GUIDE_DIR, name), "r", encoding="utf-8") as f:
        return f.read()

# Explicit request for a full list (e.g. "lista todos os biomas", "completo").
FULL_LIST_PATTERN = re.compile(
    r"\b(todos|todas|complet[oa]s?|lista(r|\b)|liste|list all|all of them|every|inteir)",
    re.IGNORECASE,
)

def wants_full_list(message: str) -> bool:
    return bool(FULL_LIST_PATTERN.search(message))

def load_card(name: str, full: bool = False) -> str | None:
    """Read a Pokémon's pre-generated card. full=True uses the untruncated
    version (on request); falls back to the slim one if the full is missing."""
    for directory in ([CARDS_FULL_DIR, CARDS_DIR] if full else [CARDS_DIR]):
        path = os.path.join(directory, name + ".md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online as {client.user}")

@client.event
async def on_message(message):
    if message.content == "!clear":
        if message.author.guild_permissions.administrator:
            await message.channel.purge()
            return
        else:
            await message.reply("Você não tem permissão!")
            return

    if message.author.bot:
        return
    if str(message.channel.id) != os.getenv("CANAL_ID"):
        return

    async with message.channel.typing():
        try:
            guide_file, language = route(message.content)

            if guide_file is None:
                if language == "en":
                    await message.reply("I don't have that information, please ask in a support channel!")
                else:
                    await message.reply("Não tenho essa informação, pergunta num canal de suporte!")
                return

            guide = load_guide(guide_file)

            # Pokémon gate (wiki.md only): deterministic name detection.
            # - found a Pokémon -> load its CARD (data) in place of wiki.md.
            # - found none      -> keep wiki.md (the tool's doc) and instruct it to
            #                       never suggest /pwiki for non-Pokémon (stronghold).
            # The instruction goes in as a directive (unlabeled) and the guide is
            # pure data, so a small model won't mimic/repeat labels in the final text.
            instruction_pt = instruction_en = ""
            if guide_file == "wiki.md":
                pokemon = detect_pokemon(message.content)
                card = load_card(pokemon, wants_full_list(message.content)) if pokemon else None
                if card:
                    guide = card
                    instruction_pt = f"O guia abaixo é a ficha de dados do Pokémon {pokemon}. Responda à pergunta usando só esses dados. Pra golpes/TMs ou algo que não esteja na ficha, diga pra usar `/pwiki {pokemon}`. Não invente dados."
                    instruction_en = f"The guide below is the data sheet for the Pokémon {pokemon}. Answer using only this data. For moves/TMs or anything not in the sheet, tell them to use `/pwiki {pokemon}`. Do not invent data."
                else:
                    instruction_pt = "Esta pergunta não é sobre um Pokémon (stronghold, vila, itens e blocos são do Minecraft). Não mencione `/pwiki`. Se for sobre como usar a própria wiki, explique com base no guia; senão responda exatamente: \"Não tenho essa informação, pergunta num canal de suporte!\""
                    instruction_en = "This question is not about a Pokémon (stronghold, village, items, blocks are Minecraft things). Do not mention `/pwiki`. If it's about how to use the wiki tool itself, explain from the guide; otherwise reply with exactly: \"I don't have that information, please ask in a support channel!\""

            if language == "en":
                system_prompt = f"You are the assistant for a Minecraft server. Answer simply and directly, like an experienced player helping another, using only the guide below. If the answer isn't in the guide, say 'I don't have that information, please ask in a support channel!'. {instruction_en} Keep biome, item and move names EXACTLY as written in the guide (do not translate them). When listing, list each name once and never repeat. Break the answer into short paragraphs: put each distinct topic (e.g. how to evolve vs. where to find it in the wild) in its own paragraph, separated by a blank line. Output ONLY the final message for the player — plain text, no internal notes, no labels like [System], no meta commentary, no made-up follow-up questions. Always respond in English.\n\n--- GUIA ---\n{guide}"
            else:
                system_prompt = f"Você é o assistente do servidor de Minecraft. Responda de forma simples e direta, como um jogador experiente ajudando outro, usando só o guia abaixo. Se a resposta não estiver no guia, diga 'Não tenho essa informação, pergunta num canal de suporte!'. {instruction_pt} Mantenha os nomes de bioma, item e golpe EXATAMENTE como estão no guia (não traduza). Ao listar, cite cada nome só uma vez e nunca repita. Quebre a resposta em parágrafos curtos: coloque cada assunto distinto (ex.: como evoluir vs. onde encontrar no mundo) num parágrafo próprio, separado por uma linha em branco. Devolva APENAS a mensagem final pro jogador — texto puro, sem notas internas, sem rótulos tipo [Sistema], sem comentários meta, sem inventar perguntas de acompanhamento. Responda sempre em português.\n\n--- GUIA ---\n{guide}"

            answer = complete(
                models=ANSWER_MODELS,
                max_tokens=500,
                temperature=0.4,
                frequency_penalty=0.6,
                presence_penalty=0.3,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message.content}
                ]
            )

            await message.reply(answer.choices[0].message.content)

        except Exception as e:
            print(e)
            await message.reply("Ocorreu um erro, tenta de novo!")

client.run(os.getenv("DISCORD_TOKEN"))
