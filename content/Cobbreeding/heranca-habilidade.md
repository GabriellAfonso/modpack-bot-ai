# Herança de Habilidade — Hidden Ability

A **Habilidade** de um Pokémon pode ser herdada durante o breeding. Este guia explica como funciona a herança e como aumentar as chances de obter a **Hidden Ability** (HA).

## De qual pai vem a habilidade

A habilidade é herdada da **mãe**. Em casos onde um dos pais é Ditto, a habilidade vem do **pai não-Ditto**.

## Como funciona a herança

O sistema olha o **slot da habilidade** do pai que transmite (Habilidade 1, Habilidade 2 ou Hidden Ability) e tenta reproduzir esse mesmo slot no filho:

- Se o pai transmissor tiver **Habilidade comum (slot 1 ou 2):** o filho tem **80% de chance** de herdar a mesma habilidade. Os 20% restantes resultam em outra habilidade disponível da espécie (que pode ser a HA, se habilitado).
- Se o pai transmissor tiver **Hidden Ability:** o filho tem **60% de chance** de herdar a HA. Os 40% restantes resultam em uma habilidade comum.

## Random Hidden Ability (padrão ativo)

Com a configuração padrão do servidor (`hiddenAbilitiesEnabled = true`), há uma **pequena chance** de o filho obter sua Hidden Ability mesmo que nenhum dos pais a possua. Isso é diferente dos jogos principais, onde a HA só pode ser passada se um dos pais tiver ela.

Se o servidor desativar essa opção (`hiddenAbilitiesEnabled = false`), a HA só pode ser obtida por breeding se o pai transmissor já tiver a HA.

## Habilidades Forçadas

Alguns Pokémon podem ter habilidades "forçadas" — habilidades que normalmente não existem para aquela espécie-filha. Por padrão, essa herança é **desativada** (`forcedAbilitiesEnabled = false`).

Se o servidor ativar essa opção, um pai com habilidade forçada transmite essa habilidade ao filho, mesmo que o filho normalmente não possa tê-la. Essas habilidades são marcadas como "forçadas" e não mudam durante a evolução.

## Casos especiais

- **Ferroseed:** possui a mesma habilidade comum e HA. O sistema ainda aplica as probabilidades normalmente para evitar que sempre herde a HA.
- **Pokémon sem slot correspondente:** se a espécie filha não tiver um slot equivalente ao do pai (por exemplo, o pai evoluiu e tem menos opções), o sistema usa o primeiro slot disponível da mesma prioridade, ou o primeiro slot comum como fallback.
