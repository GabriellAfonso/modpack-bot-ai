# Invocações Diversas (Meltan, Eternatus, Hoopa, Victini, Mew, Heatran, Celebi)

Este arquivo reúne lendários e singulares do mod Legendary Monuments que têm mecânicas próprias de invocação, separadas dos pedestais comuns.

## Caixa de Meltan (Meltan Box) → Meltan

A **Caixa de Meltan** (Meltan Box) é um bloco onde você deposita metais para invocar Meltan.

- Clique na caixa segurando **lingotes de metal** para depositá-los. A caixa só aceita lingotes de metal; outros itens são recusados ("This box only accepts metal ingots").
- Cada metal vale um certo "valor"; você precisa acumular **50 de valor em metais** dentro da caixa. A mensagem mostra "x/50 metal value stored".
- Quando estiver cheia, clique de novo para invocar um **Meltan** (nível 5). Há 2% de chance de ser Shiny.

Receita da Caixa de Meltan (3x3):
```
R W B
U S U
U U U
```
onde R = Bloco de Redstone, W = Bloco de Golem de Aço, B = Bloco de Lápis-Lazúli, S = Lingote de Netherita, U = Lingote de Ferro.

## Casulo de Eternatus (Eternatus Cocoon) → Eternatus

O **Casulo de Eternatus** (Eternatus Cocoon) é uma estrutura-bloco onde você alimenta Partículas de Galar para libertar Eternatus.

- Clique no casulo segurando **Partícula de Galar** (Galar Particle). Se você não tiver nenhuma, ele avisa "You don't have any galar particles".
- Você precisa consumir **500 Partículas de Galar** no casulo. A mensagem mostra o progresso "x/500 galar particles consumed".
- Ao atingir 500, o casulo se desfaz e **Eternatus** (nível 70) aparece, com a mensagem "Eternatus is here, brace yourself for annihilation". Há 2% de chance de ser Shiny.

O Casulo de Eternatus é localizado pelo Arc Phone usando a **Partícula de Galar**. (A Partícula de Galar é um minério/recurso próprio — veja o arquivo de Minérios e Materiais.)

## Hoopa: Fechadura do Templo, Pirâmide e Pedestal

**Hoopa** envolve a Pirâmide de Hoopa (Hoopa Pyramid), localizada pelo Arc Phone com um item específico. Dois elementos:

- **Fechadura do Templo** (Temple Lock): ativada com a **Chave do Templo** (Temple Key). Ao ser ativada, ela quebra paredes próximas e, num raio de 50 blocos, transforma os blocos especiais de invocação de Hoopa, fazendo aparecer um **Hoopa desvinculado (unbound), Shiny, nível 70, segurando uma Chave do Templo**.
- **Pedestal de Hoopa** (par de pedestais): usa **Chave do Templo** + **Garrafa-Prisão** (`mega_showdown:prison_bottle`) em dois pedestais. Invoca Hoopa e dá de recompensa uma **Garrafa-Prisão**.

A Chave do Templo (Temple Key) é, portanto, central para o conteúdo de Hoopa.

## Victini: Fechadura de Victini e Passe da Liberdade

**Victini** é invocado na **Fechadura de Victini** (Victini Lock), dentro da Ilha da Liberdade (Liberty Island).

- Clique na Fechadura de Victini segurando o **Passe da Liberdade** (Liberty Pass). Victini (nível 60) é invocado. Cada jogador só pode fazer isso uma vez por fechadura.
- O **Passe da Liberdade** é encontrado como tesouro: tem 25% de chance de aparecer nos baús de Pirâmide do Deserto. Ele também é o item usado para rastrear a **Ilha da Liberdade** pelo Arc Phone.

## Mew: Mapa do Mar Antigo e Ilha Final

**Mew** é invocado no **Pedestal de Mew**, dentro da Ilha Final (Final Island).

- Use o **Mapa do Mar Antigo** (Old Sea Map) no Pedestal de Mew para invocar Mew (nível 40). Recompensa: um **Tufo de Pelo de Mew** (Tuft of Mew Hair), descrito como contendo o DNA de todos os Pokémon.
- O **Mapa do Mar Antigo** é encontrado como tesouro: tem 50% de chance de aparecer nos baús de Templo da Selva. Ele é também o item usado para rastrear a **Ilha Final** pelo Arc Phone.

## Heatran: Pedra de Magma e Caverna de Heatran

**Heatran** é invocado no **Pedestal de Heatran**, dentro da Caverna de Heatran (que se gera no Nether).

- Use a **Pedra de Magma** (Magma Stone) no Pedestal de Heatran para invocar Heatran (nível 50).
- A Pedra de Magma é fabricada (3x3) com 8 Blocos de Magma (magma block) ao redor de 2 Sucatas de Netherita (netherite scrap) nas laterais do centro:
```
D D D
S D S
D D D
```
onde D = Bloco de Magma e S = Sucata de Netherita.
- A Pedra de Magma também é o item usado para rastrear a **Caverna de Heatran** pelo Arc Phone.

## Celebi: GS Ball e Santuário de Ilex

**Celebi** é invocado no **Santuário de Ilex** (Ilex Shrine) usando a **GS Ball**.

- Clique no Santuário de Ilex segurando a **GS Ball**. O santuário se desfaz e **Celebi** (nível 40) surge "do fluxo do tempo". Sem a GS Ball, o santuário avisa que está esperando uma pokébola especial.
- A **GS Ball** é fabricada (3x3) com 4 Apricorns Amarelos (`cobblemon:yellow_apricorn`) ao redor de 1 Sucata de Netherita no centro:
```
. U .
U R U
. U .
```
onde U = Apricorn Amarelo e R = Sucata de Netherita.
