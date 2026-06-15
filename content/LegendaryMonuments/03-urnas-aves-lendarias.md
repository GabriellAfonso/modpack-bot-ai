# Urnas e as Aves Lendárias (Articuno, Zapdos, Moltres)

## O que são as Urnas

As Urnas são itens portáteis do mod Legendary Monuments usados para invocar as aves lendárias de Kanto e suas formas de Galar. Cada urna está ligada a um Pokémon e a um tipo elemental. Você carrega a urna na mochila e a "carrega" de energia derrotando Pokémon selvagens do tipo certo; quando a urna enche, basta clicar com ela para invocar o lendário.

Existem três urnas normais e três urnas galarianas:

- **Urna das Brasas** (Urn of Embers): ligada a Moltres, tipo **Fogo**.
- **Urna das Tempestades** (Urn of Storms): ligada a Zapdos, tipo **Elétrico**.
- **Urna do Gelo** (Urn of Frost): ligada a Articuno, tipo **Gelo**.
- **Urna Galariana das Brasas** (Galarian Urn of Embers): Moltres de Galar, tipo **Sombrio**.
- **Urna Galariana das Tempestades** (Galarian Urn of Storms): Zapdos de Galar, tipo **Lutador**.
- **Urna Galariana do Gelo** (Galarian Urn of Frost): Articuno de Galar, tipo **Psíquico**.

## Como carregar e usar uma urna

A urna funciona assim:

- Sempre que um Pokémon **selvagem** (sem dono) for derrotado a até 32 blocos de você, se você tiver na mochila uma urna não cheia e o Pokémon derrotado for do **tipo** daquela urna, a urna ganha 1 ponto de progresso. Uma mensagem mostra o progresso atual (por exemplo "Progresso: 12/50").
- Cada urna só carrega com Pokémon do seu tipo: a Urna das Brasas só conta Pokémon de Fogo, a Urna do Gelo só conta Pokémon de Gelo, etc. As urnas galarianas usam o tipo da forma galariana (Sombrio, Lutador, Psíquico).
- **Urnas normais** precisam de **50 pontos** para encher. **Urnas galarianas** precisam de **75 pontos**.
- Quando a urna enche, aparece a mensagem de que ela está totalmente carregada. Aí você **clica com a urna** para invocar o Pokémon. A urna é consumida ao invocar.
- O lendário é invocado à sua frente com efeitos visuais e sonoros (raios para Zapdos, chamas para Moltres, neve para Articuno). As aves normais nascem no nível 40; as galarianas no nível 50. Há 2% de chance de ser Shiny.

A dica/tooltip da urna mostra o tipo exigido, o progresso atual e se ela já está pronta para invocar.

## Recompensa ao invocar as aves normais

Ao invocar uma ave lendária **normal**, você também recebe uma pedra elemental ligada a ela:

- Invocar **Moltres** dá a **Pedra Fundida** (Molten Stone).
- Invocar **Articuno** dá a **Pedra Ártica** (Arctic Stone).
- Invocar **Zapdos** dá a **Pedra do Raio** (Zap Stone).

Essas três pedras são usadas para fabricar a Pedra do Vórtice, necessária para invocar Lugia (veja a seção de receitas abaixo).

## Receitas das urnas

As três urnas normais usam o mesmo formato (3x3), trocando apenas a pedra elemental do centro:

- Cantos superiores e inferiores: Tijolo (brick) nas posições indicadas
- Laterais do meio: Pólvora (gunpowder)
- Centro: a pedra elemental do Cobblemon
- Posições inferiores dos cantos: Sucata de Netherita (netherite scrap)

Padrão exato (W = tijolo, A = pólvora, S = pedra elemental, U = sucata de netherita):
```
W W
A S A
W U W
```

- **Urna das Brasas**: pedra central = Pedra de Fogo (`cobblemon:fire_stone`).
- **Urna das Tempestades**: pedra central = Pedra do Trovão (`cobblemon:thunder_stone`).
- **Urna do Gelo**: pedra central = Pedra do Gelo (`cobblemon:ice_stone`).

### Urnas galarianas

Cada urna galariana é feita combinando, sem formato fixo (shapeless), a urna normal correspondente com uma **Maçã Dyna** (Dyna Apple):

- Urna das Brasas + Maçã Dyna = Urna Galariana das Brasas
- Urna das Tempestades + Maçã Dyna = Urna Galariana das Tempestades
- Urna do Gelo + Maçã Dyna = Urna Galariana do Gelo

A Maçã Dyna é um item nativo da região de Galar usado também para fabricar urnas galarianas.

## Pedra do Vórtice (Vortex Stone)

A Pedra do Vórtice é feita combinando, sem formato fixo, as três pedras obtidas ao invocar as aves normais:

- Pedra Fundida + Pedra do Raio + Pedra Ártica = Pedra do Vórtice

A Pedra do Vórtice prova que você derrotou (invocou) o trio de aves e te dá o direito de desafiar Lugia: ela é o item usado no Pedestal de Lugia e também o item necessário para rastrear o Templo de Lugia pelo Arc Phone.

## Blocos decorativos de urna

Além das urnas funcionais, o mod tem versões em bloco apenas decorativas (Urna das Brasas, das Tempestades, do Gelo e as galarianas correspondentes), feitas com tijolos, lingote de ferro e um ingrediente central simples (pólvora, gelo, redstone, carvão, gelo compactado, bloco de redstone, conforme o bloco). Esses blocos servem para decoração e fazem parte da ambientação dos monumentos.
