# Automação das Máquinas Gacha com Hoppers

O Cobbled Gacha suporta automação parcial via hoppers, permitindo que moedas sejam inseridas nas máquinas automaticamente sem que um jogador precise estar presente. Esse recurso é **desativado por padrão** e precisa ser habilitado pelo administrador do servidor.

---

## Pré-requisito: automação habilitada

A automação só funciona se o servidor tiver configurado `"automation": true` no arquivo `server_config.json`. Se não estiver ativado, hoppers não conseguem inserir moeda nas máquinas.

---

## Como funciona a automação

Quando ativada, as máquinas gacha funcionam como inventários com dois slots:

- **Slot 0 (entrada):** Recebe moedas. Um hopper apontado para a parte superior da máquina pode inserir itens aqui.
- **Slot 1 (saída):** Recebe as cápsulas dispensadas. Um hopper embaixo da máquina pode puxar os itens daqui.

A máquina processa a moeda automaticamente a cada tick do jogo quando há item válido no slot de entrada.

---

## Restrições da automação

Nem todas as máquinas podem ser automatizadas:

- **Máquinas do tipo spawner** (como a Strange Crystallized Machine, configurada como "spawner"): **não podem ser automatizadas**. A moeda é rejeitada mesmo com automação ativa.
- **Máquinas do tipo specific (Plush-O-Matic):** podem ser automatizadas, mas o hopper precisa inserir yarns do mesmo tipo para que o giro complete corretamente.
- **Máquinas genéricas:** podem ser automatizadas normalmente.

---

## Onde as recompensas vão na automação

Quando a máquina é acionada automaticamente (sem jogador presente):

1. A cápsula vai primeiro para o **slot 1** da máquina (slot de saída)
2. Se houver um inventário ou hopper abaixo da máquina, o item é transferido para lá
3. Se o slot de saída estiver cheio e não houver inventário abaixo, o item cai no chão na frente da máquina

---

## Configuração do hopper (como colocar)

Para entrada de moeda:
- Coloque um hopper apontado para **cima** conectado à parte superior da máquina
- Ou coloque um hopper apontado diretamente para a máquina pelo lado

Para saída de cápsulas:
- Coloque um hopper **embaixo** da máquina
- O hopper puxa itens do slot de saída automaticamente

---

## Notas importantes

- A automação usa um "jogador fake" internamente para processar as inserções — isso significa que o cooldown por jogador se aplica ao jogador fake, não ao jogador real
- O cooldown do jogador real não é afetado pela automação
- Se a moeda no slot de entrada não for válida para aquela máquina, ela não é consumida — fica parada no slot até ser removida manualmente
- Para máquinas do tipo specific (Plush-O-Matic), a moeda no hopper precisa ser do tipo correto após a trava ser definida; caso contrário, a inserção é rejeitada
