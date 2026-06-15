# Dungeons — Portais e Dimensões Especiais

## O que são Dungeons

Dungeons são dimensões temporárias e instanciadas que surgem no mundo via portais. Cada dungeon tem seu próprio ambiente, Pokémon exclusivos e recompensas. O acesso é feito através de portais que aparecem periodicamente no servidor ou usando **Dungeon Donuts** (veja a wiki de Donuts).

---

## Como os Portais Funcionam

Portais de dungeon aparecem espontaneamente no mundo:
- **Intervalo de spawn**: a cada **10 minutos (600 segundos)**
- **Vida útil do portal**: **30 minutos** — após esse tempo, o portal desaparece
- **Raio de spawn**: entre 32 e 80 blocos do jogador
- **Chance de spawn**: 100% (sempre aparece quando o intervalo se cumpre)
- **Notificação**: jogadores em um raio de **80 blocos** recebem uma notificação quando um portal aparece perto

Quando um portal aparece, uma mensagem no chat avisa os jogadores próximos.

---

## Tipos de Dungeon Disponíveis

### Underground Dungeon (`dungeon_underground`)
Dimensão subterrânea com corredores, áreas de escavação e o NPC Hiker Seller dentro. Contém:
- Pokémon de tipos subterrâneos e rochosos
- Digsites para escavação
- Oásis com itens em baús
- Acesso ao minigame de escavação underground

### Distortion Dungeon (`dungeon_distortion`)
Dimensão estilo Distortion World (referência ao Pokémon Platinum). Ambiente escuro e sombrio com:
- Pokémon do tipo Fantasma e variantes "Distortion" (modelos especiais)
- Estrutura labiríntica com arenas e plataformas
- Itens espalhados ("lost items" — itens perdidos pelo chão)
- Estrutura jigsaw gerada proceduralmente

### Portal/Jump Dungeon (`dungeon_jump`)
Dimensão de plataformas com desafios verticais. Desabilitada por padrão nas configurações base — verifique com a staff se está ativa no servidor.

---

## Timer de Dungeon

Cada dungeon tem um timer de **15 minutos (900 segundos)** por visita.

- Quando o timer expira, você é teleportado de volta para o mundo normal.
- Se você morrer dentro de uma dungeon, o timer expira imediatamente.
- Se você cair abaixo do Y=0, também é expulso automaticamente.
- A dungeon pode ser removida durante seu uso (por reset do servidor ou limpeza) — nesse caso você é evacuado automaticamente.

---

## Como Entrar nas Dungeons

**Via Portal Natural**: Encontre um portal gerado no mundo. Interaja com ele para receber um convite de teleporte. Você tem alguns segundos para aceitar antes do convite expirar.

**Via Dungeon Donut**: Consuma um Dungeon Donut do tipo correto enquanto estiver próximo ao ponto de entrada da dungeon. Isso força a entrada sem precisar de portal físico.

---

## Loot das Dungeons

### Oásis do Underground (baús normais)
Rola de **3 a 6 itens** por baú:
- Poké Ball, Great Ball, Ultra Ball (pesos: 25/15/5)
- Berries comuns: Oran, Pecha, Cheri, Sitrus
- Poções: Potion, Super Potion, Antidote, Paralyze Heal, Awakening
- Revive
- Apricorns: Red, Blue, Yellow
- Exp Candy XS, Exp Candy S

### Oásis Ominoso do Underground (baús raros)
Rola de **2 a 4 itens** por baú, loot mais raro:
- Ultra Ball (2–5x, peso 20)
- Dusk Ball, Timer Ball, Repeat Ball (1–3x, peso 15 cada)
- Quick Ball (1–2x, peso 12)
- Pedras de evolução: Fire, Water, Thunder, Leaf (peso 10), Moon, Sun (peso 9), Shiny, Dusk, Dawn, Ice (peso 8)
- Link Cable, Kings Rock, Metal Coat, Dragon Scale, Upgrade (peso 7–8)
- Prism Scale, Razor Claw, Razor Fang, Electirizer, Magmarizer, Protector, Dubious Disc, Reaper Cloth (peso 6)
- Exp Share (peso 5), Lucky Egg (peso 4)
- Rare Candy (1–2x, peso 8), Exp Candy L (1–3x, peso 10), Exp Candy XL (1–2x, peso 6)
- Ability Capsule (peso 3), Ability Patch (peso 2)

---

## Comandos de Dungeon (Admin)

- `/cobblesafari dungeon spawn` — força spawn de um portal aleatório perto de você
- `/cobblesafari dungeon spawn force [jogador] [id_dungeon]` — força spawn de dungeon específica
- `/cobblesafari dungeon list` — lista portais ativos
- `/cobblesafari dungeon list force` — escaneia e lista todos os portais
- `/cobblesafari dungeon dimensions` — lista dungeons registradas no sistema
- `/cobblesafari reset dungeon` — limpa todas as dimensões de dungeon (OP nível 4)
