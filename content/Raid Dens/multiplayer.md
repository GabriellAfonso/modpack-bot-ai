# Multiplayer — Raids em Grupo

## Visão Geral do Multiplayer

Raids foram projetadas para ser jogadas em grupo. Até 4 jogadores podem participar da mesma batalha simultaneamente (configurável pelo admin). Jogar em grupo aumenta o HP do chefe, mas também permite estratégias cooperativas com Cheers e Pokémon complementares.

---

## Criando e Gerenciando o Lobby

O jogador que clica primeiro num Cristal de Raid ativo se torna o **anfitrião (host)**. O anfitrião controla quem entra na raid.

### Como convidar jogadores
- Outros jogadores precisam clicar no **mesmo cristal** para pedir para entrar.
- O anfitrião recebe uma notificação com o nome do jogador e botões **Aceitar** e **Recusar**.
- O pedido expira automaticamente se não for respondido em alguns segundos.
- Se o anfitrião não estiver disponível, a mensagem *"O anfitrião não pôde ser alcançado..."* aparece para quem pediu entrar.

### Limites do lobby
- **Máximo de 4 jogadores** por raid (padrão; configurável pelo admin como `max_players`).
- Se o lobby já está cheio, a mensagem *"Este lobby já está cheio!"* aparece para quem tenta entrar.

### Aceitar automaticamente
- O anfitrião pode ativar **"Aceitar pedidos de entrada automaticamente"** nas configurações de cliente para aprovar todos os jogadores sem intervenção manual.

---

## Durante a Batalha

### HP do Chefe com Múltiplos Jogadores
O HP do chefe aumenta proporcionalmente ao número de jogadores:
- **1 jogador:** HP normal × multiplicador do tier
- **2 jogadores:** HP normal × multiplicador do tier × 2
- **3 jogadores:** HP normal × multiplicador do tier × 3
- **4 jogadores:** HP normal × multiplicador do tier × 4

Isso torna o chefe mais difícil, mas com mais jogadores o dano total também é maior.

### Cheers e Suporte
Cada jogador tem seu próprio limite de Cheers. Os efeitos do Cheer se aplicam apenas ao time do jogador que o usou — usar um Apoio de Cura cura apenas os seus próprios Pokémon, não os de outros jogadores.

Por padrão, movimentos de suporte compartilhados ficam disponíveis com até 4 jogadores (`max_players_for_support`).

### Rastreamento de Dano
O mod rastreia quanto dano cada jogador causou ao chefe. Dependendo da configuração de `reward_distribution`:
- **`random`** — Todos participantes recebem recompensas independentemente do dano.
- **`damage`** — Apenas jogadores que causaram a porcentagem mínima (`required_damage`) de dano ao chefe recebem recompensas.
- **`survivor`** — Apenas os que sobreviveram recebem recompensas.

---

## Vidas Individuais vs. Compartilhadas

### Vidas Individuais (padrão)
- Cada jogador tem seu próprio número de vidas (padrão: 1).
- Se todos os seus Pokémon desmaiarem, você perde sua vida.
- Com 0 vidas, você é eliminado da raid.
- A raid continua enquanto houver pelo menos 1 jogador com vidas restantes.

### Vidas Compartilhadas (configurável)
- Todos os jogadores compartilham um único pool de vidas.
- Qualquer jogador desmaiando consome uma vida do pool coletivo.
- Quando o pool chega a 0, a raid termina em derrota para todos.

---

## Recompensas Sincronizadas

Com `sync_rewards: true` (padrão), todos os jogadores recebem o **mesmo** Pokémon de recompensa — mesmos IVs, mesma natureza, mesmo se é shiny ou não. Isso significa que se o Pokémon sortear shiny, **todos** os participantes recebem um shiny.

Com `sync_rewards: false`, cada jogador rola seus próprios atributos individualmente.

---

## Problemas Comuns em Multiplayer

| Situação | Solução |
|----------|---------|
| Você está "travado" em estado de raid após desconexão | Peça para um admin executar `/crd refresh @s` no seu nome |
| O host desconectou antes de iniciar a batalha | A mensagem *"O anfitrião não pôde ser alcançado..."* aparece. Aguarde o cristal resetar ou peça ao admin para usar `/crd forceclear` |
| Você já completou o máximo de vitórias nesse cristal | A mensagem *"Você já concluiu esta raid."* aparece. Aguarde o reset (2h padrão) ou peça ao admin para usar `/crd resetclears @s` |
| Você já está hospedando outra raid | A mensagem *"Você já está hospedando outra raid."* aparece. Use `/crd refresh` para limpar o estado |
