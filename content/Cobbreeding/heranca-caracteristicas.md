# Herança de Características Visuais e Formas Regionais

Além de IVs, Natureza e Habilidade, o breeding também herda **características visuais e formas especiais** do Pokémon filho. Essas características vêm sempre da **mãe** (ou do pai não-Ditto se um dos pais for Ditto).

## Formas Regionais

As formas regionais são herdadas diretamente dos pais, sem depender do bioma onde o Pasto está localizado. Isso é diferente do comportamento padrão do Cobblemon.

As formas regionais que podem ser herdadas:
- **Alolan** (forma de Alola)
- **Galarian** (forma de Galar)
- **Hisuian** (forma de Hisui)
- **Paldean** (forma de Paldea)

**Exemplo:** Uma Meowth de Galar (Galarian Meowth) colocada no Pasto gerará ovos de Meowth de Galar, independentemente de onde o Pasto esteja no mundo.

## Outras Características Herdáveis

Além das formas regionais, várias características cosméticas e especiais são transmitidas da mãe para o filho. A lista padrão inclui:

- **bagworm_cloak** — padrão de Burmy
- **color** — variação de cor
- **dance_style** — estilo de dança (Oricorio)
- **fish_stripes** — padrões de listras de Magikarp
- **striped** — listras genéricas
- **magikarp_jump** — padrão especial de Magikarp
- **mooshtank** — variação de Miltank
- **region_bias** — tendência regional
- **bull_breed** — variação de Tauros
- **tatsugiri_texture** — textura de Tatsugiri
- **whiscash_nero** — variação de Whiscash
- **wooper_heart** — variação de Wooper

O servidor pode adicionar ou remover características desta lista através da configuração `inheritedFeatures`.

## Casos Especiais de Formas

Alguns Pokémon têm regras especiais para herança de forma:

- **Sirfetch'd, Cursola, Obstagoon, Runerigus, Clodsire, Overqwil, Sneasler** → O ovo nasce na forma regional exclusiva correspondente (ex: ovo de Sirfetch'd gera Galarian Farfetch'd).
- **Perrserker, Basculegion** → O ovo nasce na forma regional correspondente.
- **Manaphy + Ditto** → O ovo nasce como **Phione**, não como Manaphy.
- **Nidoran-F e Nidoran-M** → Um casal produz ovos de ambos os gêneros de Nidoran simultaneamente.
- **Volbeat e Illumise** → Um casal produz ovos tanto de Volbeat quanto de Illumise.

## Pokébola Herdada

A **Pokébola** em que o filho nasce também é herdada:

- Por padrão, o filho nasce na **Pokébola da mãe**.
- Se os dois pais forem da **mesma espécie**, a Pokébola é escolhida aleatoriamente entre a dos dois pais.
- **Ditto não transmite sua Pokébola** — nesse caso, o filho herda a Pokébola do outro pai.
- **Cherish Ball e Master Ball** são substituídas por **Poké Ball comum** — o filho não pode nascer nessas pokébolas especiais.
