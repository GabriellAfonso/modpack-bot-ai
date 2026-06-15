# Encontrando e Iniciando Raids

## O que é um Cristal de Raid

O **Cristal de Raid** (Raid Den Crystal) é um bloco especial que surge naturalmente no mundo e serve como ponto de entrada para batalhas de Raid. Ele emite luz de nível 8 quando ativo e muda de cor conforme o tipo do Pokémon dentro (por exemplo, vermelho para raids de Fogo, azul para raids de Água, etc.).

Cada cristal tem:
- **Tier** (dificuldade de 1★ a 7★)
- **Tipo** (como Fogo, Água, Psíquico — determina o visual e os Pokémon que aparecem)
- **Feature** (Regular, Mega, Tera, Dynamax, etc. — pode variar)
- **Número máximo de vitórias** antes de ser desativado (varia por tier)

## Como encontrar Cristais de Raid

Cristais de Raid surgem naturalmente pelo Overworld enquanto você explora. A chance de aparecer é **1 em 256 por chunk**, e o tier do cristal é sorteado com os seguintes pesos padrão:

| Tier | Estrelas | Peso de spawn (Overworld) |
|------|----------|--------------------------|
| 1    | ★        | 9% de chance             |
| 2    | ★★       | 15% de chance            |
| 3    | ★★★      | 25% de chance            |
| 4    | ★★★★     | 25% de chance            |
| 5    | ★★★★★    | 20% de chance            |
| 6    | ★★★★★★   | 5% de chance             |
| 7    | ★★★★★★★  | 1% de chance             |

Cristais de Tier mais alto são mais raros, mas dão recompensas muito melhores.

> **Dica:** Use mods como Jade ou WTHIT para ver informações do cristal ao apontar para ele — isso mostra o tier, tipo e se está ativo.

## Como iniciar uma Raid

1. **Clique com o botão direito** no Cristal de Raid ativo.
2. Se o cristal precisar de uma **chave especial** (Tier com `requires_key: true`), você precisará ter esse item no inventário antes de entrar.
3. Você entra no lobby como **anfitrião (host)**.
4. Outros jogadores podem clicar no mesmo cristal e pedir para entrar — uma tela de confirmação aparece para o anfitrião aceitar ou recusar.
5. O lobby suporta até 4 jogadores simultaneamente (padrão configurável).
6. Quando todos estiverem prontos, a batalha começa: todos os jogadores são teleportados para uma dimensão especial da raid.

## Sistema de Convite Multiplayer

Quando outro jogador clica num cristal onde você já está no lobby:
- Você recebe uma notificação na tela com o nome do jogador.
- Botões de **Aceitar** e **Recusar** ficam disponíveis.
- Se não responder em tempo, o pedido expira automaticamente.
- Você pode ativar **aceitar automaticamente** nas configurações de cliente.

## Limite de Vitórias e Reset

Cada cristal tem um número máximo de vitórias (padrão: 3 para Tiers 1–4, variando para Tiers 5–7). Depois de atingir esse limite:
- O cristal é **desativado** temporariamente.
- Após **2 horas** (padrão, configurável), o cristal reseta e pode ser usado novamente.
- Ao resetar, o Pokémon-chefe e/ou o tipo podem mudar, dependendo do **modo de ciclo** configurado.

## Saindo de uma Raid

Dentro da dimensão de raid, existe um bloco chamado **Cristal de Retorno** (Raid Home Block). Clicar nele teleporta você de volta ao Overworld. Se você estiver no meio da batalha, sair vai remover você da raid.
