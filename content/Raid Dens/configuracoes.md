# Configurações do Cobblemon Raid Dens

As configurações ficam em arquivos dentro da pasta `config/cobblemonraiddens/`. Cada arquivo pode ser editado manualmente ou via interface gráfica do ModMenu (se instalado).

---

## Configurações Gerais (`common.json`)

### `enable_spawning`
- **Padrão:** `true`
- **Efeito:** Ativa ou desativa o surgimento natural de Cristais de Raid no mundo. Se `false`, nenhum cristal aparece automaticamente — apenas os criados via comando `/crd dens`.

### `dimension_tier_weights`
- **Padrão:** `{"minecraft:overworld": [9.0, 15.0, 25.0, 25.0, 20.0, 5.0, 1.0]}`
- **Efeito:** Define o peso de cada tier (1 a 7) por dimensão. Os números representam a probabilidade relativa — ex: `25.0` para Tier 3 significa que 25% dos cristais gerados nessa dimensão são Tier 3. Pode ser configurado por dimensão para, por exemplo, fazer o Nether gerar apenas raids de Tier 6–7.

### `dimension_spawn_rate`
- **Padrão:** `{"minecraft:overworld": 256}`
- **Efeito:** Chance de 1 em X por chunk de um Cristal de Raid surgir. `256` significa que há 1 chance em 256 por chunk carregado. Valores menores = mais raids no mundo.

### `reset_time`
- **Padrão:** `7200` (segundos = 2 horas)
- **Efeito:** Tempo em segundos até um cristal desativado resetar e voltar a funcionar. Use `-1` para desativar o reset automático (o cristal some permanentemente após o limite de vitórias).

### `cycle_mode`
- **Padrão:** `ALL`
- **Opções:** `NONE`, `LOCK_BOTH`, `LOCK_TIER`, `LOCK_TYPE`, `BUCKET`, `ALL`
- **Efeito:** Controla como o Pokémon-chefe e o tipo mudam entre resets do cristal:
  - `NONE` — Chefe e tipo nunca mudam.
  - `LOCK_BOTH` — Chefe e tipo travados no valor inicial para sempre.
  - `LOCK_TIER` — Chefe travado, tipo pode mudar.
  - `LOCK_TYPE` — Tipo travado, chefe pode mudar.
  - `BUCKET` — Usa pools com pesos para sortear o próximo chefe.
  - `ALL` — Chefe e tipo são sorteados livremente a cada reset.

### `max_clears_include_fails`
- **Padrão:** `false`
- **Efeito:** Se `true`, derrotas também contam para o número máximo de vitórias do cristal. Se `false`, apenas vitórias contam.

### `sync_rewards`
- **Padrão:** `true`
- **Efeito:** Se `true`, o Pokémon de recompensa tem os mesmos atributos (IVs, natureza, shiny) para todos os jogadores que venceram. Se `false`, cada jogador rola seus próprios atributos individualmente.

### `can_break`
- **Padrão:** `true`
- **Efeito:** Se `false`, jogadores não conseguem quebrar os Cristais de Raid (nem com picareta nem com explosão).

### `reward_distribution`
- **Padrão:** `random`
- **Opções:** `random`, `damage`, `survivor`
- **Efeito:** Define quem recebe recompensas:
  - `random` — Todos os participantes recebem.
  - `damage` — Apenas quem causou a porcentagem mínima de dano configurada.
  - `survivor` — Apenas quem sobreviveu à batalha.

### `max_players_for_support`
- **Padrão:** `4`
- **Efeito:** Número máximo de jogadores em raid antes de desativar movimentos de suporte compartilhados.

### `required_energy`
- **Padrão:** `100`
- **Efeito:** Quantidade de energia necessária para converter um Raid Shard em Cristal de Raid.

---

## Configurações por Tier (`tier_one.json` até `tier_seven.json`)

Cada tier tem seu próprio arquivo. Os valores abaixo são os padrões globais — as diferenças entre tiers estão descritas em **tiers-dificuldade-e-estatisticas.md**.

### `requires_key`
- **Padrão:** `false`
- **Efeito:** Se `true`, jogadores precisam de uma chave especial no inventário para interagir com cristais desse tier.

### `all_require_unique`
- **Padrão:** `true`
- **Efeito:** Se `true` e `requires_key` estiver ativo, **todos** os jogadores precisam da chave (não só o anfitrião).

### `max_players`
- **Padrão:** `4`
- **Efeito:** Máximo de jogadores por raid. Use `-1` para ilimitado.

### `max_clears`
- **Padrão:** `3` (igual em todos os tiers por padrão)
- **Efeito:** Número de vitórias até o cristal ser desativado. Use `-1` para ilimitado.

### `max_cheers`
- **Padrão:** `3`
- **Efeito:** Número máximo de Cheers (apoios) que cada jogador pode usar por raid.

### `ha_rate`
- **Padrão:** `0.20` (20%)
- **Efeito:** Porcentagem de chance do Pokémon-chefe ter sua Habilidade Oculta.

### `raid_party_size`
- **Padrão:** `1`
- **Efeito:** Número de Pokémon que o jogador pode usar em combate simultaneamente durante a raid.

### `health_multiplier`
- **Padrão:** Varia por tier (5, 5, 8, 12, 20, 25, 30)
- **Efeito:** Multiplicador do HP do chefe. O HP final é `HP base × health_multiplier × número_de_jogadores`.

### `multiplayer_health_multiplier`
- **Padrão:** `1.0`
- **Efeito:** Multiplicador adicional de HP por jogador extra. `1.0` significa que cada jogador adicional multiplica o HP por 1 (ou seja, dobra por 2 jogadores, triplica por 3, etc.).

### `boss_level`
- **Padrão:** Varia (12, 20, 35, 45, 75, 75, 100)
- **Efeito:** Nível do Pokémon-chefe na batalha.

### `reward_level`
- **Padrão:** Igual ao `boss_level`
- **Efeito:** Nível do Pokémon de recompensa recebido.

### `ivs`
- **Padrão:** Varia (0, 1, 2, 3, 4, 5, 6)
- **Efeito:** Número de IVs máximos garantidos no Pokémon de recompensa.

### `shiny_rate`
- **Padrão:** `-1.0`
- **Efeito:** Taxa de shiny como `1 em X`. Use `-1.0` para usar a taxa padrão do Cobblemon. Ex: `8192.0` = 1 em 8192.

### `currency`
- **Padrão:** Varia (1000, 2000, 5000, 10000, 20000, 50000, 100000)
- **Efeito:** Quantidade de CobbleDollars recebidos ao vencer (requer mod CobbleDollars).

### `max_catches`
- **Padrão:** `-1` (ilimitado)
- **Efeito:** Máximo de Pokémon que podem ser capturados por raid. `-1` significa que todos os jogadores podem capturar.

### `raid_ai`
- **Padrão:** `random`
- **Opções:** `random`, `strong`, `rct`
- **Efeito:** IA usada pelo chefe para escolher movimentos. `random` = aleatório; `strong` = escolhe movimentos mais fortes; `rct` = IA avançada (requer RCTAPI).

### `lives`
- **Padrão:** `1`
- **Efeito:** Número de vidas por jogador na raid. Se todos os Pokémon do jogador desmaiarem, ele perde 1 vida.

### `players_share_lives`
- **Padrão:** `false`
- **Efeito:** Se `true`, todos os jogadores compartilham um único pool de vidas. Se `false`, cada jogador tem suas próprias vidas.

### `energy`
- **Padrão:** Varia (0, 1, 2, 5, 10, 15, 20)
- **Efeito:** Quantidade de energia de Raid concedida ao Raid Shard por vitória nesse tier.

### `required_damage`
- **Padrão:** `0.0` (0%)
- **Efeito:** Porcentagem mínima de dano que um jogador precisa causar para receber recompensas. `0.0` = qualquer participação é suficiente.

### `catch_rate`
- **Padrão:** `1.0`
- **Efeito:** Multiplicador base da taxa de captura do chefe. `1.0` = taxa normal da Pokébola usada.

---

## Configurações de Cliente

Estas configurações são individuais por jogador e podem ser alteradas nas configurações do jogo (via ModMenu ou tecla de configurações):

### Feixe de Sinalizador (Beacon Beam)
- **`show_beam_tier_one` até `show_beam_tier_seven`** — Ativa ou desativa o feixe de luz acima dos cristais de cada tier. Útil para visualizar raids a distância. Padrão: ativado para todos.

### Interface
- **`auto_accept_requests`** — Aceita automaticamente todos os pedidos de jogadores para entrar na sua raid. Padrão: desativado.
- **`enable_raid_logs`** — Exibe o log de batalha (movimentos usados) na tela durante raids. Padrão: ativado.
- **`raid_popup_x / raid_popup_y`** — Posição horizontal/vertical do popup de raid na tela (em %).
- **`raid_status_x / raid_status_y`** — Posição horizontal/vertical do painel de status da raid na tela (em %).
