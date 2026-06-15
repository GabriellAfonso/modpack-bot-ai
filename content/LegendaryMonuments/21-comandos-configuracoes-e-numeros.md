# Comandos, Configurações e Números Importantes

## Comandos

O mod Legendary Monuments **não adiciona comandos próprios para o jogador** (não há comandos do tipo `/legendarymonuments ...`). Toda a interação é feita por itens, blocos e pelo Arc Phone. As funções como localizar estruturas, curar a equipe, abrir PC/baú e ver progresso são acessadas pelo **Arc Phone** e pelos blocos do mod, não por comandos digitados.

(Internamente o mod usa o sistema de comandos do servidor apenas para gerar efeitos de partícula durante invocações; isso é automático e não é algo que o jogador digite.)

## Configuração dos itens dos pedestais

A única configuração editável fica em `config/LegendaryMonuments/pedestals.json`, gerada automaticamente na primeira execução. Ela define qual item cada pedestal aceita. Valores padrão:

- `entei_pedestal_item` = `legendarymonuments:entei_treat`
- `raikou_pedestal_item` = `legendarymonuments:raikou_treat`
- `suicune_pedestal_item` = `legendarymonuments:suicune_treat`
- `heatran_pedestal_item` = `legendarymonuments:magma_stone`
- `hooh_pedestal_item` = `legendarymonuments:rainbow_feather`
- `latias_pedestal_item` = `legendarymonuments:latias_treat`
- `latios_pedestal_item` = `legendarymonuments:latios_treat`
- `lugia_pedestal_item` = `legendarymonuments:vortex_stone`
- `hoopa_pedestal_first_item` = `legendarymonuments:temple_key`
- `hoopa_pedestal_second_item` = `mega_showdown:prison_bottle`
- `zekrom_pedestal_first_item` = `legendarymonuments:darkstone`
- `zekrom_pedestal_second_item` = `cobblemon:electric_gem`
- `reshiram_pedestal_first_item` = `legendarymonuments:lightstone`
- `reshiram_pedestal_second_item` = `cobblemon:fire_gem`
- `kyurem_pedestal_first_item` = `legendarymonuments:truthbottle`
- `kyurem_pedestal_second_item` = `legendarymonuments:idealsbottle`
- `zacian_pedestal_first_item` = `minecraft:totem_of_undying`
- `zacian_pedestal_second_item` = `mega_showdown:rusted_sword`
- `zamazenta_pedestal_first_item` = `minecraft:totem_of_undying`
- `zamazenta_pedestal_second_item` = `mega_showdown:rusted_shield`

Efeito: alterar um valor muda qual item aquele pedestal passa a aceitar para invocar o lendário. O resto da mecânica (consumo, uso único por jogador, recompensa) não muda.

## Bloco Santuário (configuração em jogo)

O Bloco Santuário tem ajustes feitos pela sua tela de configuração (não por arquivo): proteção contra explosão, colocação de blocos, quebra de blocos e geração de monstros (cada um liga/desliga), além do raio (padrão **50 blocos**, horizontal e vertical). Veja o arquivo do Bloco Santuário.

## Números e constantes importantes do mod

Valores fixos que ditam a progressão:

- **Chance de Shiny**: 2% para praticamente todos os lendários invocados pelo mod.
- **IVs garantidos**: todo lendário invocado nasce com pelo menos 3 IVs perfeitos.
- **Pegadas (Espadas da Justiça)**: 50 pegadas do mesmo tipo para invocar Terrakion, Cobalion ou Virizion.
- **Pó Cósmico (Cosmog)**: 50 partículas (coletadas com o Catalisador Cósmico) para invocar Cosmog.
- **Estacas/Santuários (Tesouros da Ruína)**: 8 estacas enfraquecidas do mesmo tipo para ativar o santuário correspondente.
- **Urnas normais**: 50 de progresso (Pokémon do tipo certo derrotados) para encher.
- **Urnas galarianas**: 75 de progresso para encher.
- **Casulo de Eternatus**: 500 Partículas de Galar consumidas para libertar Eternatus.
- **Caixa de Meltan**: 50 de "valor em metais" depositado para invocar Meltan.
- **Aplicativo Heal do Arc Phone**: 600 segundos (10 minutos) de recarga entre curas; não funciona em batalha.
- **Fio dos Sonhos**: 10% de chance de cair ao derrotar Pokémon selvagem à noite (a até 32 blocos).
- **Detecção de abate para urnas e drops**: o Pokémon selvagem derrotado precisa estar a até 32 blocos de você.

## Níveis dos lendários invocados

Níveis em que cada lendário nasce ao ser invocado pelo mod:

- Nível 40: Entei, Raikou, Suicune, Mew, Terrakion/Cobalion/Virizion, Celebi.
- Nível 5: Cosmog, Meltan.
- Nível 50: Heatran, Latias/Latios, Mesprit/Azelf/Uxie, Keldeo, Cresselia, Darkrai, Chi-Yu e os Tesouros da Ruína; aves lendárias galarianas.
- Nível 40: aves lendárias normais (Articuno/Zapdos/Moltres).
- Nível 60: Lugia, Ho-Oh, Victini, Reshiram/Zekrom/Kyurem, Zacian/Zamazenta/Hoopa.
- Nível 70: Palkia, Dialga, Giratina, Eternatus, os Regis e Regigigas.
- Nível 90: Arceus.
