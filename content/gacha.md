# Cobbled Gacha — máquinas de gacha (moedas, cápsulas, recompensas, Gacha Balls)

Cobbled Gacha adiciona **máquinas de gacha** ao Minecraft integradas ao Cobblemon. Você insere moedas, a máquina dispensa recompensas aleatórias — cápsulas com itens do Cobblemon, Pokémon spawnados, ou pelúcias decorativas.

---

## Como usar uma máquina

1. Segure a moeda correta na mão principal e clique com o botão direito na máquina.
2. Cada clique insere uma moeda. Um contador `[x/max]` aparece na action bar.
3. Ao completar o custo, a máquina dispensa a recompensa na direção que ela está virada.
4. **Atalho:** segurar a moeda na mão secundária (off-hand) insere todas as moedas necessárias de uma vez.

Se aparecer a mensagem *"Invalid currency inserted"*, você está usando a moeda errada. Se aparecer *"Hold on! You can use this machine again in Xs"*, a máquina está em cooldown para você.

---

## As Máquinas

| Máquina | Moeda | Custo | O que dá |
|---|---|---|---|
| **Poké Gacha Machine** | Poké Gacha Coin (ou Relic Coin diretamente) | 5 | Cápsulas série A |
| **Cram O' Matic** | Erratic Gacha Coin | 20 | Poké Balls variadas + held items |
| **Item Printer** | Blueberry Gacha Coin | 20 | Cápsulas série C |
| **Strange Crystallized Machine** | Tera Gacha Coin | 5 | **Spawna um Pokémon** (não dá item) |
| **Citrine Gacha Machine** | Citrine Gacha Coin | 5 | Cápsulas |
| **Verdant Gacha Machine** | Verdant Gacha Coin | 5 | Cápsulas |
| **Azure Gacha Machine** | Azure Gacha Coin | 5 | Cápsulas |
| **Roseate Gacha Machine** | Roseate Gacha Coin | 5 | Cápsulas |
| **Slate Gacha Machine** | Slate Gacha Coin | 5 | Cápsulas |
| **Premier Gacha Machine** | Premier Gacha Coin | 5 | Cápsulas |
| **Rocket Prize Master** | Koban Coin | 1 | Rocket Ball (para spawnar Pokémon) |
| **Plush-O-Matic** | Yarn (tipo específico) | 3 | Pelúcia de Pokémon (requer PokeBlocks) |

> As máquinas Citrine, Verdant, Azure, Roseate, Slate e Premier são variantes visuais da Poké Gacha Machine — funcionam igual, só mudam a aparência e a moeda.

---

## Como obter as moedas

### Poké Gacha Coin
**Craft (sem forma):** Relic Coin + Red Dye  
*(A Relic Coin também pode ser inserida direto na Poké Gacha Machine sem precisar craftear a coin.)*

### Koban Coin
Matar **Meowth** tem **7.5% de chance** de dropar um Koban Coin.

### Yarns (Plush-O-Matic)
Craft em formato de L com: **Wool (lã) + Gem do tipo + String (barbante)**

| Yarn | Gem usada |
|---|---|
| Plain Yarn | Normal Gem |
| Fiery Yarn | Fire Gem |
| Frosty Yarn | Ice Gem |
| Soggy Yarn | Water Gem |
| Sparky Yarn | Electric Gem |
| Grassy Yarn | Grass Gem ou Bug Gem |
| Feathery Yarn | Flying Gem |
| Hardy Yarn | Fighting, Ground, Rock ou Steel Gem |
| Toothy Yarn | Dragon Gem |
| Creepy Yarn | Dark Gem, Ghost Gem ou Poison Gem |
| Fantasy Yarn | Fairy Gem ou Psychic Gem |

### Outras moedas
Craftadas de forma similar à Poké Gacha Coin — verifique as receitas no inventário criativo ou JEI.

---

## Receitas das máquinas

### Poké Gacha Machine
```
Ferro   Ferro   Ferro
Vidro   PokéBall Vidro
Ferro  Dispenser  Ferro
```

### Plush-O-Matic
```
Lã   Dispenser   Lã
Alavanca  PokéBall  ·
Ferro  OuroBlock  Ferro
```

---

## Cápsulas — Conteúdo por raridade

A **Poké Gacha Machine** dispensa uma cápsula aleatória com as seguintes chances:

| Cápsula | Chance |
|---|---|
| **Poké Capsule** (comum) | 51% |
| **Great Capsule** | 24% |
| **Ultra Capsule** | 15% |
| **Master Capsule** | 7% |
| **Cherish Capsule** (raríssima) | 3% |

Cada cápsula, ao ser usada (clique direito), abre e dá **um item aleatório** da sua pool.

---

### Poké Capsule — 51% de chance de sair da máquina

Pool com ~130 itens. Um item aleatório de igual peso:

- **Berries comuns:** Cheri, Chesto, Pecha, Rawst, Aspear, Oran, Sitrus, e muitas outras (quantidade: 4 de cada)
- **Apricorns:** Black, Blue, Green, Pink, Red, White, Yellow — 10 unidades cada (+ sementes: 5 cada)
- **Pedras de evolução:** Fire Stone, Water Stone, Thunder Stone, Leaf Stone, Moon Stone, Ice Stone, Dusk Stone, Dawn Stone, Shiny Stone, Sun Stone — 1 unidade cada
- **Poké Balls:** Poké Ball ×3, Premier Ball ×3, Heal Ball ×3, Azure/Citrine/Verdant/Slate/Roseate Ball ×3
- **EV Feathers:** Health, Muscle, Resist, Genius, Clever, Swift — 3 de cada
- **Mints:** todos os tipos (Adamant, Bold, Brave, Calm, etc.) — 1 unidade cada
- **Held items:** Assault Vest, Leftovers, Life Orb, Choice Band/Scarf/Specs, Focus Sash, Rocky Helmet, Muscle Band, Wise Glasses e outros — 1 unidade cada
- **EV Training:** Tumblestone ×2, Sky Tumblestone ×2, Black Tumblestone ×2
- **Consumíveis:** Potion ×2, Burn Heal ×2, Antidote ×2, Paralyze Heal ×2, etc.
- **Outros:** Evolution stones ×1, Sherds ×1, Exp Candy XS ×10, Exp Candy S ×5, X items ×1

---

### Great Capsule — 24% de chance de sair da máquina

Pool com ~150 itens. Melhoria geral em quantidade e qualidade:

- **Mints:** todos os tipos — **3 unidades** (vs 1 da Poké Capsule)
- **EV Feathers:** 6 de cada
- **Pedras de evolução:** 3 de cada
- **Berries raras:** Custap, Micle, Enigma, Salac, Liechi, Petaya, Ganlon, Apicot, Starf, Lansat e outras — 4 de cada
- **Ancient Balls:** todas as variantes — 3 de cada
- **Balls especiais:** Fast, Friend, Heavy, Lure, Level, Moon, Park, Dive, Net, Nest — 3 de cada
- **Power Items:** Power Anklet, Band, Belt, Bracer, Herb, Lens, Weight — 1 de cada
- **Held items mais raros:** Destiny Knot ×1-2, Eviolite ×1, Blunder Policy ×1, Flame Orb ×1, Toxic Orb ×1, Scope Lens ×1, Shell Bell ×1, Weakness Policy ×1, Loaded Dice ×1
- **Items de evolução:** Electirizer, Magmarizer, Dragon Scale, Deep Sea Scale/Tooth, Kings Rock, Metal Coat, Prism Scale, Protector, Reaper Cloth, Razor Claw/Fang, Link Cable, Upgrade, Dubious Disc, Oval Stone, Black Augurite, Galarica Cuff/Wreath, Sachet ×2, Whipped Dream ×1
- **Exp Candy:** L ×5, M ×10
- **Consumíveis melhores:** Revive ×3, Elixir ×3, Ether ×3, Energy Root ×3, Revival Herb ×3, Full Heal ×4, Super Potion ×2
- **Fossils:** Skull Fossil, Dome Sherd e outros
- **Misc:** Cracked Pot ×1, Peat Block ×1, Unremarkable Teacup ×1, Vivichoke ×3, Auspicious Armor ×1, Malicious Armor ×1

---

### Ultra Capsule — 15% de chance de sair da máquina

Pool com ~150 itens. Salto de qualidade significativo:

- **Ability Capsule ×3, Ability Patch ×3**
- **Mints:** todos os tipos — **6 unidades**
- **Pedras de evolução:** 5 de cada
- **EV Vitamins:** HP Up, Iron, Calcium, Carbos, Protein, Zinc — **4 de cada**
- **Exp Candy:** L ×10, M ×20, **XL ×5**
- **Exp Share ×2**
- **Lucky Egg ×2**
- **PP Up ×4, PP Max ×4**
- **Max Revive ×3, Max Elixir ×3, Max Ether ×3, Full Restore ×3**
- **Relic Coin ×30**
- **Rare Candy ×1** (da Cram O' Matic, pool diferente: ×5)
- **Fossils completos:** Helix, Dome, Old Amber, Skull, Armor, Claw, Cover, Jaw, Plume, Sail, Root, Fossilized Bird/Dino/Drake/Fish — 1 de cada
- **Fossil Analyzer ×1**
- **Fishing rods:** Poké Rod, Great Rod, Ultra Rod, Ancient rods (Great, Ivory, Poke, Ultra, Wing) — 1 de cada
- **Cobblemon blocks:** PC ×1, Pasture ×1, Healing Machine ×1, Monitor ×1, Restoration Tank ×1
- **Gems:** todos os tipos — 3 de cada
- **Gilded Chests:** todos os tipos (Black, Blue, Green, Pink, White, Yellow, regular) — 2 de cada
- **Soothe Bell ×2, Sweet Apple ×2, Tart Apple ×2**
- **Pokedex coloridas:** Black, Blue, Green, Pink, Red, White, Yellow — 1 de cada
- **Masterpiece Teacup ×2, Unremarkable Teacup ×2**

---

### Master Capsule — 7% de chance de sair da máquina

Pool menor (~80 itens), tudo em grande quantidade:

- **Ability Capsule ×7, Ability Patch ×7**
- **Mints:** todos — **6 unidades**
- **EV Vitamins:** todos — **7 de cada**
- **PP Up ×7, PP Max ×7**
- **Exp Candy:** L ×10, XL ×10
- **Exp Share ×4**
- **Lucky Egg ×6**
- **Master Ball ×1**
- **Relic Coin ×60**
- **Rare Candy ×15**
- **Max Elixir ×10, Max Ether ×10, Max Revive ×6, Full Restore ×6, Super Potion ×5, Hyper Potion ×5**
- **Fossils:** 3 de cada
- **Fossil Analyzer ×2**
- **Todas as fishing rods normais e antigas** — 1 de cada
- **Cobblemon blocks:** PC ×2, Pasture ×2, Healing Machine ×2, Monitor ×2, Restoration Tank ×2
- **Gilded Chests:** todos os tipos — 4 de cada
- **Beast Ball ×3, Dream Ball ×3, Safari Ball ×3, Sport Ball ×3**
- **Gems:** pedras de evolução em bloco (dawn_stone_block, dusk_stone_block, etc.) — 1 de cada
- **Superb Remedy ×3, Guard Spec ×6, Dire Hit ×6**
- **Stone blocks:** Fire/Ice/Leaf/Moon/Shiny/Sun/Thunder/Water Stone Block — 1 de cada

---

### Cherish Capsule — 3% de chance de sair da máquina

Pool menor ainda (~25 itens), quantidades máximas:

- **Ability Capsule ×15, Ability Patch ×15**
- **Master Ball ×3**
- **Cherish Ball ×3**
- **Ancient Origin Ball ×3**
- **Beast Ball ×3** *(via Beast Rod também)*
- **Relic Coin ×150**
- **Rare Candy ×20**
- **Exp Candy XL ×30**
- **EV Vitamins:** todos — **16 de cada** (HP Up, Iron, Calcium, Carbos, Protein, Zinc)
- **PP Up ×16, PP Max ×16**
- **Max Elixir ×15, Max Ether ×15, Max Revive ×15, Full Restore ×15**
- **Max Potion ×15**
- **Exp Share ×4, Lucky Egg ×6** *(quantidade igual à Master)*
- **Superb Remedy ×7**
- **Fishing rods raros:** Ancient Origin Rod, Beast Rod, Cherish Rod, Master Rod, Dream Rod, Dive Rod — 1 de cada
- **Gilded Chests:** todos — 4 de cada

---

## Cram O' Matic — Drops diretos

Essa máquina não usa cápsulas — dá Poké Balls diretamente (rolls 1–5 itens por uso):

**Mais comuns (peso 80):** Poké Ball, Great Ball equivalentes, Premier Ball, Ancient Verdant/Citrine/Slate/Azure/Roseate/Ivory Ball — 1 a 3 de cada  
**Médios:** Heal Ball ×1-4, Repeat Ball, Dusk Ball, Net Ball, Nest Ball, Dive Ball — 1 a 3  
**Raros (peso 5–15):** Luxury Ball, Lure Ball, Friend Ball, Love Ball, Level Ball, Fast Ball, Moon Ball, Safari Ball, Sport Ball, Heavy Ball — 1 a 2  
**Ultra Ball (peso 20)** ×1-3  
**Extras:** Ability Capsule ×1-5, Rare Candy ×1-5, Sweets, Cracked Pot, Whipped Dream  
**Held items:** Choice Band/Scarf/Specs, Eviolite, Life Orb, Shell Bell, Destiny Knot e muitos outros

---

## Strange Crystallized Machine — Spawna Pokémon

Essa máquina **não dá item** — ela spawna um Pokémon diretamente no mundo.

- Usa **Tera Gacha Coin** (custo: 5)
- Pool com **228+ Pokémon** de todas as regiões: Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar, Hisui, Paldea
- Raridade do Pokémon depende do bucket (common → legendary)
- Alguns Pokémon têm formas regionais (ex: Hisuian Samurott, Galarian Stunfisk)

---

## Rocket Prize Master — Koban Coin → Rocket Ball

- Custo: **1 Koban Coin** por uso
- Sempre dá um **Rocket Ball**
- Use o Rocket Ball com **clique direito** para spawnar um Pokémon de qualquer região (mesma pool da Strange Crystallized Machine)
- O Pokémon spawnado pelo Rocket Ball vai **direto para a party** (ou PC se estiver cheia)

---

## Plush-O-Matic — Pelúcias de Pokémon

Requer o mod **PokeBlocks** instalado para os itens aparecerem.

- Custo: **3 Yarns** do mesmo tipo
- O tipo de Yarn determina **qual Pokémon** pode sair como pelúcia
- Cada tipo dá versão normal, shiny, e gigante (gigantic) de Pokémon do tema

| Yarn | Pokémon temáticos (exemplos) |
|---|---|
| Plain Yarn | Eevee, Furret, Happiny, Lickitung, Munchlax, Sentret, Snorlax |
| Outros tipos | Pokémon do tipo correspondente |

---

## Gacha Balls — Item de uso direto

Gacha Balls não precisam de máquina. **Clique direito** para usar:
- Spawna um Pokémon aleatório da pool da ball
- Pokémon vai **direto para a party** (ou PC se cheia)
- O item é consumido ao usar

| Item | Pool |
|---|---|
| Poké Gacha Ball | Pool padrão de Pokémon |
| Citrine/Verdant/Azure/Roseate/Slate Gacha Ball | Pools específicas por cor |

---

## Cooldowns

Algumas máquinas podem ter cooldown configurado pelo servidor. Se isso acontecer, ao tentar usar a máquina aparece:

> *"Hold on! You can use this machine again in Xs."*

Basta esperar o tempo indicado. O cooldown é **por jogador** — não afeta outros jogadores usando a mesma máquina.
