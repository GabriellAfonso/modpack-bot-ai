# Configuração do Mega Showdown

O mod cria um arquivo de configuração em `config/mega_showdown/config.json` na pasta do jogo/servidor. Você edita esse arquivo e aplica as mudanças com o comando `/msd reload` (ou reiniciando). Abaixo estão as opções, com o valor padrão e o efeito de cada uma.

## Ligar/desligar sistemas inteiros

- **`mega`** (padrão: ligado) — liga ou desliga todo o sistema de Mega Evolução.
- **`zMoves`** (padrão: ligado) — liga ou desliga todo o sistema de Movimentos Z (e, por consequência, o Ultra Burst do Necrozma).
- **`teralization`** (padrão: ligado) — liga ou desliga todo o sistema de Terastalização (inclui a queda de Tera Shards).
- **`dynamax`** (padrão: ligado) — liga ou desliga todo o sistema de Dinamax e Gigantamax.

## Mega Evolução

- **`multipleMegas`** (padrão: desligado) — quando desligado, você só pode ter um Pokémon Mega Evoluído por vez. Ligue para permitir vários Megas ao mesmo tempo.
- **`outSideMega`** (padrão: ligado) — permite Mega Evoluir um Pokémon fora de batalha, pela roda de interação dele.

## Ultra Burst

- **`outSideUltraBurst`** (padrão: ligado) — permite ativar o Ultra Burst do Necrozma fora de batalha, pela roda de interação.

## Terastalização

- **`teraShardRequired`** (padrão: 50) — quantos Tera Shards do mesmo tipo são necessários para mudar o Tera Tipo de um Pokémon.
- **`teraShardDropRate`** (padrão: 10.0) — chance, em porcentagem, de um Pokémon derrotado soltar o Tera Shard do tipo dele.
- **`stellarShardDropRate`** (padrão: 1.0) — chance, em porcentagem, de um Pokémon soltar um Stellar Tera Shard.
- **`teraHats`** (padrão: ligado) — mostra a "coroa" de cristal visual quando um Pokémon terastaliza.
- **`legacyTeraEffect`** (padrão: desligado) — usa o efeito visual antigo de terastalização em vez do novo.
- **`likoPendentDuration`** (padrão: cerca de 1 hora) — quanto tempo a Liko's Pendant leva, depois de equipada, para invocar um Terapagos.

## Dinamax

- **`powerSpotRange`** (padrão: 20) — alcance, em blocos, dentro do qual um Power Spot permite dinamaxar.
- **`dynamaxAnywhere`** (padrão: desligado) — quando ligado, permite dinamaxar em qualquer lugar, sem precisar de Power Spot.
- **`dynamaxScaleFactor`** (padrão: 4.0) — o quanto o Pokémon cresce de tamanho ao dinamaxar.

## Formas de vínculo (Battle Bond)

- **`minBondingRequired`** (padrão: 200) — nível mínimo de amizade que um Greninja precisa para receber a forma Ash-Greninja com o Ash Cap.

## Interface de batalha

- **`showBattleHUD`** (padrão: ligado) — mostra o HUD/painel extra de informações durante as batalhas.
- **`showStatChanges`** (padrão: ligado) — mostra as mudanças de atributos (ataque, defesa, etc.) na interface de batalha.
- **`showMoveTooltips`** (padrão: ligado) — mostra o inspetor de golpes, com detalhes dos movimentos durante a batalha.

## Outras opções

- **`msdPatchAutoUpdate`** (padrão: ligado) — mantém atualizado automaticamente o "patch" de dados de batalha do mod.
- **`debugMode`** (padrão: desligado) — ativa mensagens de depuração; útil para diagnóstico, deixe desligado no uso normal.

## Como aplicar mudanças

1. Edite `config/mega_showdown/config.json`.
2. Rode `/msd reload` no jogo (precisa ser operador) ou reinicie o servidor/jogo.
