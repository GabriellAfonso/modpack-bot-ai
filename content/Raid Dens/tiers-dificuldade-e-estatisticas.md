# Tiers de Dificuldade e Estatísticas

## O que são Tiers

Cada Cristal de Raid possui um **tier** de 1 a 7 estrelas que define a dificuldade da batalha. Tiers mais altos têm Pokémon mais fortes, mais HP, melhores recompensas e IVs garantidos no Pokémon de recompensa.

## Tabela de Estatísticas por Tier

| Tier | Estrelas | Nível do Chefe | Nível da Recompensa | HP do Chefe (×base) | IVs Garantidos | Energia de Raid |
|------|----------|---------------|---------------------|---------------------|----------------|-----------------|
| 1    | ★        | 12            | 12                  | 5×                  | 0 IVs máximos  | 0               |
| 2    | ★★       | 20            | 20                  | 5×                  | 1 IV máximo    | 1               |
| 3    | ★★★      | 35            | 35                  | 8×                  | 2 IVs máximos  | 2               |
| 4    | ★★★★     | 45            | 45                  | 12×                 | 3 IVs máximos  | 5               |
| 5    | ★★★★★    | 75            | 75                  | 20×                 | 4 IVs máximos  | 10              |
| 6    | ★★★★★★   | 75            | 75                  | 25×                 | 5 IVs máximos  | 15              |
| 7    | ★★★★★★★  | 100           | 100                 | 30×                 | 6 IVs máximos  | 20              |

> **IVs Garantidos:** O Pokémon de recompensa tem pelo menos esse número de IVs em valor máximo (31). Por exemplo, no Tier 7 você recebe um Pokémon com todos os 6 IVs no máximo.

## HP do Chefe com Múltiplos Jogadores

O HP do chefe escala com o número de jogadores na batalha. Cada jogador adicional multiplica o HP base (após o multiplicador de tier) por mais **1×** (padrão):

- **1 jogador:** HP base × multiplicador do tier
- **2 jogadores:** HP base × multiplicador do tier × 2
- **3 jogadores:** HP base × multiplicador do tier × 3
- **4 jogadores:** HP base × multiplicador do tier × 4

> Exemplo: Um Tier 5 com 4 jogadores tem seu HP total multiplicado por 20 (tier) × 4 (jogadores) = **80× o HP base** do Pokémon.

## Configurações por Tier

Além das estatísticas, cada tier tem configurações que podem ser ajustadas por admins:

- **Máximo de jogadores** — padrão: 4 (use -1 para ilimitado)
- **Máximo de vitórias** — número de vezes que o cristal pode ser conquistado antes de desativar:
  - Tiers 1–6: 3 vitórias
  - Tier 7: 3 vitórias
- **Máximo de Cheers por jogador** — padrão: 3 por raid
- **Taxa de Habilidade Oculta** — 20% de chance do chefe ter Habilidade Oculta
- **Taxa de shiny** — padrão: usa a taxa do Cobblemon (normalmente 1/8192); pode ser sobrescrita no config
- **Recompensa em moedas** (requer CobbleDollars):
  - Tier 1: $1.000
  - Tier 2: $2.000
  - Tier 3: $5.000
  - Tier 4: $10.000
  - Tier 5: $20.000
  - Tier 6: $50.000
  - Tier 7: $100.000
- **Vidas por jogador** — padrão: 1 vida (se todos os seus Pokémon desmaiarem, você perde)
- **Vidas compartilhadas** — padrão: desativado (cada jogador tem suas próprias vidas)
- **Dano mínimo para recompensa** — padrão: 0% (qualquer participação dá direito a recompensa)

## Alcançando Tiers Maiores

Não há um progresso linear bloqueado — qualquer jogador pode tentar qualquer tier encontrado. No entanto:

- Raids de Tier alto têm Pokémon com HP muito elevado e podem exigir Pokémon bem treinados.
- Alguns Tiers podem exigir uma **chave especial** no inventário para interagir com o cristal (configurável pelo admin).
- Raids de Tier 6 e 7 são raras de achar naturalmente (apenas 5% e 1% de chance de spawn).
