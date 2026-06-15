# Batalha em Raid

## Como funciona a Batalha de Raid

Uma batalha de Raid é uma luta cooperativa onde até 4 jogadores enfrentam juntos um único Pokémon-chefe muito poderoso. Ao contrário de uma batalha normal do Cobblemon, o chefe tem o HP multiplicado várias vezes e ações especiais próprias.

## Entrando na Batalha

Depois que o anfitrião aceita todos os jogadores no lobby e a batalha começa:
- Todos os jogadores são teleportados para uma **dimensão exclusiva da raid**.
- Cada jogador usa **1 Pokémon** por vez por padrão (configurável pelo admin como `raid_party_size`).
- A batalha começa automaticamente.

## HP do Chefe

O HP total do chefe é calculado assim:

```
HP Total = HP Base do Pokémon × Multiplicador do Tier × Número de Jogadores
```

Exemplos com 2 jogadores:
- Tier 1: HP Base × 5 × 2 = 10× o HP normal
- Tier 5: HP Base × 20 × 2 = 40× o HP normal
- Tier 7: HP Base × 30 × 2 = 60× o HP normal

## Mecânicas Especiais do Chefe

### Escudo (Shield)
- Em determinados momentos da batalha, o chefe pode ativar um **escudo de energia**.
- Enquanto o escudo está ativo, o chefe recebe menos dano.
- A mensagem *"Energia começou a se reunir ao redor de [chefe]!"* aparece quando o escudo é ativado.
- *"[Chefe] sucumbiu ao ataque e quebrou sua postura!"* aparece quando o escudo quebra.

### Reset de Status
- O chefe pode limpar seus próprios efeitos negativos (como quedas de atributo, status).
- A mensagem *"[Chefe] limpou seus próprios efeitos negativos!"* aparece.
- O chefe também pode limpar os boosts positivos dos jogadores:
  - A mensagem *"[Chefe] limpou suas alterações de status positivas!"* aparece para os jogadores afetados.

## Vidas dos Jogadores

- Por padrão, cada jogador tem **1 vida** por raid.
- Se todos os seus Pokémon desmaiarem durante a batalha, você **perde sua vida** e fica eliminado da raid.
- Se todos os jogadores perderem suas vidas, a raid termina em derrota.
- O admin pode configurar mais vidas por jogador ou ativar **vidas compartilhadas** (todos os jogadores dividem um único pool de vidas).

## Restrições Durante a Batalha

Algumas ações são bloqueadas durante raids:
- **Itens normais** não podem ser usados na batalha (somente Cheers).
- **Held items (itens segurados) proibidos** podem ser bloqueados pelo admin.
- **Habilidades ou movimentos proibidos** também podem ser restritos.

A mensagem *"Você não pode usar itens em uma batalha de Raid."* aparece se tentar usar itens regulares.

## Usando Cheers (Apoios)

Durante a batalha, cada jogador pode usar **Cheers** — ações especiais de apoio que não gastam turno normal. Existem 3 tipos:

- **Apoio de Ataque** — Aumenta Ataque e Ataque Especial do seu time em 50%.
- **Apoio de Defesa** — Aumenta Defesa e Defesa Especial do seu time em 50%.
- **Apoio de Cura** — Restaura 50% do HP de todo o seu time.

Cada jogador tem um limite de Cheers por raid (padrão: **3 uses** nos Tiers 1–6, **3 uses** no Tier 7). Ao tentar usar mais que o limite, a mensagem *"Você não tem mais apoios restantes."* aparece.

> Para mais detalhes sobre os Cheers, veja o arquivo **cheers-apoios.md**.

## Capturando o Chefe

Após a vitória, a tela de recompensas aparece com a pergunta *"Você gostaria de capturar [Pokémon]?"*:

- Pressione **Capturar** para tentar capturar o chefe (você precisa estar segurando uma Pokébola na mão).
- Pressione **Passar** para pular a captura e ir direto para os itens.
- Pressione **Resgatar recompensas** se quiser forçar a coleta sem capturar.

A taxa de captura do chefe pode ser aumentada com o **Catching Charm** (Amuleto de Captura) equipado na mão esquerda.

Por padrão, não há limite de capturas por raid (todos os jogadores podem tentar). Isso pode ser configurado pelo admin.

## Fim da Batalha

- **Vitória:** Todos os jogadores recebem um Raid Pouch com itens, e podem tentar capturar o chefe.
- **Derrota:** A mensagem *"O chefe da raid era muito forte!"* aparece. Nenhuma recompensa é dada.
- Derrotas **não contam** como uma vitória para o limite máximo de clears do cristal (padrão; configurável).

## Distribuição de Recompensas

Por padrão (modo `random`), todos os jogadores que participaram recebem recompensas. Outros modos disponíveis (configuráveis pelo admin):

- **random** — todos os participantes recebem recompensas de forma independente.
- **damage** — apenas jogadores que causaram uma porcentagem mínima de dano recebem recompensas.
- **survivor** — apenas jogadores que sobreviveram à batalha recebem recompensas.
