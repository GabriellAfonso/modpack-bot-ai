# Plano: migrar o roteamento para RAG com LlamaIndex

> Documento para auditoria. Nada de código foi alterado ainda.
> Todas as decisões estão fechadas (§13).

## 1. Objetivo

Trocar o roteador baseado em LLM (que escolhe **um** arquivo de guia por
pergunta) por **recuperação semântica (RAG)** sobre todo o conteúdo `.md`,
usando **LlamaIndex**. A geração da resposta continua no **Groq**. Os caminhos
determinísticos de alta precisão (ficha de um Pokémon, contagens/listas,
admins) **continuam** — arquitetura híbrida.

## 2. Arquitetura atual (o que existe hoje)

Fluxo por mensagem (`modpack_bot/responder.py::Responder.answer`):

1. `reset_usage()` no completer.
2. **Router LLM** (`router.py`): 1 chamada Groq (modelo barato) → devolve
   `arquivo|idioma`. O catálogo de arquivos é gerado dos cabeçalhos `##` dos
   guias (`router_catalog.py`) e injetado no `core.md` via `{{ARQUIVOS}}`.
3. Branch por destino:
   - `none` → mensagem de fallback.
   - `tool:admins` → menções ao vivo do cargo Admin (sem LLM).
   - `wikigui.md` → `detect_pokemon()` determinístico; achou Pokémon → injeta a
     **ficha** (`species_cards/<nome>.md`) e responde; não achou → responde do
     guia da wiki.
   - `facts.md` → lista determinística (sem LLM) **ou** chamada Groq com a tool
     `filtrar_pokemon` (`pokemon_filter.py`).
   - demais guias → 1 chamada Groq respondendo só com aquele guia.
4. **Answer LLM**: 2ª chamada Groq gera o texto final.

Custo típico: **2 chamadas Groq** (router + answer).

## 3. Conteúdo

- Guias versionados (todos no git): `core.md`, `facts.md`, `faq.md`, `gacha.md`,
  `market.md`, `rules.md`, `wikigui.md`. Hoje todos flat em `content/`.
- **Subpastas de mod previstas**: vão entrar `content/<mod>/*.md` (ex.:
  `content/cobbledgacha/*.md`) com vários `.md` por mod. O index varre isso
  recursivamente (ver §7).
- `content/facts.md` (gerado pelo `build_cards`), `biome_map.md`.
- **1025 fichas** em `species_cards/` (~2.4 MB, ~800k tokens no total — grande
  demais para stuffar; alvo natural de RAG) e `species_cards_full/`.
- `card_builder/` é um **gerador offline** (JSON → `.md`). **Não muda** com este
  plano; continua produzindo as fichas que o RAG vai indexar.

## 4. Arquitetura nova (pipeline proposto)

Gates determinísticos primeiro (precisão + custo zero), RAG como **fallback
geral** (substitui o router de guias e ainda cobre busca semântica entre fichas):

```
answer(message):
  reset_usage()
  lang = detect_language(message)            # heurístico, sem LLM
  1. admins_intent(message)?      -> admins ao vivo            (sem LLM)
  2. detect_pokemon(message)?     -> ficha exata + Groq        (1 chamada)
  3. facts_intent(message)?       -> lista determinística OU filtrar_pokemon
  4. else (FALLBACK RAG):
       contexto = retriever.retrieve(message)  # top-k chunks, local, 0 token Groq
       se vazio -> fallback_message(lang)
       senão    -> Groq responde só com `contexto`  (1 chamada)
```

Ganhos:
- **Some a chamada do router LLM** (substituída por embedding local da query →
  rápido, grátis, offline). Volta a 1 chamada Groq no caminho comum.
- Pergunta aberta agora pode puxar trechos de **vários** guias (antes: 1 só).
- RAG sobre fichas cobre perguntas semânticas que os gates não pegam
  (ex.: "qual Pokémon de fogo nasce no deserto") — **o maior ganho do RAG**.

## 5. O que sai / fica / entra

**Sai (removido):**
- `modpack_bot/router.py`, `modpack_bot/router_catalog.py` — roteamento por LLM.
- `content/core.md` — era só o prompt do router.
- `tests/test_router.py`, `tests/test_router_catalog.py`.
- `ROUTER_MODELS` em `llm.py` (se nada mais usar).

**Fica (intocado ou quase):**
- `pokemon.py` (`detect_pokemon`), `facts_index.py`, `pokemon_filter.py`,
  `admins.py`, `text.py`, `prompts.py` (`build_system_prompt` etc.).
- `llm.py` (`GroqCompleter`, `ANSWER_MODELS`, path de tools).
- `card_builder/` inteiro.
- `guides.py::CardRepository` (detecção de nomes + carga de ficha) e
  `GuideRepository` (leitura de guias — agora também alimenta o build do index).

**Entra (novo):**
- `modpack_bot/retrieval.py` — Protocol `ContextRetriever` + `LlamaIndexRetriever`.
- `modpack_bot/indexing.py` — funções **puras** de chunking dos `.md`.
- `build_index.py` + `index_builder/` (ou função em `indexing.py`) — gerador
  offline do index, paralelo a `build_cards.py` (ver §14).
- `modpack_bot/intent.py` — `detect_language`, `admins_intent`, `facts_intent`.

## 6. Novos módulos e responsabilidades

### `modpack_bot/retrieval.py`
```python
class ContextRetriever(Protocol):
    def retrieve(self, query: str) -> list[str]: ...   # trechos relevantes

class LlamaIndexRetriever:
    """Carrega o index persistido uma vez; embeda a query e devolve top-k nós."""
    def __init__(self, storage_dir: str, embed_model: str, top_k: int = 4): ...
    def retrieve(self, query: str) -> list[str]: ...
```
- Espelha o padrão `ModelCompleter`: Responder depende do **Protocol**, testes
  injetam `FakeRetriever`. Nenhum outro módulo importa LlamaIndex.

### `modpack_bot/indexing.py` (puro, testável)
- `chunk_guide(text, source) -> list[Chunk]`: quebra guia por cabeçalho `##`,
  1 chunk por seção + metadata `{source, section}`.
- `chunk_card(text, pokemon) -> Chunk`: 1 chunk por ficha (já compacta),
  metadata `{source: "card", pokemon}`.
- Funções puras (string → chunks) testáveis sem modelo de embedding.

### `build_index.py` (offline) — ver §14 para o fluxo completo
- Varre o conteúdo, gera chunks, embeda, persiste em `content/index/`.
- Imprime contagem de nós, igual aos prints do `build_all`.
- Auto-build: no startup do bot, se `content/index/` não existir, builda 1x.

### `modpack_bot/intent.py` (puro)
- `detect_language(message) -> "pt"|"en"`: heurístico por stopwords (sem dep,
  sem LLM).
- `admins_intent(message) -> bool`: tokens tipo `admin/staff/moderacao/mod`.
- `facts_intent(message) -> bool`: `wants_full_list` **ou** casa algum eixo de
  `facts.md` (tipo/categoria/item) via os índices já existentes.

## 7. Embedding, chunking e descoberta de arquivos

- **Modelo:** `intfloat/multilingual-e5-small` (~470 MB, bom em PT, leve). e5
  exige prefixos `query:`/`passage:` — setar via `query_instruction` /
  `text_instruction` do `HuggingFaceEmbedding`.
- **Descoberta de arquivos (recursiva):**
  - Guias: `glob("content/**/*.md", recursive=True)` **excluindo** tudo sob
    `content/pokemons-db/` (tratado à parte) e o `core.md` (será deletado).
    → pega `content/*.md` E `content/<mod>/*.md` automaticamente. Jogar
    `content/cobbledgacha/balls.md` e rodar o build = entra, zero config.
  - Fichas: `glob("content/pokemons-db/species_cards/*.md")` (caminho dedicado;
    `species_cards_full/`, `_report.md`, `biome_map.md` ficam de fora).
- **Chunking:** guias por seção `##`; fichas = 1 nó cada (compactas).
- **Metadata por nó:** `source` = **caminho relativo** (`cobbledgacha/balls.md`,
  não só o nome) + `section`/`pokemon`. Serve pra debug e filtragem por origem.
- **Persistência:** `VectorStoreIndex` + `SimpleVectorStore` salvos via
  `StorageContext.persist("content/index/")`. Carregado 1x no construtor do
  retriever.

## 8. Idioma (decidido: heurístico)

Sem router, o idioma sai de:
- **Answer model** responde no idioma da pergunta (Groq resolve bem);
  `build_system_prompt` já tem variantes pt/en.
- **Strings de produto determinísticas** (fallback, admins, lead-in da listagem)
  usam `detect_language()` heurístico (stopwords PT vs EN). Mensagens curtas e
  fixas, heurístico simples basta.

## 9. Dependências e footprint

Adicionar a `requirements.txt` (com versões fixadas):
```
llama-index-core
llama-index-embeddings-huggingface
sentence-transformers           # puxa torch (CPU)
```
- ⚠️ **Footprint grande**: torch + modelo (~1.5–2 GB no deploy) vs deps atuais
  minúsculas. Cold start carrega o modelo de embedding na memória. Avaliar no
  ambiente de deploy (RAM/disco). Mitiga: modelo pequeno (e5-small), buildar o
  index offline (não no request).

## 10. Testes

Padrão do projeto: `pytest`, fakes nomeados, mock de I/O externo, regressão por
bug. Plano:
- `tests/test_indexing.py` — funções puras de chunking (sem modelo).
- `FakeRetriever` em `conftest.py` (devolve trechos canned), espelhando
  `FakeCompleter`.
- `tests/test_intent.py` — `detect_language`, `admins_intent`, `facts_intent`.
- `tests/test_responder.py` — reescrito pro novo pipeline (sem router; gates +
  fallback RAG via `FakeRetriever`).
- Remover `tests/test_router.py`, `tests/test_router_catalog.py`.
- Mantêm-se: `test_facts*`, `test_pokemon*`, `test_text`, `test_card`,
  `test_*` do `card_builder`.
- O `LlamaIndexRetriever` real (carrega modelo/index) **não** entra em teste
  unitário — só o Protocol é exercitado via fake; opcional 1 teste de fumaça
  marcado `@pytest.mark.slow` fora do `pytest` padrão.

## 11. Plano de migração (etapas pequenas, cada uma com testes verdes)

1. Adicionar deps e fixar versões.
2. `indexing.py` (chunking puro + descoberta recursiva de arquivos) +
   `test_indexing.py`.
3. `build_index.py` gerando `content/index/` a partir de guias + fichas.
4. `retrieval.py` (Protocol + `LlamaIndexRetriever`) + `FakeRetriever` no conftest.
5. `intent.py` (`detect_language`, `admins_intent`, `facts_intent`) + testes.
6. Reescrever `Responder` pro pipeline da §4 (gates → fallback RAG).
7. Reconfigurar `__main__.build_responder` (injeta retriever no lugar do Router).
8. Remover `router.py`, `router_catalog.py`, `core.md`, testes do router;
   limpar `ROUTER_MODELS`/`ROUTABLE_GUIDES` se órfãos.
9. Gerar o index, rodar `pytest`, smoke test manual com perguntas reais
   (market/gacha/faq/ficha/contagem/semântica).

## 12. Riscos

- **Footprint/cold start** do torch + modelo (§9).
- **Qualidade PT** do modelo pequeno — pode exigir trocar p/ `bge-m3`.
- **RAG menos preciso** que o caminho de arquivo único em perguntas factuais
  (ex.: taxa do market). Mitiga: chunk por seção `##`, top-k ajustável, gates na
  frente.
- **Index desatualizado** vs conteúdo — disciplina de rebuild (§14) ou rebuild
  no startup se ausente.
- **Teto de token do Groq free tier** (12k TPM, já citado no código) com vários
  chunks — limitar top-k e tamanho de chunk.

## 13. Decisões (todas fechadas)

1. **Idioma** (§8): **heurístico determinístico** (`detect_language` por
   stopwords, sem LLM). Answer model responde no idioma da pergunta.
2. **Indexar fichas** (§7): **sim — guias + as 1025 fichas.** Fichas no index são
   o único ganho de *capacidade* do RAG (busca semântica reversa: "pokemon de
   fogo no deserto"), que os gates determinísticos não cobrem. Custo quase nulo:
   fichas já existem como `.md`, só passam pelo mesmo embed local. Mitigar ruído
   no retrieval com top-k baixo + metadata `source` por nó.
3. **Index no git**: **gerar no deploy** (não commitar `content/index/`). O
   `build_index.py` roda 1x; auto-build no startup se a pasta não existir. Como
   o embedding é local, o modelo já está no deploy — gerar lá é barato e mantém
   o git limpo. (Difere das fichas, que SÃO commitadas porque gerá-las exige a
   fonte JSON; o index exige só os `.md` já versionados + o modelo.)
   - Adicionar `content/index/` ao `.gitignore`.
4. **Modelo de embedding**: **`intfloat/multilingual-e5-small`** (~470 MB, bom
   PT, leve). Trocar p/ `bge-m3` só se a qualidade PT decepcionar.
5. **`core.md`**: **deletar.** Era só o prompt do router; sai junto com
   `router.py`/`router_catalog.py`.

## 14. Fluxo de build (geradores offline)

Dois geradores offline, em **ordem de dependência**. Nenhum roda no request.

| Gerador | Lê | Escreve | Quando rodar |
|---|---|---|---|
| `build_cards.py` (já existe, **não muda**) | `species/*.json`, `spawn_pool_world/*.json`, `biome_map.md` | `species_cards/*.md`, `species_cards_full/*.md`, `facts.md` | mudou JSON de Pokémon / spawn / biome |
| `build_index.py` (**novo**) | `content/**/*.md` (guias, recursivo) + `species_cards/*.md` | `content/index/` (vetores) | mudou qualquer `.md`, ou logo após o `build_cards` |

`build_index.py` **consome a saída** do `build_cards.py` (as fichas). Por isso a
ordem importa: rodar o index com fichas velhas indexa dados velhos.

Cenários:
- **Mudou um JSON de Pokémon** → `python build_cards.py` → `python build_index.py`
- **Mudou/adicionou um guia `.md`** (inclusive em subpasta de mod) →
  `python build_index.py`
- **Adicionou pasta de mod** (`content/cobbledgacha/*.md`) → `python build_index.py`
  (o glob recursivo pega; nenhuma lista pra editar)
- **Deploy sem index** → o bot builda sozinho no startup (1x)

## 15. As tools (não mudam)

Continuam **as 2 que já existem**; o RAG **não é tool**.
- `filtrar_pokemon` — cruza tipo/categoria/item. Roda no gate `facts_intent` (3).
- `tool:admins` — menções ao vivo. Roda no gate `admins_intent` (1).
- **RAG** = retrieval direto no gate 4 (embeda query → top-k chunks → Groq). O
  modelo NÃO "decide chamar" o RAG; ele é o fallback. O que o RAG substitui é o
  **router LLM**, não as tools.
