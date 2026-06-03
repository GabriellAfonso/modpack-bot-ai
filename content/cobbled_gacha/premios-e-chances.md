# Prêmios e Chances — Configuração de Override do Servidor

Este documento descreve **o que cada máquina gacha entrega** e **com que probabilidade**, conforme a configuração de override aplicada neste servidor (datapack `cobbledgacha_override`). O mod base permanece intacto; os valores abaixo refletem as tabelas de loot e o `server_config.json` do override, que têm prioridade sobre os arquivos originais do mod.

> Para a referência bruta de todos os drops do mod (incluindo cápsulas e máquinas não alteradas), veja `DROPS-REFERENCIA.md`. Este arquivo foca apenas no que o override define como ativo.

---

## Como a probabilidade funciona

Cada item dentro de um pool tem um **peso** (`weight`). A chance de um item sair é:

```
chance = peso do item ÷ soma dos pesos do pool
```

- Item sem peso definido conta como peso **1**.
- `rolls` indica quantos sorteios o pool faz por abertura/giro. Se `rolls = 1`, sai 1 item; se for um intervalo (ex: 1–5), sai uma quantidade aleatória nesse intervalo.
- `set_count` (a "quantidade" ao lado de cada item) define **quantas unidades** daquele item vêm quando ele é sorteado — não afeta a chance, só o tamanho do prêmio.

---

## Custo por giro de cada máquina (override)

Definido em `server_config.json`. Valor = quantidade de moeda exigida por giro.

| Máquina | Custo (moedas) | O que entrega |
|---|---|---|
| gacha_machine_1 (Poké Gacha) | 5 | Cápsulas grupo A |
| gacha_machine_2 | 20 | Itens diretos (bolas, sweets, held items) |
| gacha_machine_3 | 10 | Itens diretos (loja grande) |
| gacha_machine_4 | 1 | Spawner (tipo `spawner`) |
| gacha_machine_11 (Rocket) | 1 | Rocket Ball |
| gacha_machine_12 (Plush-O-Matic) | 3 | Pokédolls (tipo `specific`) |

Flags globais do override: `pickup: false`, `automation: false`, `gacha_machine_4_type: spawner`, `gacha_machine_12_type: specific`.

Buckets de raridade (usados por máquinas que spawnam Pokémon): `common: 100`, `uncommon: 40`, `rare: 15`, `ultra_rare: 5`, `legendary: 1`.

---

## Máquina 1 (Poké Gacha) → qual cápsula sai

A máquina 1 custa 5 moedas e dispensa uma cápsula do grupo A. Distribuição (`rolls = 1`):

| Cápsula | Tier | Peso | Chance |
|---|---|---|---|
| capsule_a1 (Poké Capsule) | comum | 51 | ~51% |
| capsule_a2 (Great Capsule) | médio | 24 | ~24% |
| capsule_a3 (Ultra Capsule) | alto | 15 | ~15% |
| capsule_a4 (Master Capsule) | muito alto | 7 | ~7% |
| capsule_a5 (Cherish Capsule) | topo | 3 | ~3% |

A cápsula é um item: segure na mão e use (botão direito no ar) para abrir e receber o conteúdo. O conteúdo de cada tier está descrito abaixo.

---

## Conteúdo das cápsulas (chance de cada item ao abrir)

Todas as cápsulas abrem com `rolls = 1` (1 item por abertura).

### capsule_a3 — Ultra Capsule (~15% da máquina 1)

198 itens, **todos com peso 1** → chance igual de **~0,505% por item**.

Categorias presentes (quantidade entre parênteses = `set_count`):
- **Type gems** (3 un): bug, dark, dragon, electric, fairy, fighting, fire, flying, ghost, grass, ground, ice, normal, poison, psychic, rock, steel, water
- **Fósseis** (1 un): armor, claw, cover, dome, helix, jaw, old_amber, plume, root, sail, skull + fossilized_bird/dino/drake/fish
- **Gilded chests** (2 un): black, blue, green, pink, white, yellow, regular
- **Pokédex** (1 un): black, blue, green, pink, red, white, yellow
- **Mints** (6 un): lista completa de naturezas (adamant, bold, brave, calm, careful, gentle, hasty, impish, jolly, lax, lonely, mild, modest, naive, naughty, quiet, rash, relaxed, sassy, serious, timid)
- **Vitaminas** (4 un): calcium, carbos, hp_up, iron, protein, zinc, pp_max, pp_up
- **Exp candy**: m (20 un), l (10 un), xl (5 un)
- **Rods**: variantes normais (great, poke, premier, ultra) + ancient (1 un)
- **Bolas** (3 un): dusk, love, luxury, quick, repeat, safari, sport, timer, ultra + ancient balls
- **X items** (6 un): x_accuracy, x_attack, x_defence, x_special_attack, x_special_defence, x_speed
- **Sherds** (7 un): bygone, capture, dome, helix, nostalgic, suspicious
- **Tumblestones** (12 e 15 un): black, sky, regular
- **Materiais evolutivos** (2 un): black_augurite, deep_sea_scale/tooth, dragon_scale, dubious_disc, electirizer, galarica_cuff/wreath, magmarizer, oval_stone, peat_block, prism_scale, protector, reaper_cloth, upgrade, link_cable, etc.
- **Pedras evolutivas** (5 un): dawn, dusk, fire, ice, leaf, moon, shiny, sun, thunder, water
- **Restauros/curas**: full_restore (3), max_elixir/ether/revive (3), revive (8), super_potion (5), hyper_potion (5)
- **Power items** (2 un): anklet, band, belt, bracer, lens, weight, herb
- **gacha_coin** (30 un)
- Diversos: ability_capsule/patch (3), big_root, kings_rock, mental_herb, soothe_bell, lucky_egg, exp_share, vivichoke, energy_root, e itens de comida Pokémon (apples, teacups, pots)

> Duplicatas conhecidas no arquivo (contam como entradas separadas, aumentando levemente a chance dessas linhas): black_tumblestone, sky_tumblestone, tumblestone (12 e 15), power_herb (2 e 3).

### capsule_a4 — Master Capsule (~7% da máquina 1)

95 itens. Soma dos pesos = **887**.
- **88 itens "padrão" com peso 10** → **~1,13% cada**
- **7 smartphones com peso 1** → **~0,11% cada** (os itens mais raros desta cápsula)

**Esta cápsula NÃO contém Master Ball** — apesar do nome "Master Capsule". A única cápsula com Master Ball é a Cherish Capsule (capsule_a5). A Master Ball aqui não existe.

Itens peso 10 (1 un salvo indicado):
- Destaques: beast_ball (3), dream_ball (3), dream_rod (1)
- **Stone blocks** (1 un): dawn, dusk, fire, ice, leaf, moon, shiny, sun, thunder, water
- **Todos os rods** (1 un): great, dive, dusk, fast, friend, level, love, lure, luxury, moon, nest, net, park, quick, repeat, sport, timer, heavy + ancient (feather, gigaton, heavy, leaden, wing)
- **Fósseis** (3 un): armor, claw, cover, dome, helix, jaw, old_amber, plume, root, sail, skull + fossilized_bird/dino/drake/fish
- **Gilded chests** (4 un): black, blue, green, pink, white, yellow + regular (3)
- **Vitaminas** (7 un): calcium, carbos, hp_up, iron, protein, zinc, pp_max, pp_up
- **Exp candy**: l (20 un), xl (10 un)
- **rare_candy** (8 un), **gacha_coin** (60 un)
- **Restauros grandes**: max_elixir (10), max_ether (10), max_potion (15), max_revive (6), full_restore (6)
- **Utilitários** (2 un): healing_machine, monitor, pasture, pc, restoration_tank, fossil_analyzer
- ability_capsule/patch (7), exp_share (4), lucky_egg (6), superb_remedy (7)

Smartphones peso 1 (raros, 1 un): white, red, black, blue, purple, pink, gray (`cobblemon_smartphone:*_smartphone`)

> Duplicatas no arquivo: helix_fossil, jaw_fossil (aparecem 2×).

### capsule_a5 — Cherish Capsule (~3% da máquina 1, a mais rara)

**Esta é a ÚNICA cápsula que contém Master Ball** (1 unidade, peso 1). Nenhuma outra cápsula a entrega. Chance total de tirar uma Master Ball: ~3% (sair a Cherish Capsule da máquina 1) × ~4,17% (sair a Master Ball dentro dela) ≈ **0,125%** por giro da máquina 1.

24 itens, **todos com peso 1** → chance igual de **~4,17% por item**. Tier topo: quantidades altas.

| Item | Quantidade |
|---|---|
| ability_capsule | 15 |
| ability_patch | 15 |
| ancient_origin_ball | 3 |
| ancient_origin_rod | 1 |
| beast_rod | 1 |
| calcium | 16 |
| carbos | 16 |
| cherish_ball | 3 |
| cherish_rod | 1 |
| exp_candy_xl | 30 |
| full_restore | 15 |
| hp_up | 16 |
| iron | 16 |
| master_ball | 1 |
| master_rod | 1 |
| max_elixir | 15 |
| max_ether | 15 |
| max_revive | 15 |
| pp_max | 16 |
| pp_up | 16 |
| protein | 16 |
| rare_candy | 10 |
| gacha_coin | 150 |
| zinc | 16 |

---

## Máquina 2 → itens diretos (sem cápsula)

Custo 20 moedas. Não dá cápsula — entrega itens direto. `rolls = 1 a 5` (média ~3 itens por giro). 103 itens, soma dos pesos = **2320**.

Chance por item = peso ÷ 2320, **por sorteio** (e há de 1 a 5 sorteios por giro).

| Peso | Chance/sorteio | Itens |
|---|---|---|
| 80 | ~3,45% cada | bolas básicas: azure, citrine, poke, premier, roseate, slate, verdant |
| 60 | ~2,59% cada | ancient balls: azure, citrine, ivory, roseate, slate, verdant |
| 40 | ~1,72% cada | great_ball, heal_ball |
| 35 | ~1,51% cada | ancient_feather_ball, ancient_great_ball, ancient_heavy_ball |
| 25 | ~1,08% cada | dive_ball, dusk_ball, nest_ball, net_ball + sweets (berry, clover, flower, love, ribbon, star, strawberry) |
| 20 | ~0,86% cada | quick_ball, repeat_ball, timer_ball, ultra_ball, cracked_pot, whipped_dream |
| 15 | ~0,65% cada | held items diversos (rocky_helmet, quick_powder, oval_stone, etc.) + ancient balls (gigaton, jet, leaden, ultra, wing) |
| 10 | ~0,43% cada | held items/bolas menores (luxury_ball, friend_ball, fast_ball, heavy_ball, eviolite, kings_rock, etc.) + ability_capsule, pp_up, rare materiais |
| 5 | ~0,22% | rare_candy (item mais raro da máquina 2) |

---

## Máquina 12 (Plush-O-Matic) → Pokédolls

Custo 3 moedas. Tipo `specific`. **No override, a tabela `gacha_machine_12_fantasy_yarn` foi expandida para conter TODOS os pokémon** (não apenas os 4 do tema "fantasy" original). 288 entradas = 72 pokémon × 4 variantes. `rolls = 1`. Soma dos pesos = **2584**.

Cada pokémon tem 4 variantes com pesos fixos:

| Variante | Peso | Chance global | Chance relativa (dentro do mesmo pokémon) |
|---|---|---|---|
| pokedoll_X (normal) | 20 | ~0,77% | 55,6% |
| gigantic_pokedoll_X | 10 | ~0,39% | 27,8% |
| pokedoll_shiny_X | 4 | ~0,15% | 11,1% |
| gigantic_pokedoll_shiny_X | 2 | ~0,08% | 5,6% (mais raro) |

Os 72 pokémon disponíveis (namespace `pokeblocks:`): trevenant, absol, drifloon, gastly, gengar, gholdengo, marshadow, marshadow_zenith, netherite_gholdengo, palossand, phantump, pumpkaboo, sableye, sandygast, mimikyu, rellor, rabsca, happiny, corviknight, corvisquire, rookidee, rowlet, tropius, delibird, charmander, beartic, cetoddle, cubchoo, cubchoo_animated, eiscue, eiscue_noice, frigibax, froslass, glalie, piloswine, snorunt, snorunt_family, spheal, swinub, arboliva, bellossom, bulbasaur, bulbasaur_posed, calyrex, calyrex_animated, dolliv, ivysaur, smoliv, treecko, venusaur, riolu, stonjourner, eevee, furret, lickitung, munchlax, sentret, snorlax, blastoise, cloyster, kyogre, luvdisc, quagsire, shellder, squirtle, wailmer, wailord, wartortle, wooper, ampharos, flaaffy, mareep.

> Anomalias na tabela: piloswine não tem a variante `gigantic_pokedoll` (só 3 variantes); existe uma entrada extra `gigantic_shiny_eiscue_head_pile` (peso 2). Por isso a contagem de pesos é 72×20 + 71×10 + 72×4 + 73×2 = 2584.

---

## Moeda dos prêmios: `gacha_coin`

No override, **todas as cápsulas que antes davam `cobblemon:relic_coin` agora dão `cobbledgacha:gacha_coin`** (a moeda própria do mod). Quantidades: capsule_a3 = 30, capsule_a4 = 60, capsule_a5 = 150. Isso fecha o ciclo: abrir cápsulas devolve moedas para girar de novo.

---

## Resumo das mudanças do override vs. mod base

| Item alterado | Antes (mod) | Depois (override) |
|---|---|---|
| Custo máquina 3 | 20 | 10 |
| Custo máquina 4 | 5 | 1 |
| Moeda em cápsulas a3/a4/a5 | relic_coin | gacha_coin |
| capsule_a4 | 89 itens, pesos iguais | 95 itens, peso 10 (padrão) + 7 smartphones peso 1 |
| gacha_machine_12_fantasy_yarn | 16 entradas (4 pokémon do tema) | 288 entradas (todos os 72 pokémon) |
| gacha_machine_2 | (igual) | inalterada, incluída no override |

As demais máquinas e cápsulas (a1, a2, máquina 1, máquina 11 Rocket, etc.) seguem os valores padrão do mod, documentados em `DROPS-REFERENCIA.md`.
