# Tasks: migração RAG com LlamaIndex

Checklist executável derivado do `plan.md`. Cada fase deixa os testes verdes
(`pytest`) antes de avançar. Marcar `[x]` ao concluir.

Convenções do projeto (CLAUDE.md): funções 4-20 linhas, arquivos < 500 linhas,
sem `any`/`Dict`, early returns, todo código em inglês (strings de produto pt/en
ok), 1 teste por função nova, fakes nomeados, `pytest` único comando.

---

## Fase 0 — Baseline
- [x] Rodar `pytest` e confirmar tudo verde antes de mexer (linha de base). → 148 passed
- [x] Criar branch a partir de `dev` (não trabalhar direto na `master`). → feat/rag-migration

## Fase 1 — Dependências (§9)
- [x] Adicionar a `requirements.txt`, com versões fixadas:
      `llama-index-core==0.14.22`, `llama-index-embeddings-huggingface==0.7.0`,
      `sentence-transformers==5.5.1`. Torch pinado CPU-only (`torch==2.12.0+cpu`
      via `--extra-index-url .../whl/cpu`): default puxava build CUDA (+3.4 GB
      inúteis). Honra §9 ("torch CPU").
- [x] `pip install -r requirements.txt`; footprint medido: **1.7 GB**
      site-packages (era 5.5 GB com CUDA). + modelo e5-small ~470 MB no 1º build
      ⇒ ~2.2 GB runtime. Dentro da estimativa §9 (1.5–2 GB). Risco deploy OK.
- [x] `pytest` ainda verde (deps não quebram import). → 148 passed

## Fase 2 — Chunking puro (§6 indexing.py, §7)
- [x] `modpack_bot/indexing.py`:
  - [x] tipo `Chunk` (frozen dataclass: `text`, `source`, `section`/`pokemon`
        explícitos — sem Dict).
  - [x] `chunk_guide(text, source) -> list[Chunk]` — split por `## ` heading,
        1 chunk/seção (preâmbulo vira chunk próprio), heading fica no texto.
  - [x] `chunk_card(text, pokemon) -> Chunk` — 1 chunk, `source="card"`.
  - [x] `discover_guides(content_dir) -> list[path]` — `glob **/*.md` recursivo,
        excluir `pokemons-db/` e `core.md`.
  - [x] `discover_cards(content_dir) -> list[path]` — `species_cards/*.md`.
  - [x] extras puros p/ Fase 3: `guide_source` (path relativo, forward slashes)
        e `card_pokemon` (stem do arquivo).
- [x] `tests/test_indexing.py` — chunking + descoberta (fixtures de string e
      tmp_path; SEM modelo de embedding). + doctests.
- [x] `pytest` verde. → 157 passed

## Fase 3 — Build do index offline (§6 build_index.py, §14)
- [x] `build_index.py` (shim) + lógica em `index_builder/`:
      `nodes.py` (collect_chunks/node_metadata, puro, SEM torch) + `build.py`
      (embed+persist). Embedding centralizado em `modpack_bot/embedding.py`
      (build offline + retriever Fase 4 usam o mesmo modelo/prefixos).
  - [x] Ler guias (`discover_guides`) + fichas (`discover_cards`) → chunks.
  - [x] Embeddar com `HuggingFaceEmbedding(multilingual-e5-small)` + prefixos
        `query:`/`passage:` (`query_instruction`/`text_instruction`).
  - [x] `VectorStoreIndex` → `storage_context.persist("content/index/")`.
  - [x] Print contagem de nós. → "Indexed 1170 nodes" (1025 fichas + ~145 seções).
- [x] Adicionar `content/index/` ao `.gitignore`. → `git check-ignore` confirma.
- [x] Rodar `python build_index.py`; `content/index/*.json` gerado (12M, ~4min CPU).
- [~] Smoke test `@pytest.mark.slow`: pulado — build manual já valida; teste de
      ~4min (carrega modelo) não compensa no fluxo `pytest` rápido.
- [x] `pytest` verde. → 160 passed (1.2s, torch fora dos testes)

## Fase 4 — Retriever (§6 retrieval.py)
- [x] `modpack_bot/retrieval.py`:
  - [x] `ContextRetriever` (Protocol): `retrieve(query) -> list[str]`.
  - [x] `LlamaIndexRetriever(storage_dir, embed_model, top_k=4)` — carrega index
        1x (`load_index_from_storage`), embeda query, devolve top-k textos. Único
        módulo runtime que importa LlamaIndex.
- [x] `FakeRetriever` em `tests/conftest.py` (trechos canned), espelhando
      `FakeCompleter`.
- [x] `pytest` verde (fake exercitado; retriever real só em smoke `@slow`,
      deselecionado por padrão — pytest.ini `addopts -m "not slow"`, import pesado
      dentro da função). → 161 passed/1 deselected (1.2s); `-m slow` passa (20s,
      acha passagem do market).

## Fase 5 — Intent / idioma (§6 intent.py, §8)
- [x] `modpack_bot/intent.py`:
  - [x] `detect_language(message) -> "pt"|"en"` — heurístico por stopwords
        distintivas (disjuntas), empate → pt.
  - [x] `admins_intent(message) -> bool` — tokens admin/adm/staff/moderacao/
        moderador/moderator/**mod/mods** (mod/mods incluídos: decisão confirmada
        durante o build — seguir §6 literal).
  - [x] `facts_intent(message, facts) -> bool` — **só** casa eixo de facts
        (tipo/categoria/item) via `matched_facts_lines`. Decisão confirmada:
        `wants_full_list` isolado NÃO dispara (evita "quais comandos" virar
        facts); desvia do "OU" do §6 de propósito.
- [x] `tests/test_intent.py` — casos pt/en, positivos e negativos por função.
- [x] `pytest` verde. → 170 passed

## Fase 6 — Reescrever Responder (§4)
- [x] `Responder.__init__` recebe `retriever: ContextRetriever` no lugar do
      `Router`; mantém `completer`, `guides` (lê facts.md), `cards`, `admins`,
      `show_usage`.
- [x] `answer()`: pipeline de gates da §4:
  1. `admins_intent` → `_answer_admins`
  2. `detect_pokemon` → ficha exata + Groq
  3. `facts_intent` → listing determinístico OU `filtrar_pokemon`
  4. else → `retriever.retrieve` → vazio? fallback : Groq sobre contexto
- [x] Idioma via `detect_language` (não mais do router).
- [x] Reescrever `tests/test_responder.py` pro novo pipeline (gates + RAG via
      `FakeRetriever`); sem `route_reply`. Asserts atualizados: caminho comum 1
      chamada (não 2), listing/admins 0 chamadas.
- [x] Imports pesados (llama_index/torch) tornados **lazy** em `retrieval.py` e
      `embedding.py` — Responder depende só do Protocol e fica torch-free
      (suite 1.2s, não 6.9s).
- [x] `pytest` verde. → 169 passed (1.2s); `-m slow` ok.

## Fase 7 — Wiring (§6 __main__)
- [x] `__main__.build_responder`: instancia `LlamaIndexRetriever`, injeta no
      `Responder`. Router removido do wiring. `GuideRepository` MANTIDO (não é
      órfão: Responder lê facts.md por ele). CardRepository fica.
- [x] Auto-build: `_load_retriever` chama `build_index` se `index_dir` ausente.
- [x] Settings novas: `index_dir`/`embed_model`/`top_k` (env INDEX_DIR/
      EMBED_MODEL/TOP_K) em config.py.
- [x] Smoke end-to-end (retriever real + FakeCompleter, sem Groq): admins=0
      chamadas verbatim; pikachu→ficha+/pwiki; fogo→counts-header (tool);
      market/gacha→RAG guia; "fogo no deserto"→RAG **fichas** (Gouging Fire,
      Delphox). `python bot.py` completo fica pra deploy (precisa de secrets).

## Fase 8 — Limpeza (§5)
- [x] Deletar `modpack_bot/router.py`, `modpack_bot/router_catalog.py`.
- [x] Deletar `content/core.md`.
- [x] Deletar `tests/test_router.py`, `tests/test_router_catalog.py`.
- [x] Remover `ROUTER_MODELS` de `llm.py` (só conftest/router usavam);
      `ROUTABLE_GUIDES`/`VALID_GUIDES` removidos de `guides.py` (órfãos).
      `GuideRepository` simplificado (só `load_guide`; `load_core` removido).
      `TOOL_ADMINS` removido de `admins.py` (só o router usava).
- [x] Atualizar `conftest.py`: removido import `ROUTER_MODELS`, `FakeCompleter`
      sem distinção router/answer, `FakeGuideRepository` sem `load_core`.
- [x] `grep` por refs mortas (router/core.md/ROUTER_MODELS/etc.) → nenhuma.
- [~] `non_pokemon_instruction` (prompts.py): agora órfão em runtime (caminho
      wiki-sem-pokemon virou RAG) mas mantido — fora do escopo de limpeza do §8;
      ainda tem teste. Candidato a remoção futura.
- [x] `pytest` verde. → 155 passed (1.3s)

## Fase 9 — Validação final (§11.9)
- [x] `python build_cards.py` && `python build_index.py` (cadeia completa). →
      cards sem diff (gerador intacto), 1170 nós reindexados.
- [x] `pytest` verde, suite inteira. → 157 passed (1 deselected).
- [x] **Bug achado e corrigido (rule a/b):** facts_intent (eixo) interceptava
      "fogo no deserto" antes do RAG e o filtro não tem bioma → resposta errada.
      Fix confirmado: facts_intent = cue contagem/lista **E** eixo. +2 regressões.
- [x] Smoke test manual de cada caminho (retriever real, gate verificado):
  - [x] market ("tem taxa?") → RAG guia (topk: "Compra, Imposto e Economia")
  - [x] gacha ("o que dá a cherish capsule?") → RAG guia ("Como usar uma cápsula")
  - [x] faq ("qual o ip?") → RAG guia ("FAQ — Informações do Servidor")
  - [x] ficha ("onde nasce pikachu?") → gate detect_pokemon
  - [x] contagem ("quantos de fogo?") → gate facts/filter
  - [x] semântica ("pokemon de fogo que nasce no deserto") → RAG **ficha**
        (topk: Gouging Fire, Fogo) — ganho-estrela do RAG funcionando
  - [x] admins ("como falo com admin?") → gate admins (0 Groq, verbatim)
- [x] Token usage: caminho comum 1 chamada Groq (não 2). Validado por
      `test_usage_footer_shows_single_groq_call` (15 tokens). Texto final das
      respostas precisa de GROQ_API_KEY no deploy.

## Fase 10 — Docs / commit
- [x] Atualizar docstrings que citem o router: `llm.py` (pipeline = answer+tools,
      não router+answer), `indexing.py` (core.md "removed", não "soon-deleted").
      Sem README no repo.
- [x] Atualizar `.env.example` com envs novas opcionais: `INDEX_DIR`,
      `EMBED_MODEL`, `TOP_K` (com defaults documentados).
- [ ] Commits lógicos por fase (skill git-commit), não tudo num só.
      → AGUARDANDO o usuário pedir (regra: não commitar até pedir).

---

## Pendências / riscos a vigiar (§12)
- Footprint torch+modelo no deploy (medir na Fase 1).
- Qualidade PT do e5-small — se ruim, trocar p/ `bge-m3`.
- Ruído no retrieval (fichas competindo com guias) — ajustar top-k / filtrar por
  `source`.
- Teto 12k TPM do Groq free — limitar top-k e tamanho de chunk.
