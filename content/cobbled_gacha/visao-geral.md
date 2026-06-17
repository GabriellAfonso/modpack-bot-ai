# Cobbled Gacha — Visão Geral do Mod

**Cobbled Gacha** é um mod para Minecraft (Fabric) que adiciona máquinas de gacha ao jogo. Você insere itens de moeda em uma máquina e recebe cápsulas com recompensas aleatórias, ou faz um Pokémon aparecer, dependendo do tipo de máquina. Muitos jogadores chamam essas máquinas de gacha de **cassino** (ou casino), por causa da mecânica de pagar moeda e receber prêmio aleatório.

O mod funciona em conjunto com o **Cobblemon** (mod de Pokémon para Minecraft), mas nem todas as máquinas exigem isso.

---

## O que o mod adiciona

### Máquinas (blocos)
São 12 máquinas diferentes, cada uma com sua própria moeda, custo e recompensas:

Moedas configuradas pelo datapack deste servidor:

| Máquina | Nome | Moeda aceita |
|---|---|---|
| Poké Gacha Machine | Máquina principal | Gacha Coin |
| Cram O' Matic | Máquina de apricorns | Apricorns (7 tipos) |
| Item Printer | Impressora de itens | Gacha Coin |
| Strange Crystallized Machine | Máquina especial de spawn | Gacha Coin 10 (Premier) |
| Citrine Poké Gacha Machine | Variante dourada | Gacha Coin |
| Verdant Poké Gacha Machine | Variante verde | Gacha Coin |
| Azure Poké Gacha Machine | Variante azul | Gacha Coin |
| Roseate Poké Gacha Machine | Variante rosa | Gacha Coin |
| Slate Poké Gacha Machine | Variante preta | Gacha Coin |
| Premier Poké Gacha Machine | Variante branca | Gacha Coin |
| Rocket Prize Master | Máquina do Team Rocket | Gacha Coin 10 (Premier) |
| Plush-O-Matic | Máquina de pelúcias | Fantasy Yarn |

### Itens de moeda
- **Gacha Coins 1–10** — moedas craftáveis; neste servidor a **Gacha Coin** é a moeda padrão das máquinas e a **Gacha Coin 10 (Premier)** é usada pela Strange Crystallized Machine e pelo Rocket Prize Master
- **Apricorns** — usados pelo Cram O' Matic
- **Fantasy Yarn** — único yarn aceito pelo Plush-O-Matic neste servidor (craftável com gems Pokémon)
- **Koban Coin** — drop de Meowth; **não** é mais necessária aqui (o Rocket Prize Master foi reconfigurado para Gacha Coin 10)

### Cápsulas
- **100 cápsulas** (grupos A–J, 10 variantes cada) — itens que ao serem usados na mão abrem uma tabela de loot e dão recompensas
- Cada cápsula tem sua própria lista de recompensas definida pelo servidor

### Bolas de Pokémon
- **Gacha Balls 1–6** — bolas que ao serem usadas fazem um Pokémon aparecer perto de você
- **Rocket Ball** — bola especial que spawna Pokémon do pool do Team Rocket

---

## Como as máquinas funcionam (resumo)

As máquinas gacha (o "cassino" do servidor) funcionam assim:

1. Segure a moeda correta na mão
2. Clique com botão direito na máquina
3. Cada clique insere 1 moeda — a máquina precisa de um número fixo de moedas para girar
4. Ao completar o custo, a máquina dispensa a recompensa na frente dela
5. Pode haver um cooldown antes de poder usar a máquina novamente

Para detalhe completo da mecânica de uso, veja o arquivo **como-usar-maquinas-gacha.md**.

---

## Sistemas do mod

- **Sistema de cooldown** — limita quantas vezes por período um jogador pode usar cada máquina
- **Automação com hoppers** — máquinas podem receber moeda via hopper (se habilitado no servidor)
- **Spawn pools personalizados** — máquinas do tipo "spawner" usam pools de Pokémon configuráveis por datapack
- **Tipo "specific" (contiguous)** — máquinas que travam o tipo de moeda na primeira inserção e variam a recompensa conforme a moeda usada

---

## Configuração

O comportamento do mod é controlado pelo arquivo `data/cobbledgacha/config/server_config.json`. Servidores podem ajustar cooldowns, custo de moedas, tipo de cada máquina e pesos dos buckets de raridade. Veja **configuracoes-servidor.md** para o guia completo.
