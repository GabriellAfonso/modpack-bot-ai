# Cobbreeding — Visão Geral

Cobbreeding é um addon para o mod Cobblemon que adiciona reprodução de Pokémon ao jogo. Com ele, você pode colocar dois Pokémon compatíveis no **bloco de Pasto** (Pasture Block) para que produzam ovos, exatamente como no breeding dos jogos principais da série Pokémon.

## O que o mod adiciona

- Pokémon compatíveis no Pasto colocam ovos automaticamente ao longo do tempo.
- Os ovos aparecem na parte inferior do bloco de Pasto e podem ser pegos de lá.
- Ovos carregados no inventário do jogador chocam conforme o tempo passa.
- Herança de IVs, Natureza, Habilidade, Egg Moves, Pokébola e características visuais (formas regionais, padrões, etc.).
- Suporte a Método Masuda e outros métodos de shiny hunting por breeding.
- Mirror Herb ensina Egg Moves diretamente no Pasto, sem precisar colocar no moveset do pai.
- Pokémon com Chama ou habilidades similares aceleram a chocagem dos ovos.

## Fluxo básico de uso

1. **Coloque dois Pokémon compatíveis no Pasto.** Eles precisam compartilhar ao menos um Egg Group e ser um macho e uma fêmea — ou um dos dois ser um Ditto.
2. **Ative o breeding no Pasto** clicando no botão de breeding dentro da interface do Pasto.
3. **Aguarde.** Após entre 8.000 e 14.000 ticks (aproximadamente 6 a 12 minutos), um ovo aparecerá na base do bloco de Pasto.
4. **Pegue o ovo** clicando na parte inferior do Pasto.
5. **Carregue o ovo no inventário.** Ele só choca enquanto estiver no inventário de um jogador. O tempo de chocagem varia conforme o número de ciclos de ovo da espécie — um Pokémon com 20 ciclos leva cerca de 10 minutos para chocar sem auxílio.
6. **O Pokémon nascerá automaticamente** ao fim do timer, indo direto para a party ou PC do jogador.

## Compatibilidade de breeding

Para que dois Pokémon possam ter ovos juntos:
- Precisam compartilhar ao menos um **Egg Group** em comum.
- Devem ser de **gêneros opostos** (macho + fêmea), ou um deles deve ser **Ditto**.
- Nenhum dos dois pode estar no Egg Group **Undiscovered** (grupo de Pokémon que não se reproduzem).
- Nenhum dos dois pode estar marcado como **neutered** (veja o arquivo sobre o Pasto).

Pokémon com gênero desconhecido (como Magnemite) podem se reproduzir apenas com Ditto.

## O que é herdado

- **IVs:** 3 IVs herdados dos pais por padrão (5 com Destiny Knot equipado).
- **Natureza:** herdada de um dos pais caso ele segure uma Everstone; aleatória caso nenhum segure.
- **Habilidade:** herdada da mãe (ou do pai não-Ditto) com chance de mudar de slot ou virar Hidden Ability.
- **Egg Moves:** todos os moves que os pais possam aprender no Egg Moves da espécie-filho.
- **Pokébola:** herdada da mãe; se os dois pais forem da mesma espécie, escolhida aleatoriamente de um dos dois.
- **Formas regionais e características visuais:** herdadas da mãe (Alolan, Galarian, Hisuian, Paldean, padrões de Magikarp, etc.).
- **Brilho (Shiny):** calculado via Método Masuda, Crystal ou outros configuráveis pelo servidor.
