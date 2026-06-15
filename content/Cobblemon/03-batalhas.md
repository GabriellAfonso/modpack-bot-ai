# Batalhas — Sistema de Combate

O Cobblemon usa o sistema de batalha por turnos dos jogos Pokémon originais. Toda batalha roda no simulador Showdown integrado ao mod.

---

## Batalha Selvagem

- Clique com botão direito num Pokémon selvagem para iniciar batalha, ou ele ataca você automaticamente.
- A cada turno: escolha um **golpe**, **troque de Pokémon**, **use item** ou tente **fugir**.
- Distância máxima para iniciar batalha selvagem: **12 blocos**.

---

## Batalha PvP (Jogador vs Jogador)

- Distância máxima para desafiar outro jogador: **32 blocos**.
- Use `/pokebattle <jogador>` ou interaja com ele segurando uma Pokébola.
- Ambos precisam aceitar.
- Espectadores podem assistir a até **128 blocos** de distância.
- Troca máxima para batalha: **12 blocos** de distância do Pokémon selvagem (PvP vai até 32).

---

## Ações por Turno

- **Atacar** — escolha 1 dos até 4 golpes do Pokémon ativo.
- **Trocar** — envie outro Pokémon da equipe.
- **Item** — use poção, Pokébola, etc. (gasta o turno).
- **Fugir** — só funciona contra selvagens.

---

## Efetividade de Tipos

Funciona igual aos jogos oficiais:
- **2x (superefetivo)** — tipo atacante forte contra o tipo do defensor.
- **0,5x (resistente)** — tipo atacante fraco contra o tipo do defensor.
- **0x (imune)** — defensor imune ao tipo do atacante.
- Pokémon com dois tipos acumulam as multiplicações (pode chegar a 4x ou 0,25x).

---

## Experiência e Drop

- Pokémon ganham XP ao derrotar inimigos em batalha.
- **Lucky Egg** multiplicador: **1,5x** de XP.
- Multiplicador base do servidor: **1x** (sem bônus extra).
- XP de PvP está habilitado.
- Pokémon derrotados podem **dropar itens** — o drop aparece no mundo onde o Pokémon estava.

---

## Dano de Jogador em Pokémon

Jogadores podem atacar Pokémon com armas do Minecraft e causar dano diretamente. Útil para enfraquecer antes de capturar, mas cuidado para não matar.

---

## Status de Batalha

Golpes podem aplicar status negativos:
- **Veneno / Veneno Grave** — dano por turno crescente.
- **Queimadura** — dano por turno + reduz Ataque físico.
- **Paralisia** — pode perder o turno + reduz Velocidade.
- **Sono** — fica sem agir por vários turnos.
- **Congelamento** — fica sem agir (pode descongelar ao receber golpe de Fogo).

Fora de batalha, todos os status duram entre **3 e 5 minutos** e somem sozinhos.
