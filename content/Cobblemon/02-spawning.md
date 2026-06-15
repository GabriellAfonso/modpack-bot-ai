# Spawning — Como Pokémon Aparecem no Mundo

Pokémon aparecem naturalmente no mundo com base em condições específicas: bioma, hora do dia, clima, altura, blocos ao redor e outros fatores. Cada espécie tem suas próprias condições de spawn definidas.

---

## Condições de Spawn

Cada Pokémon exige condições específicas. As mais comuns são:

- **Bioma** — a maioria dos Pokémon só aparece em biomas específicos (ex: Bulbasaur só aparece em florestas e ilhas tropicais).
- **Luz solar (skylight)** — alguns precisam de luz alta (superfície de dia), outros de escuridão (cavernas).
- **Hora do dia** — alguns só à noite, outros só de dia, alguns a qualquer hora.
- **Clima** — chuva ou trovão pode ser condição para certos Pokémon.
- **Altura (Y)** — alguns Pokémon só aparecem em Y alto, outros nas profundezas.
- **Blocos próximos** — alguns precisam de blocos específicos embaixo ou ao redor (gramado, água, lava, redstone, etc.).
- **Estruturas** — alguns Pokémon só aparecem dentro de estruturas (cidade antiga, mansão, pirâmide, etc.).
- **Fase da lua** — alguns dependem da fase lunar.

---

## Tipos de Posição de Spawn

- **Grounded** — no chão, superfície sólida.
- **Submerged** — dentro da água.
- **Seafloor** — no fundo do mar.
- **Surface** — na superfície da água.
- **Airborne** — no ar.

---

## Presets de Spawn (Ambientes)

Pokémon usam "presets" que agrupam condições comuns. Exemplos:

| Preset | Onde aparecem |
|--------|--------------|
| `natural` | Em blocos naturais (não farmland) |
| `water` | Em água |
| `lava` | Em lava |
| `foliage` | Em vegetação |
| `urban` | Perto de construções |
| `redstone` | Perto de redstone |
| `webs` | Perto de teias |
| `treetop` | No topo de árvores |
| `ancient_city` | Dentro de cidades antigas |
| `mansion` | Dentro de mansões |
| `stronghold` | Dentro de fortalezas |

---

## Buckets de Raridade

Cada Pokémon tem um "bucket" (balde) de raridade que define o peso de spawn:

| Bucket | Descrição |
|--------|-----------|
| `common` | Muito frequente |
| `uncommon` | Moderado |
| `rare` | Raro |
| `ultra-rare` | Muito raro |

Bulbasaur, por exemplo, é `ultra-rare` e só aparece em florestas/ilhas tropicais com luz solar de dia.

---

## Taxa de Spawn

- **1 Pokémon por chunk** ao redor do jogador (raio de 16 a 64 blocos).
- Tentativa de spawn a cada **1 segundo** (20 ticks).
- Máximo de **8 spawns por ciclo**.
- Pokémon surgem entre **16 e 64 blocos** de distância do jogador.

---

## Despawn

Pokémon selvagens desaparecem automaticamente quando:
- Ficam a mais de **160 blocos** do jogador mais próximo.
- Atingem a idade máxima (entre **5 e 10 minutos** após spawnar).
- Mínimo de **5 minutos** para despawn (não desaparecem instantaneamente).

---

## Spawn em Estruturas Específicas

Alguns Pokémon só aparecem dentro de estruturas geradas pelo mundo:
- **Cidade Antiga** — Pokémon sombrios ou especiais.
- **Mansão** — Pokémon dos quartos, sala de jantar e outros cômodos.
- **Pirâmide do Deserto / da Selva** — Pokémon de terrenos secos e tropicais.
- **Monumento Oceânico** — Pokémon aquáticos de nível alto.
- **Fortaleza (Stronghold)** — Pokémon de dungeon.
- **Portal em Ruínas** — Pokémon próximos a portais.
- **Estruturas do Nether** — Pokémon especiais do submundo.
- **Cidade do End** — Pokémon do End.
