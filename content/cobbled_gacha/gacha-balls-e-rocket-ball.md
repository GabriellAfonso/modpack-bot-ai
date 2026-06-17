# Gacha Balls e Rocket Ball — Cápsulas de Spawn de Pokémon

As Gacha Balls e a Rocket Ball são itens especiais que, ao serem usados, fazem um Pokémon aparecer diretamente perto do jogador. Diferente das cápsulas normais que dão itens, essas bolas spawnam criaturas do Cobblemon.

---

## Como usar

1. Segure a bola na **mão principal**
2. Clique com **botão direito** no ar
3. Um Pokémon aparece na sua posição
4. A mensagem "A wild **[Nome]** appeared!" aparece no chat
5. Se a sua party já estiver cheia (6 Pokémon), o Pokémon vai direto para o **PC**
6. A bola é consumida (1 bola = 1 Pokémon)

---

## Gacha Balls (1–6)

São 6 Gacha Balls diferentes, cada uma com seu próprio pool de Pokémon. O pool é definido pelo servidor via datapack. Por padrão, cada Gacha Ball tem alguns Pokémon de exemplo registrados.

### Gacha Ball 1 — Poké Gacha Ball
Pool padrão: Caterpie (comum), Pidgey (comum), Rattata (incomum)

### Gacha Ball 2 — Citrine Gacha Ball
Pool padrão: Caterpie (comum), Pidgey (comum), Rattata (incomum)

### Gacha Ball 3 — Verdant Gacha Ball
Pool padrão: Caterpie (comum), Pidgey (comum), Rattata (incomum)

### Gacha Ball 4 — Azure Gacha Ball
Pool padrão: Caterpie (comum), Pidgey (comum), Rattata (incomum)

### Gacha Ball 5 — Roseate Gacha Ball
Pool padrão: Caterpie (comum), Pidgey (comum), Rattata (incomum)

### Gacha Ball 6 — Slate Gacha Ball
Pool padrão: Caterpie (comum), Pidgey (comum), Rattata (incomum)

> **Nota:** Os pools padrão têm apenas alguns Pokémon de exemplo. Na prática, o servidor configura os pools com dezenas ou centenas de espécies. Pergunte aos administradores do servidor quais Pokémon estão disponíveis em cada bola.

---

## Rocket Ball

A Rocket Ball é uma bola especial temática do Team Rocket. Ela usa o pool de spawn do **rocket_ball**, que por padrão inclui Pokémon de todas as regiões (Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar, Hisui, Paldea).

**Como obter:** A Rocket Ball é obtida como recompensa do **Rocket Prize Master** (máquina 11). Neste servidor você insere uma Gacha Coin 10 (Premier Gacha Coin) na máquina e ela dispensa uma Rocket Ball.

**Ao usar:** Spawna um Pokémon do pool rocket_ball perto de você.

---

## Nível dos Pokémon spawnados

O nível de cada Pokémon é sorteado aleatoriamente dentro da faixa configurada no pool. Por exemplo:
- Caterpie: nível 1–20
- Rattata: nível 1–25

Cada espécie no pool tem um `minLevel` e `maxLevel` definidos pelo servidor.

---

## Sistema de raridade (Buckets)

Os Pokémon nos pools estão divididos em buckets de raridade. Primeiro o sistema sorteia um bucket (com base nos pesos), depois sorteia um Pokémon dentro daquele bucket.

Os buckets padrão e seus pesos:

| Bucket | Peso | Chance aproximada |
|---|---|---|
| common | 100 | ~61,7% |
| uncommon | 40 | ~24,7% |
| rare | 15 | ~9,3% |
| ultra_rare | 5 | ~3,1% |
| legendary | 1 | ~0,6% |

Pesos mais altos = mais provável de ser selecionado. Um Pokémon no bucket `legendary` tem bem menos chance de aparecer que um no `common`.

O servidor pode alterar esses pesos no `server_config.json` para balancear as chances de acordo com o servidor.

---

## Diferença entre Gacha Ball e Capsule

| | Gacha Ball / Rocket Ball | Cápsula (capsule_a1, etc.) |
|---|---|---|
| Ao usar | Spawna um Pokémon | Dá itens no inventário |
| Pokémon vai para a party? | Sim (se não estiver cheia) | N/A |
| Party cheia | Pokémon vai para o PC | N/A |
| Consumida ao usar | Sim | Sim |
