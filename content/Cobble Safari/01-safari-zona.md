# Safari Zone — Entrada e Funcionamento Geral

## O que é a Safari Zone

A Safari Zone é uma dimensão especial do CobbleSafari onde você pode capturar Pokémon usando regras diferentes das batalhas normais. Não há batalhas: você usa **Safari Balls**, **Bait** e **Mud Balls** para aumentar suas chances antes de arremessar a bola. A dimensão reseta todos os dias à meia-noite (UTC), apagando tudo e expulsando os jogadores.

---

## Como entrar

Para entrar na Safari Zone você precisa de um **Ticket Safari** (`cobblesafari:ticket_safari`). Esse ticket é consumido na entrada. Re-entrada paga está desabilitada neste servidor — ou seja, cada ticket dá acesso durante aquele ciclo diário.

Após entrar, você recebe automaticamente na hora:
- **16 Safari Balls**
- **32 Bait**
- **32 Mud Balls**

Esses itens são repostos uma vez por dia, no reset. Nenhum Safari Ball extra é dado sem um ticket.

---

## Teleportador Safari

O **Safari Teleporter** é o bloco usado para acessar a Safari Zone. Ele pode ser craftado:

```
Crafting (Shaped):
I G I
I D I
S D S

I = Iron Ingot
G = Glass
D = Diamond
S = Smooth Stone
```

Também é possível encontrar teleportadores já posicionados no mundo (raio de até 5000 blocos da origem do servidor).

---

## Timer de sessão

Cada entrada na Safari Zone tem um timer de **15 minutos (900 segundos)**. Quando o tempo acaba:
- Você é teleportado de volta para o ponto onde estava antes de entrar.
- Se você morrer dentro da dimensão, o timer é consumido imediatamente e você é expulso ("death drained" — a morte age como fim de sessão).
- Existe um período de graça de **5 minutos (300 segundos)** antes do reset diário: se você estiver dentro durante o reset, receberá um aviso e terá tempo para sair antes de ser expulso.

---

## Reset diário

Todo dia à meia-noite (UTC), a Safari Zone reseta:
- Todos os Pokémon despawnam.
- Os itens diários (Safari Balls, Bait, Mud Balls) são repostos para o próximo acesso.
- Jogadores dentro da dimensão são expulsos (com período de graça de 5 minutos antes do reset acontecer).

---

## Restrições dentro da Safari Zone

Dentro da dimensão, algumas ações podem ser bloqueadas por configuração do servidor:
- Quebrar blocos pode ser desabilitado.
- Colocar blocos pode ser desabilitado.
- Batalhas normais de Pokémon podem ser desabilitadas (a captura Safari é o único método).

Use `/safariexit` a qualquer momento para sair da dimensão e retornar ao ponto de origem.
