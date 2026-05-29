# CobblemonWikiGui — wiki de um Pokémon pelo comando /pwiki

GUI server-side que abre uma "wiki" de um Pokémon. Aberta por **comando**, não há item nem keybind.

⚠️ Sem keybind e sem item de abertura. Só comandos.

---

## Como abrir a GUI

- **`/pwiki <species>`** — abre wiki da espécie pra si mesmo.
- **`/pwiki <species> <form>`** — abre numa forma específica.
- **`/pwikiother <player> <species> [form]`** — abre wiki pra outro jogador (precisa permissão).

Aliases de `/pwiki`: `pokewiki`, `pokemonwiki`, `cobblemonwiki`, `cobblewiki`, `cwiki`.
Aliases de `/pwikiother`: mesmos + sufixo `other` (`pokewikiother`, `cwikiother`, etc.).

Permissões: `command.pwiki`, `command.pwikianother`, `command.cwgreload`.
Admin: **`/cwg reload <arg>`** recarrega config de lang.

Navegação: dentro da wiki, slots 48/50 = Pokémon anterior/próximo por número da Pokédex; slot 49 = o Pokémon atual.

---

## O que a wiki mostra de um Pokémon (tipo, fraqueza, evolução, spawn, drops, golpes, habilidades, stats)

Tela principal. Cada item é um botão com lore. Passar o mouse pra ler a lore.

### Tela principal — botões de info direta
- **Type** — tipo(s) do Pokémon.
- **Effectiveness** — fraquezas/resistências/imunidades. Lore: "Is weak against:", "Resistant against:", "Immune against:" + tipos.
- **CatchRate** — taxa de captura em %.
- **Base Stats** — HP/Atk/Def/SpA/SpD/Speed + Friendship base.
- **Abilities** — habilidades.
- **EV Yield** — EVs concedidos ao derrotar.
- **Moves by level** — golpes por nível (`nível : golpe`).
- **TM Moves** — golpes por TM.
- **Tutor Moves** — golpes de tutor.
- **Evolution Moves** — golpes ao evoluir.
- **Form Changes Moves** — golpes por mudança de forma.
- **Egg Moves** — golpes de ovo.
- **Egg Groups** — grupos de ovo.
- **Forms** — formas disponíveis.
- **Dynamax** — pode Gigantamax? "Yes"/"Not".
- **Drops** — itens dropados + % de chance; "No Drops" se nenhum.

### Spawn Conditions (sub-tela)
Botão **Biome Spawns** ("Click to see spawn conditions"). Paginado (14/página), botão voltar no slot 0.
Mostra por spawn:
- **Conditions / Anti-Conditions**: Biomas, Moon Phase, Can See Sky, Área X/Y/Z, Light, Sky Light, Raining, Thundering, Slime Chunk, Structures, Markers.
- **Time**: faixa(s) de horário (ex. dia/noite); "Any time" se sem restrição.
- Rótulo do bucket de raridade (ex. `[common]`) no nome do botão.
- Sem spawn → "No spawn conditions found for %s".

### Evolutions (sub-tela)
Botão **Evolutions** ("Click to see evolutions"). Paginado, voltar no slot 0. Clicar numa evolução abre a wiki dela.
Lore = requisitos da evolução: Level, Friendship, held item, trade (qualquer/específico), Time of day, biome tag, structure, MoveSet/MoveType, Use move N vezes, Defeats, Blocks traveled, Recoil, Stat compare/equal, Attack/Defence ratio, Moon Phase, right-click block, "any of these requirements". Sem evolução → "No evolution found for %s".

---

## Notas para o assistente

A wiki acima descreve a **ferramenta** `/pwiki`, não os dados de cada Pokémon. Os dados por Pokémon (spawn, evolução, tipo, etc.) ficam na seção **"Dados dos Pokémon"** mais abaixo, quando existirem.

Regra de resposta, em ordem:

1. **Se a seção "Dados dos Pokémon" tiver o dado pedido** → responda **direto** com o dado e, no fim, complemente com o `/pwiki` pra mais detalhes.
   Ex.: *"O Eevee nasce em biomas de savana. Se quiser mais infos sobre ele, usa `/pwiki eevee`."*

2. **Se NÃO tiver o dado daquele Pokémon** → não invente. Diga que você não tem o dado, mas ensine o jogador a descobrir sozinho pelo `/pwiki` e o botão certo.
   Ex.: *"Não tenho onde o Eevee nasce salvo aqui, mas você descobre com `/pwiki eevee` → botão **Biome Spawns** (mostra biomas, horário, luz, clima e raridade)."*

Nunca mande só "use /pwiki" cru quando você tiver o dado — responda primeiro, indique a ferramenta depois.

⚠️ **`/pwiki` só existe pra Pokémon.** O sistema te informa numa linha `[Sistema]` se a pergunta cita um Pokémon real (e qual). Só sugira `/pwiki <nome>` com o nome confirmado nessa linha. Se o sistema disser que **nenhum Pokémon foi identificado**, NÃO invente um `/pwiki` — coisas como stronghold, vila, fortaleza, itens e blocos são do Minecraft, não Pokémon. Nesses casos, responda sobre a wiki só se a pergunta for sobre a própria ferramenta; senão, diga que não tem a info e mande pro suporte.

### Qual botão do `/pwiki` corresponde a cada pergunta (pra orientar no caso 2)

- **Onde encontro / que horas spawna** → botão **Biome Spawns** (biomas, **Time**, luz, clima, raridade).
- **Como evoluo** → botão **Evolutions** (nível, item, amizade, troca, etc.).
- **Fraqueza** → botão **Effectiveness** (Is weak against / Resistant / Immune).
- **Tipo** → botão **Type**.
- **Drops** → botão **Drops** (item + %).
- **Golpes / TMs** → botões **Moves by level**, **TM Moves**, **Tutor Moves**, **Egg Moves**.
- **Habilidades** → botão **Abilities**.
- **Stats / catch rate / EVs** → botões **Base Stats**, **CatchRate**, **EV Yield**.
- **Gigantamax?** → botão **Dynamax** (Yes/Not).
- **Formas** → botão **Forms**, ou abra direto com `/pwiki {pokemon} <form>`.
- **Abrir wiki pra outro jogador** → `/pwikiother <player> {pokemon}` (precisa `command.pwikianother`).

---

### Dados dos Pokémon

Os dados de cada Pokémon **não ficam aqui** — quando a pergunta cita um Pokémon real, o sistema entrega a **carta** daquele Pokémon (tipo, fraqueza, stats, spawn, evolução, drops, formas) num bloco próprio, e você responde direto com base nela (caso 1). Este arquivo (`wikigui.md`) só é usado quando **nenhum Pokémon** é identificado — aí vale o mapa de botões acima pra orientar `/pwiki`, ou a regra do `[Sistema]` pra recusar não-Pokémon (stronghold etc.).
