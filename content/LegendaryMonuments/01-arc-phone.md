# Arc Phone (Celular Arceus)

## O que é o Arc Phone

O Arc Phone é um item-celular do mod Legendary Monuments que funciona como central de utilidades do jogador. Ao usá-lo (clique direito segurando o item), ele abre uma tela com vários aplicativos. É o item mais importante do mod para a maioria dos jogadores, porque é por ele que você localiza as estruturas dos lendários, consulta seus itens-chave guardados, cura sua equipe e acessa baú e PC à distância. O Arc Phone é um item raro (raridade épica) e ocupa apenas 1 por pilha.

## Como obter o Arc Phone

O Arc Phone é fabricado em mesa de trabalho com a seguinte receita (formato 3x3):

- Linha de cima: Lingote de Ferro, Lingote de Ouro, Lingote de Ferro
- Linha do meio: Lingote de Ouro, **Cristal do End** (end crystal), Lingote de Ouro
- Linha de baixo: Lingote de Ferro, **tela de Pokédex** (qualquer item da tag `cobblemon:pokedex_screen`), Lingote de Ferro

Resultado: 1 Arc Phone.

## Aplicativos sempre disponíveis

Estes aplicativos vêm desbloqueados desde o começo, sem custo:

- **Map (Mapa)**: abre um mapa para navegação.
- **Legendary Tracking (Rastreamento de Lendários)**: localiza as estruturas do mod. Veja a seção abaixo.
- **Key Items (Itens-Chave)**: abre um inventário especial de até 63 espaços para guardar seus itens-chave de invocação. Itens guardados aqui contam como "tê-los" para liberar o rastreamento de estruturas, mesmo que não estejam na sua mochila normal.
- **System Upgrades (Melhorias de Sistema)**: tela onde você desbloqueia os aplicativos extras pagando com itens. Veja a seção abaixo.
- **Settings (Configurações)**: ajustes do celular.

## Aplicativos que precisam ser desbloqueados

Quatro aplicativos extras só ficam disponíveis depois de comprados na tela "System Upgrades", gastando itens da sua mochila. Cada desbloqueio consome **1 Upgrade do Cobblemon** (`cobblemon:upgrade`) mais um item específico:

- **PC**: custa 1 Upgrade + 1 PC do Cobblemon. Abre seu PC de Pokémon à distância.
- **Pokédex**: custa 1 Upgrade + 1 Pokédex Branca (`cobblemon:pokedex_white`). Abre a Pokédex.
- **Heal (Cura)**: custa 1 Upgrade + 1 Máquina de Cura (`cobblemon:healing_machine`). Permite curar toda a equipe à distância.
- **Ender Chest (Baú do End)**: custa 1 Upgrade + 1 Baú do End (ender chest). Abre seu baú do End à distância.

Se você não tiver os itens necessários na mochila ao tentar desbloquear, o celular avisa que faltam itens e nada é gasto. Esses desbloqueios ficam salvos por jogador e são mantidos entre sessões.

## Aplicativo Heal: cura de equipe e suas regras

Depois de desbloqueado, o aplicativo Heal cura completamente todos os HP e PP da sua equipe de Pokémon. Regras importantes:

- Há um tempo de espera (cooldown) de **600 segundos (10 minutos)** entre cada cura. Se você tentar curar antes disso, o celular mostra quantos segundos ainda faltam.
- Você **não pode** curar enquanto estiver em batalha. O celular avisa "You cannot heal your Pokémon while in battle!".

## Aplicativo Legendary Tracking: localizar estruturas

O aplicativo Legendary Tracking encontra a estrutura do mod mais próxima de você e mostra sua localização. Para a maioria das estruturas, você só consegue rastreá-las se estiver **segurando ou guardando no app Key Items** o item-chave exigido por aquela estrutura. Se você não tiver o item exigido, o rastreamento responde que a estrutura não foi encontrada.

Itens necessários para rastrear cada estrutura (os confirmados):

- **Dragonspiral Tower** (Torre Espiral do Dragão): exige Fragmento de Pedra Clara (Light Stone Shard).
- **Vila de Ecruteak** (vila tradicional): exige Sino Claro (Clear Bell).
- **Caverna de Heatran**: exige Pedra de Magma (Magma Stone).
- **Santuário Firescourge**: exige Selo Firescourge (Firescourge Seal).
- **Santuário Grasswither**: exige Selo Grasswither (Grasswither Seal).
- **Santuário Groundblight**: exige Selo Groundblight (Groundblight Seal).
- **Santuário Icerend**: exige Selo Icerend (Icerend Seal).
- **Templo de Lugia**: exige Pedra do Vórtice (Vortex Stone).
- **Casulo de Eternatus**: exige Partícula de Galar (Galar Particle).
- **Caverna de Kyurem**: exige Garrafa dos Ideais (Ideals Bottle).
- **Ilha de Giratina**: exige Lingote de Origem (Origin Ingot).
- **Ilha Final**: exige Mapa do Mar Antigo (Old Sea Map).
- **Templo de Snowpoint**: exige Sucata de Golem (Golem Scrap).
- **Pilar da Lança (Spear Pillar)**: exige Corrente Vermelha (Red Chain).
- **Ilha da Liberdade**: exige Passe da Liberdade (Liberty Pass).

O rastreamento procura num raio enorme (cerca de 20.000 blocos) e tem uma lógica para não te mandar repetidamente à mesma estrutura já concluída: se você marcar uma estrutura como concluída, o app procura uma estrutura diferente do mesmo tipo em volta de você.
