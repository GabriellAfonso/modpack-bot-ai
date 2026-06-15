# Pedestais de Invocação de Lendários

## Como funcionam os pedestais

Os Pedestais são blocos do mod Legendary Monuments onde você coloca um item específico para invocar um Pokémon Lendário. A maioria dos lendários do mod é invocada desta forma. O funcionamento básico é:

- Clique no pedestal com o **item de invocação correto na mão**. O item é colocado sobre o pedestal e, se for o item certo, dispara a invocação.
- Em modo sobrevivência, o item de invocação é consumido. Em modo criativo não é gasto.
- Cada pedestal guarda quem já o usou: **um mesmo jogador só pode usar cada pedestal uma vez**. Se tentar de novo, recebe a mensagem "This pedestal has already been used by you."
- Se você clicar no pedestal de mãos vazias (e não estiver agachado), pega de volta o item que estiver em cima dele.
- O lendário sempre aparece logo acima do pedestal, com 2% de chance de ser Shiny e com pelo menos 3 IVs perfeitos.

Existem dois tipos de pedestal: os **simples** (um único item invoca o lendário) e os **duplos** (precisam de dois pedestais ativados ao mesmo tempo com itens complementares).

## Pedestais simples e o que cada um pede

Cada pedestal aceita um item específico e, muitas vezes, dá uma recompensa que abre o próximo passo da progressão:

- **Pedestal de Entei**: usa o Petisco de Entei (Entei Treat), nível 40. Dá uma **Pena Vermelha** (Red Feather).
- **Pedestal de Suicune**: usa o Petisco de Suicune (Suicune Treat), nível 40. Dá uma **Pena Azul** (Blue Feather).
- **Pedestal de Raikou**: usa o Petisco de Raikou (Raikou Treat), nível 40. Dá uma **Pena Amarela** (Yellow Feather).
- **Pedestal de Ho-Oh**: usa a Pena Arco-Íris (Rainbow Feather), nível 60. O Ho-Oh aparece segurando **Cinzas Sagradas** (Sacred Ash).
- **Pedestal de Lugia**: usa a Pedra do Vórtice (Vortex Stone), nível 60. Dá uma **Chave de Lugia** (Lugia Key).
- **Pedestal de Latias/Latios** (Lati Pedestal): usa o Petisco de Latias ou o Petisco de Latios, nível 50. Invoca Latias ou Latios conforme o petisco usado.
- **Pedestal de Heatran**: usa a Pedra de Magma (Magma Stone), nível 50.
- **Pedestal de Mew**: usa o Mapa do Mar Antigo (Old Sea Map), nível 40. Dá um **Tufo de Pelo de Mew** (Tuft of Mew Hair).
- **Pedestal de Palkia**: usa a Corrente Vermelha (Red Chain), nível 70. Dá um **Globo do Espaço** (Space Globe).
- **Pedestal de Dialga**: usa a Corrente Vermelha (Red Chain), nível 70. Dá um **Globo do Tempo** (Time Globe).
- **Pedestal de Giratina**: usa o Orbe Griseu (`mega_showdown:griseous_orb`), nível 70. Dá um **Globo de Antimatéria** (Antimatter Globe) e quebra todo o vidro num raio de 50 blocos ao redor.

Importante sobre a Corrente Vermelha: nos pedestais de Palkia e Dialga, ao usar a Corrente Vermelha ela vira uma **Corrente Vermelha Fragmentada** (em vez de simplesmente sumir), que depois pode ser consertada.

## Pedestais duplos (dois pedestais ativados juntos)

Alguns lendários exigem dois pedestais próximos (num raio de 10 blocos), cada um recebendo um item complementar. Você ativa um pedestal com um item e o outro pedestal precisa já estar com o item complementar; quando os dois combinam, o lendário (nível 60) é invocado entre eles. Se você ativar só um, o celular/jogo avisa "You sense that another pedestal must be activated nearby...".

Pares de itens e recompensas:

- **Reshiram** (par de pedestais): Pedra Clara (Lightstone) + Gema de Fogo (`cobblemon:fire_gem`). Dá uma **Garrafa da Verdade** (Truth Bottle).
- **Zekrom** (par de pedestais): Pedra Escura (Darkstone) + Gema Elétrica (`cobblemon:electric_gem`). Dá uma **Garrafa dos Ideais** (Ideals Bottle).
- **Kyurem** (par de pedestais): Garrafa da Verdade (Truth Bottle) + Garrafa dos Ideais (Ideals Bottle). Por isso é preciso invocar Reshiram e Zekrom antes, para ganhar as duas garrafas.
- **Zacian** (par de pedestais): Totem da Imortalidade (totem of undying) + Espada Enferrujada (`mega_showdown:rusted_sword`). Dá de volta uma **Espada Enferrujada**.
- **Zamazenta** (par de pedestais): Totem da Imortalidade + Escudo Enferrujado (`mega_showdown:rusted_shield`). Dá de volta um **Escudo Enferrujado**.
- **Hoopa** (par de pedestais): Chave do Templo (Temple Key) + Garrafa-Prisão (`mega_showdown:prison_bottle`). Dá uma **Garrafa-Prisão**.

## Configuração dos itens dos pedestais

Os itens que cada pedestal aceita podem ser alterados por administradores de servidor num arquivo de configuração gerado automaticamente em `config/LegendaryMonuments/pedestals.json`. Os valores padrão são:

- Entei = `entei_treat`, Raikou = `raikou_treat`, Suicune = `suicune_treat`
- Heatran = `magma_stone`, Ho-Oh = `rainbow_feather`, Lugia = `vortex_stone`
- Latias = `latias_treat`, Latios = `latios_treat`
- Hoopa = `temple_key` + `mega_showdown:prison_bottle`
- Zekrom = `darkstone` + `cobblemon:electric_gem`; Reshiram = `lightstone` + `cobblemon:fire_gem`
- Kyurem = `truthbottle` + `idealsbottle`
- Zacian = `totem_of_undying` + `mega_showdown:rusted_sword`; Zamazenta = `totem_of_undying` + `mega_showdown:rusted_shield`

Trocar esses valores muda quais itens são aceitos em cada pedestal, sem alterar o resto da mecânica.

## Onde conseguir os pedestais

Todos os pedestais (Pedestal comum e os pedestais específicos de cada lendário) estão disponíveis na aba criativa "Legendary Monuments" do mod. Em jogo normal, eles já vêm posicionados dentro das estruturas/monumentos gerados no mundo, prontos para serem usados.
