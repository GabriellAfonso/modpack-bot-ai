# Spawn Pools Personalizados — Pokémon das Máquinas Spawner

Máquinas do tipo **spawner** (como a Strange Crystallized Machine) e bolas como as Gacha Balls e Rocket Ball usam **spawn pools** para decidir qual Pokémon aparecer. O servidor pode customizar esses pools via datapack.

---

## O que são os spawn pools

Um spawn pool é uma lista de Pokémon que pode aparecer quando uma máquina spawner é ativada ou quando uma Gacha Ball / Rocket Ball é usada. Cada Pokémon tem uma raridade (bucket), um peso e uma faixa de nível.

Se uma máquina spawner não tiver pool configurado, ela usa os spawns normais do mundo do Cobblemon.

---

## Como os Pokémon são escolhidos

A escolha acontece em duas etapas:

**Etapa 1 — Sortear o bucket:**
Primeiro o sistema sorteia qual "bucket" (categoria de raridade) será usado, com base nos pesos dos buckets.

| Bucket | Peso padrão | Chance aproximada |
|---|---|---|
| common | 100 | ~61,7% |
| uncommon | 40 | ~24,7% |
| rare | 15 | ~9,3% |
| ultra_rare | 5 | ~3,1% |
| legendary | 1 | ~0,6% |

**Etapa 2 — Sortear o Pokémon dentro do bucket:**
Depois, o sistema pega todos os Pokémon do bucket sorteado que correspondem ao bioma atual do jogador e sorteia um com base nos pesos individuais de cada espécie.

---

## Pools disponíveis por padrão

### Strange Crystallized Machine (gacha_machine_4)
Pool com Pokémon de todas as regiões, organizados em subpastas por região: kanto, johto, hoenn, sinnoh, unova, kalos, alola, galar, hisui, paldea. Inclui centenas de espécies com raridades variadas.

### Gacha Balls 1–6
Cada bola tem seu próprio pool. Por padrão contém apenas alguns exemplos (Caterpie, Pidgey, Rattata). O servidor deve configurar pools completos via datapack.

### Rocket Ball
Pool com Pokémon de todas as regiões, similar ao da Strange Crystallized Machine mas com seleção temática do Team Rocket.

---

## Filtro por bioma

Cada entrada no pool pode ter uma lista de biomas opcional. Se especificado, o Pokémon só aparece quando o jogador está naquele bioma. Se não tiver bioma definido, o Pokémon pode aparecer em qualquer lugar.

Isso permite criar pools onde Pokémon de água só aparecem em biomas de oceano, por exemplo.

---

## Estrutura de um arquivo de spawn pool (para referência de datapack)

Os arquivos ficam em `data/cobbledgacha/spawn_pool_files/{pool_key}/{nome_arquivo}.json`.

Exemplo de arquivo para o pool da Gacha Ball 1 (`gacha_ball_1/rattata.json`):
```json
{
  "spawns": [
    {
      "species": "rattata",
      "bucket": "uncommon",
      "weight": 8,
      "minLevel": 1,
      "maxLevel": 25
    }
  ]
}
```

Exemplo com filtro de bioma:
```json
{
  "spawns": [
    {
      "species": "magikarp",
      "bucket": "common",
      "weight": 10,
      "minLevel": 5,
      "maxLevel": 20,
      "biomes": ["minecraft:ocean", "minecraft:river"]
    }
  ]
}
```

Campos obrigatórios:
- `species` — nome do Pokémon (ex: "pikachu", "eevee")
- `bucket` — categoria de raridade: "common", "uncommon", "rare", "ultra_rare", "legendary"
- `weight` — peso dentro do bucket (número inteiro, maior = mais frequente)
- `minLevel` e `maxLevel` — faixa de nível (sorteado aleatoriamente nessa faixa)

Campos opcionais:
- `biomes` — lista de IDs de bioma; se ausente, spawna em qualquer bioma

---

## Pesos de bucket por pool

Cada pool pode ter seus próprios pesos de bucket, diferentes dos padrões globais. Isso é configurado via um arquivo `_buckets.json` dentro da pasta do pool:

`data/cobbledgacha/spawn_pool_files/gacha_machine_4/_buckets.json`:
```json
{
  "common": 100,
  "uncommon": 40,
  "rare": 10,
  "legendary": 1
}
```

Se não houver `_buckets.json`, usa os pesos definidos em `server_config.json` (se houver) ou os pesos padrão do mod.

---

## Override de datapack

Se um arquivo `_override.json` existir em `data/cobbledgacha/spawn_pool_files/`, o mod ignora todos os pools do mod base e usa apenas os pools definidos em datapacks externos. Isso permite que o servidor substitua completamente os pools sem conflito.
