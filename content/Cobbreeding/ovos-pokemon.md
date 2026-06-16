# Ovos Pokémon — Chocagem e Comportamento

Quando um par de Pokémon compatíveis produz um ovo no Pasto, esse ovo aparece como um item que pode ser carregado no inventário do jogador. Este guia explica como os ovos funcionam depois que você os pega.

## Como pegar um ovo

Clique na **parte inferior do bloco de Pasto** para coletar os ovos gerados. O Pasto pode armazenar até 5 ovos ao mesmo tempo (valor padrão configurável pelo servidor). Hoppers posicionados sob o Pasto podem coletar os ovos automaticamente.

## Aparência dos ovos

Por padrão, todos os ovos têm a mesma aparência visual genérica. Passe o mouse sobre o ovo no inventário para ver o **nome do Pokémon** que está dentro e o **tempo restante para chocar**.

Se o servidor ativar a opção de **cores personalizadas**, os ovos terão aparências diferentes conforme o tipo do Pokémon contido — por exemplo, ovos de Pokémon do tipo Fogo terão cor avermelhada.

## Como chocar um ovo

- O ovo **só choca enquanto estiver no inventário de um jogador**. Se estiver em um baú ou no chão, o timer para.
- A cada segundo que o jogador está ativo no mundo, o timer do ovo diminui.
- Quando o timer chega a zero, o Pokémon nasce automaticamente e vai para a **party** do jogador (ou para o PC se a party estiver cheia).
- O Pokémon nascido começa com **120 de amizade (friendship)**.

## Tempo de chocagem

O tempo depende do **número de ciclos de ovo** da espécie. Cada ciclo equivale a 600 ticks de timer. Com o multiplicador padrão (1.0):

- Espécie com 5 ciclos → timer de 3.000 ticks → **~2,5 minutos**
- Espécie com 20 ciclos → timer de 12.000 ticks → **~10 minutos**
- Espécie com 40 ciclos → timer de 24.000 ticks → **~20 minutos**

O servidor pode aplicar um multiplicador ao tempo de chocagem. Multiplicador menor que 1.0 acelera o processo; multiplicador maior o desacelera.

## Acelerando a chocagem com habilidades

Se qualquer Pokémon na sua **party** tiver uma das seguintes habilidades, os ovos no seu inventário chocam **duas vezes mais rápido**:

- **Flame Body** (Corpo de Chama)
- **Magma Armor** (Armadura de Magma)
- **Steam Engine** (Motor a Vapor)

O Pokémon com a habilidade precisa estar na party — não adianta estar no Pasto ou no PC.

## Informações escondidas no ovo

Por padrão, os dados do Pokémon dentro do ovo são **criptografados** para que o jogador não saiba exatamente o que vai chocar antes do nascimento. Apenas o nome da espécie é visível no tooltip.

Se o servidor desabilitar a criptografia (opção `eggEncryptionEnabled`), você pode clicar com o botão direito no ovo para descriptografar e ver todos os dados do Pokémon (apenas recomendado para single player ou servidores que queiram essa transparência).

## Casos especiais no nascimento

- **Wooloo e Mareep** nascem sem lã e precisam crescer para ficar com ela.
- **Pokémon com formas regionais** nascem na forma correta conforme herdada dos pais.
