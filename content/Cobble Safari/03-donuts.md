# Donuts — Itens de Boost com Poderes Especiais

## O que são Donuts

Donuts são itens consumíveis que concedem efeitos temporários ao jogador e aos Pokémon da party. Cada donut tem um **sabor principal**, até **3 bônus de poder** e um nível de **calorias** que determina quanto tempo os efeitos duram. São craftados no Cooking Pot do Cobblemon.

---

## Como Craftar Donuts

No **Cooking Pot**, combine:
- 1x **Donut Mix** (`cobblesafari:donut_mix`)
- 1x **Butter** (tipo determina a quantidade produzida e o tier)
- Berries como tempero (flavour seasoning) — o tipo de berry determina o sabor e os poderes disponíveis

### Tipos de Butter e Quantidade Produzida

| Butter | Donuts Produzidos | Tier |
|--------|-------------------|------|
| Butter Great (`cobblesafari:butter_great`) | 2 | Médio |
| Butter Amazing (`cobblesafari:butter_amazing`) | 3 | Alto |
| Butter Supreme (`cobblesafari:butter_supreme`) | 4 | Alto |
| Butter Luminosian (`cobblesafari:butter_luminosian`) | 1 | Especial |
| Butter Hyperspace (`cobblesafari:butter_hyperspace`) | — | Usado em Dungeon Donuts |

O **tier do donut** é determinado pela soma dos níveis dos bônus inseridos via berries. Tiers mais altos têm duração base maior.

---

## Tiers de Donut e Duração

O tier determina o multiplicador de calorias (e portanto a duração dos efeitos):

| Tier | Soma dos Níveis dos Bônus | Multiplicador de Calorias |
|------|--------------------------|---------------------------|
| 0 | 0–1 | 1,5x |
| 1 | 2 | 1,4x |
| 2 | 3–4 | 1,3x |
| 3 | 5–6 | 1,2x |
| 4 | 7–8 | 1,1x |
| 5 | 9+ | 1,0x |

A duração em segundos = `calorias × 20 ticks × multiplicador`. Tiers mais baixos têm duração proporcionalmente maior.

---

## Sabores e Poderes Disponíveis

Cada donut tem um sabor principal (definido pelas berries usadas). O sabor determina quais poderes podem aparecer nos slots de bônus.

### Sabor SWEET (Doce)
- **Friendship Power** — aumenta o valor de amizade dos Pokémon na party (+50/+75/+100 pontos por nível)
- **Atypical Power** — aumenta a chance de spawns atípicos (nível 1/2/3: +1/+2/+3)
- **Sparkling Power** — aumenta a chance de shinies em spawns (nível 1/2/3: +1/+2/+3)
- **Humongo Power** — aumenta o nível dos Pokémon que aparecem (+5/+10/+15 níveis)
- **Teensy Power** — diminui o nível dos Pokémon que aparecem (-5/-10/-15 níveis)

### Sabor DRY (Seco)
- **Hidden Power** — aumenta a taxa de spawn de Pokémon com Hidden Ability (2x/3x/4x por nível)
- **Capture Power** — aumenta a taxa de captura de Pokémon (+10%/+20%/+30%)
- **Encounter Power** — aumenta a taxa de encontros com Pokémon (+10%/+25%/+50%)

### Sabor SOUR (Azedo)
- **Luck Power** — concede o atributo de Luck ao jogador (+1/+3/+5 por nível), útil para o Underground Minigame
- **Salvage Power** — concede rolls extras em saques (loot tables) (+1/+2/+3 rolls extras)

### Sabor SPICY (Picante)
- **Attack Power** — aumenta o Ataque dos Pokémon da party (+10%/+20%/+30%)
- **Sp. Atk Power** — aumenta o Ataque Especial (+10%/+20%/+30%)
- **Speed Power** — aumenta a Velocidade (+10%/+20%/+30%)
- **Move Power** — aumenta o dano dos moves (+10%/+20%/+30%)
- **Self Attack Power** — aumenta o dano que o jogador causa (+10%/+25%/+50%)

### Sabor BITTER (Amargo)
- **Defense Power** — aumenta a Defesa dos Pokémon da party (+10%/+20%/+30%)
- **Sp. Def Power** — aumenta a Defesa Especial (+10%/+20%/+30%)
- **Resistance Power** — reduz o dano recebido pelos Pokémon da party (-10%/-20%/-30%)
- **Self Defense Power** — reduz o dano recebido pelo jogador (-10%/-25%/-50%)

---

## Dungeon Donuts

Dungeon Donuts são itens especiais usados para entrar em dimensões de Dungeon. Não têm poderes de stat — são "chaves" consumíveis.

### Recipes de Dungeon Donuts

Todos no Cooking Pot com: `donut_mix + butter_hyperspace + ingredient_dungeon_X`

| Resultado | Ingrediente Especial | Dimensão Acessada |
|-----------|---------------------|-------------------|
| Donut Dungeon Distortion | `ingredient_dungeon_distortion` | Distortion World |
| Donut Dungeon Underground | `ingredient_dungeon_underground` | Underground |
| Donut Dungeon Portal | `ingredient_dungeon_portal` | Dungeon Jump |
| Donut Dungeon Paris | `ingredient_dungeon_paris` | (variante especial) |

Os ingredientes de dungeon (`ingredient_dungeon_X`) são encontrados dentro das próprias dungeons ou em drops especiais.

---

## Comandos de Donut (Admin)

Apenas operadores podem criar donuts via comando:

- `/donut random <sabor> <tier> <quantidade>` — gera um donut aleatório com o sabor e tier especificados
- `/donut custom <bonus1> <bonus2> <bonus3> <quantidade>` — cria donut com bônus específicos no formato `poder:nivel:tipo`

Os sabores válidos para o comando são os nomes em inglês: `sweet`, `dry`, `sour`, `spicy`, `bitter`.
