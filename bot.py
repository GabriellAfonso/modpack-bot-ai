import discord
import os
import re
import unicodedata
import difflib
from groq import Groq, RateLimitError
from dotenv import load_dotenv

load_dotenv()

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Modelos por etapa, em ordem de prioridade (cai pro próximo em rate limit).
# Roteador = classificação trivial, modelo barato basta.
# Resposta = qualidade importa (não degenerar/alucinar): 70b primário, scout
# (cota de 500K/dia) pega o overflow, 8b é o último recurso. Tudo instruct puro
# (sem modelos de raciocínio, que poderiam vazar tokens de <think> na resposta).
MODELOS_ROTEADOR = [
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]
MODELOS_RESPOSTA = [
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.1-8b-instant",
]

def completar(messages, modelos, **kwargs):
    """Tenta os modelos da lista em ordem; ao pegar rate limit, cai pro próximo."""
    ultimo_erro = None
    for modelo in modelos:
        try:
            return groq.chat.completions.create(model=modelo, messages=messages, **kwargs)
        except RateLimitError as e:
            ultimo_erro = e
            continue
    raise ultimo_erro

GUIA_DIR = "guia"

with open(os.path.join(GUIA_DIR, "core.md"), "r", encoding="utf-8") as f:
    CORE = f.read()

ARQUIVOS_VALIDOS = {"market.md", "rules.md", "wiki.md"}

# Dicionário canônico de Pokémon: os nomes das cartas pré-geradas em
# species_cards/ são a fonte da verdade do que é (e do que não é) um Pokémon.
# (species/ é só insumo do build_cards.py — fica fora do repo/runtime.)
# Lookup em memória, 0 tokens.
CARDS_DIR = os.path.join(GUIA_DIR, "pokemons-db", "species_cards")
CARDS_FULL_DIR = os.path.join(GUIA_DIR, "pokemons-db", "species_cards_full")
POKEMONS = {f[:-3] for f in os.listdir(CARDS_DIR) if f.endswith(".md")}

def _tokens(texto: str) -> list[str]:
    """Minúsculas, sem acento, só pedaços alfanuméricos."""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", texto.lower())

def detectar_pokemon(mensagem: str) -> str | None:
    """Acha o nome de um Pokémon na mensagem, ou None se não houver.

    Normaliza igual aos nomes de arquivo (mrmime, hooh, tapukoko...). Junta
    pares de palavras adjacentes ('mr mime' -> 'mrmime') e, por último, tenta
    um fuzzy conservador pra typos ('pikachuu' -> 'pikachu')."""
    tokens = _tokens(mensagem)
    bigramas = [a + b for a, b in zip(tokens, tokens[1:])]
    for candidato in bigramas + tokens:  # bigrama primeiro (match mais longo)
        if candidato in POKEMONS:
            return candidato
    for t in tokens:
        if len(t) >= 4:
            m = difflib.get_close_matches(t, POKEMONS, n=1, cutoff=0.85)
            if m:
                return m[0]
    return None

def rotear(mensagem: str) -> tuple[str | None, str]:
    """Retorna (arquivo, idioma). arquivo é None se nenhum se encaixar."""
    rota = completar(
        modelos=MODELOS_ROTEADOR,
        max_tokens=15,
        temperature=0,
        messages=[
            {"role": "system", "content": CORE},
            {"role": "user", "content": mensagem}
        ]
    )
    saida = rota.choices[0].message.content.strip().lower()

    arquivo, _, idioma = saida.partition("|")
    arquivo = arquivo.strip()
    idioma = idioma.strip()

    arquivo = arquivo if arquivo in ARQUIVOS_VALIDOS else None
    idioma = idioma if idioma in ("pt", "en") else "pt"

    return arquivo, idioma

def carregar_guia(arquivo: str) -> str:
    with open(os.path.join(GUIA_DIR, arquivo), "r", encoding="utf-8") as f:
        return f.read()

# Pedido explícito de lista completa (ex.: "lista todos os biomas", "completo").
PADRAO_COMPLETO = re.compile(
    r"\b(todos|todas|complet[oa]s?|lista(r|\b)|liste|list all|all of them|every|inteir)",
    re.IGNORECASE,
)

def quer_lista_completa(mensagem: str) -> bool:
    return bool(PADRAO_COMPLETO.search(mensagem))

def carregar_carta(nome: str, completo: bool = False) -> str | None:
    """Lê a carta pré-gerada de um Pokémon. completo=True usa a versão sem
    truncamento (sob pedido); cai pra enxuta se a completa não existir."""
    for d in ([CARDS_FULL_DIR, CARDS_DIR] if completo else [CARDS_DIR]):
        caminho = os.path.join(d, nome + ".md")
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
    return None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online como {client.user}")

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
            arquivo, idioma = rotear(message.content)

            if arquivo is None:
                if idioma == "en":
                    await message.reply("I don't have that information, please ask in a support channel!")
                else:
                    await message.reply("Não tenho essa informação, pergunta num canal de suporte!")
                return

            guia = carregar_guia(arquivo)

            # Gate de Pokémon (só pro wiki.md): detecção determinística do nome.
            # - achou Pokémon  -> carrega a CARTA dele (dados) no lugar do wiki.md.
            # - não achou      -> mantém o wiki.md (doc da ferramenta) e instrui a
            #                      nunca sugerir /pwiki com não-Pokémon (stronghold).
            # A instrução vai como diretiva (não rotulada) e o guia é só dado puro,
            # pra um modelo pequeno não imitar/repetir rótulos no texto final.
            instrucao_pt = instrucao_en = ""
            if arquivo == "wiki.md":
                pkmn = detectar_pokemon(message.content)
                carta = carregar_carta(pkmn, quer_lista_completa(message.content)) if pkmn else None
                if carta:
                    guia = carta
                    instrucao_pt = f"O guia abaixo é a ficha de dados do Pokémon {pkmn}. Responda à pergunta usando só esses dados. Pra golpes/TMs ou algo que não esteja na ficha, diga pra usar `/pwiki {pkmn}`. Não invente dados."
                    instrucao_en = f"The guide below is the data sheet for the Pokémon {pkmn}. Answer using only this data. For moves/TMs or anything not in the sheet, tell them to use `/pwiki {pkmn}`. Do not invent data."
                else:
                    instrucao_pt = "Esta pergunta não é sobre um Pokémon (stronghold, vila, itens e blocos são do Minecraft). Não mencione `/pwiki`. Se for sobre como usar a própria wiki, explique com base no guia; senão responda exatamente: \"Não tenho essa informação, pergunta num canal de suporte!\""
                    instrucao_en = "This question is not about a Pokémon (stronghold, village, items, blocks are Minecraft things). Do not mention `/pwiki`. If it's about how to use the wiki tool itself, explain from the guide; otherwise reply with exactly: \"I don't have that information, please ask in a support channel!\""

            if idioma == "en":
                system_prompt = f"You are the assistant for a Minecraft server. Answer simply and directly, like an experienced player helping another, using only the guide below. If the answer isn't in the guide, say 'I don't have that information, please ask in a support channel!'. {instrucao_en} Keep biome, item and move names EXACTLY as written in the guide (do not translate them). When listing, list each name once and never repeat. Break the answer into short paragraphs: put each distinct topic (e.g. how to evolve vs. where to find it in the wild) in its own paragraph, separated by a blank line. Output ONLY the final message for the player — plain text, no internal notes, no labels like [System], no meta commentary, no made-up follow-up questions. Always respond in English.\n\n--- GUIA ---\n{guia}"
            else:
                system_prompt = f"Você é o assistente do servidor de Minecraft. Responda de forma simples e direta, como um jogador experiente ajudando outro, usando só o guia abaixo. Se a resposta não estiver no guia, diga 'Não tenho essa informação, pergunta num canal de suporte!'. {instrucao_pt} Mantenha os nomes de bioma, item e golpe EXATAMENTE como estão no guia (não traduza). Ao listar, cite cada nome só uma vez e nunca repita. Quebre a resposta em parágrafos curtos: coloque cada assunto distinto (ex.: como evoluir vs. onde encontrar no mundo) num parágrafo próprio, separado por uma linha em branco. Devolva APENAS a mensagem final pro jogador — texto puro, sem notas internas, sem rótulos tipo [Sistema], sem comentários meta, sem inventar perguntas de acompanhamento. Responda sempre em português.\n\n--- GUIA ---\n{guia}"

            resposta = completar(
                modelos=MODELOS_RESPOSTA,
                max_tokens=500,
                temperature=0.4,
                frequency_penalty=0.6,
                presence_penalty=0.3,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message.content}
                ]
            )

            await message.reply(resposta.choices[0].message.content)

        except Exception as e:
            print(e)
            await message.reply("Ocorreu um erro, tenta de novo!")

client.run(os.getenv("DISCORD_TOKEN"))
