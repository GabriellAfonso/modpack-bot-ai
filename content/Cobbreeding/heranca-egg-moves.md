# Herança de Egg Moves e Mirror Herb

**Egg Moves** são golpes especiais que um Pokémon só pode aprender ao nascer de um ovo, desde que um dos pais saiba esse golpe. O Cobbreeding implementa essa mecânica com uma diferença importante em relação aos jogos principais.

## Como funciona a herança de Egg Moves

Para que o filho herde um Egg Move:
1. O golpe precisa estar na **lista de Egg Moves** da espécie filha.
2. Pelo menos um dos pais precisa **ser capaz de aprender** esse golpe (não precisa estar no moveset ativo — qualquer golpe que o pai já tenha aprendido ou possa aprender conta).

Isso é diferente dos jogos principais, onde o pai precisa ter o move equipado no moveset. Aqui, **todos os moves já aprendidos pelos pais contam automaticamente**, sem precisar colocá-los nos 4 slots ativos.

## Mirror Herb — Ensinando Egg Moves no Pasto

O **Mirror Herb** (Erva Espelho) permite que um Pokémon aprenda Egg Moves diretamente dentro do Pasto, copiando golpes dos companheiros ali presentes.

**Como usar:**
1. Equipe o **Mirror Herb** no Pokémon que você quer que aprenda o Egg Move.
2. Coloque esse Pokémon no Pasto junto com outro Pokémon que saiba o golpe desejado.
3. Aguarde. A cada **600 ticks (~30 segundos)**, o mod verifica os Pokémon no Pasto com Mirror Herb e ensina os Egg Moves aplicáveis.
4. O Pokémon não precisa ter o move equipado no moveset — qualquer golpe aprendido anteriormente que o portador do Mirror Herb possa aprender como Egg Move será transmitido.

**Importante:** os dois Pokémon não precisam ser compatíveis para breeding — Mirror Herb funciona com qualquer combinação de Pokémon no Pasto.

## Volt Tackle para Pichu

Existe um caso especial: se qualquer um dos pais estiver segurando uma **Light Ball** durante o breeding de um **Pichu**, o Pichu nascerá com **Volt Tackle** em seu moveset, exatamente como nos jogos principais.
