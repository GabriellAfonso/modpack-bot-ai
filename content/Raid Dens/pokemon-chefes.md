# Pokémon Chefes de Raid

## Como Funcionam os Chefes

Cada Cristal de Raid contém um **Pokémon-chefe** pré-definido (ou sorteado ao gerar). O chefe possui:
- Um conjunto fixo de 4 movimentos definidos pelo mod.
- HP muito acima do normal, multiplicado pelo tier e pelo número de jogadores.
- Nível determinado pelo tier (12 para Tier 1, 100 para Tier 7).
- Possibilidade de ter Habilidade Oculta (20% de chance padrão).
- Possibilidade de ser shiny (taxa padrão do Cobblemon).

O mod inclui **879 Pokémon** configurados como possíveis chefes — um para cada espécie principal do Cobblemon.

---

## Exemplos de Chefes e Movimentos

### Alakazam (Tier 4 — Psíquico)
- Movimentos: Future Sight, Psychic, Psyshock, Psycho Cut
- Tipo de Raid: Psíquico

### Charizard (Tier 5 — Fogo)
- Movimentos: Flare Blitz, Slash, Dragon Claw, Air Slash
- Tipo de Raid: Fogo

Os movimentos e tiers de cada Pokémon são definidos em arquivos de configuração e **podem ser personalizados pelo admin do servidor**.

---

## Propriedades Customizáveis (para Admins)

Cada chefe pode ter as seguintes propriedades no seu arquivo de configuração:

- **Movimentos** — 4 movimentos que o chefe usa em batalha.
- **Tier** — Dificuldade (TIER_ONE a TIER_SEVEN).
- **Tipo** — Tipo visual do cristal que gera esse chefe.
- **Feature** — Forma especial (DEFAULT, MEGA, TERA, DYNAMAX, etc.).
- **Peso (weight)** — Probabilidade relativa de aparecer. Chefes com `weight: 20` são mais comuns que com `weight: 1`.
- **Chave única** — Item especial necessário para desafiar esse chefe.
- **Texto da barra de vida** — Nome customizado na barra de HP do chefe.
- **Escala** — Tamanho do modelo do chefe (requer Size Variations).
- **Música** — Música customizada para a batalha.
- **Máximo de jogadores** — Sobrescreve o limite do tier para esse chefe específico.
- **Máximo de vitórias** — Sobrescreve o limite do tier para esse chefe específico.
- **Taxa de Habilidade Oculta** — Sobrescreve a chance de HA do tier.
- **Taxa de shiny** — Sobrescreve a taxa do tier.
- **Recompensa em moedas** — Sobrescreve o valor do tier.
- **Taxa de captura** — Sobrescreve a taxa base do tier.
- **Multiplicador de HP** — Sobrescreve o multiplicador do tier.
- **Tamanho do time** — Sobrescreve quantos Pokémon o jogador pode usar.
- **Scripts** — Comportamentos especiais ativados por gatilhos (ex: ao usar % de HP, por turno, etc.).
- **IA de batalha** — `random`, `strong` ou `rct`.
- **Marcas** — Marcas que o Pokémon de recompensa receberá automaticamente.

---

## Peso e Sorteio de Chefes

Quando um cristal é sorteado (modo de ciclo `ALL`, `BUCKET` ou `LOCK_TYPE`), o jogo escolhe o chefe com base no **peso** de cada um. Exemplo:

- Alakazam (weight: 20) aparece com mais frequência.
- Um chefe raro (weight: 1) aparece muito menos.

O sorteio é feito entre todos os chefes elegíveis para o tier e tipo do cristal.

---

## Chefes com Chave Especial

Alguns chefes (configuráveis pelo admin) podem exigir um **item de chave exclusiva** no inventário para desafiar. Se você não tiver a chave:
- A mensagem *"Você precisa de um item especial para entrar nesta raid!"* aparece.
- Você não consegue entrar no lobby.

Chaves são itens customizados criados pelo admin e distribuídos como recompensas especiais, eventos ou via loot personalizado.

---

## Comportamentos Especiais (Scripts)

Chefes podem ter **scripts** — comportamentos automáticos ativados por gatilhos durante a batalha. Exemplos de gatilhos possíveis:

- **Por turno** — Executado a cada N turnos da batalha.
- **Por dano recebido** — Ativado quando o chefe perde uma % do HP.
- **Ao desmaiar** — Ativado quando o Pokémon do jogador desmaia.
- **Ao entrar um jogador** — Ativado quando um jogador entra na batalha.
- **Por timer** — Ativado após um tempo específico.

Scripts podem fazer o chefe executar movimentos extras, ativar escudos, curar-se, limpar debuffs, etc. O comportamento exato depende do que foi configurado pelo admin.
