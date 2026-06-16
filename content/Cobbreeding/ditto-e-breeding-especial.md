# Ditto e Casos Especiais de Breeding

O **Ditto** é um Pokémon único que pode se reproduzir com praticamente qualquer espécie, inclusive aquelas que normalmente não têm gênero. Este guia explica as regras de breeding com Ditto e os casos especiais do mod.

## Ditto + Pokémon comum

Ditto pode se reproduzir com qualquer Pokémon que **não pertença** ao Egg Group **Undiscovered** e que também **não seja Ditto**. Isso inclui:

- Pokémon sem gênero (como Staryu, Magnemite, etc.)
- Pokémon 100% machos ou 100% fêmeas de certas espécies

Quando Ditto está no par, ele age como o "parceiro neutro" — a espécie e a forma do filho vêm do outro Pokémon (não do Ditto), e a habilidade/Pokébola/características também vêm do **pai não-Ditto**.

**Manaphy + Ditto** é um caso especial: o filho sempre será **Phione**, nunca Manaphy.

## Ditto + Ditto

Por padrão, **dois Dittos não produzem ovos**. Essa mecânica pode ser ativada pelo servidor com a opção `dittoAndDittoRandomEgg`.

Quando ativada, dois Dittos no Pasto produzem ovos de **espécies aleatórias**. A espécie só é revelada quando o ovo choca. O servidor pode controlar quais categorias de Pokémon podem aparecer:

- **Pokémon comuns:** sempre permitidos (quando ativado).
- **Lendários e Míticos:** desativados por padrão (`dittoAndDittoAllowLegendary`).
- **Pokémon Paradoxo:** desativados por padrão (`dittoAndDittoAllowParadox`).
- **Ultra Beasts:** desativados por padrão (`dittoAndDittoAllowUltraBeast`).
- **Grupo Undiscovered:** desativados por padrão (`dittoAndDittoAllowUndiscovered`).

Ovos gerados por Ditto + Ditto não herdam nenhuma característica específica dos pais (IVs, Natureza, etc.) além das estatísticas básicas calculadas pelo sistema.

## Pokémon que não podem se reproduzir

Pokémon do **Egg Group Undiscovered** nunca produzem ovos por breeding normal. Isso inclui Pokémon bebê (como Magby, Elekid, Togepi), lendários, míticos, Pokémon Paradoxo e Ultra Beasts.

A única exceção é via **Ditto + Ditto com a opção especial ativada** pelo servidor, que pode incluir essas categorias.

## Pokémon marcados como Neutered

Qualquer Pokémon pode ser individualmente bloqueado de participar do breeding através da função **Neutered**, ativável pelo treinador original na interface do Pasto. Pokémon neutered são ignorados pelo sistema de breeding mesmo estando no Pasto com parceiros compatíveis.

## Herança com Ditto

Quando Ditto é um dos pais:
- **Espécie do filho:** sempre a do Pokémon não-Ditto (na forma bebê, se houver).
- **Habilidade:** herdada do Pokémon não-Ditto.
- **Pokébola:** herdada do Pokémon não-Ditto (Ditto não transmite sua Pokébola).
- **Formas regionais:** herdadas do Pokémon não-Ditto.
- **IVs e Natureza:** herança normal (Power Items e Destiny Knot funcionam em ambos os pais).
