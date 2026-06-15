# Bagas (Berries)

Bagas são frutos cultiváveis com múltiplos usos: alimentar Pokémon, criar itens de batalha, tingir blocos e produzir suco.

---

## Como Cultivar Bagas

1. Encontre arbustos de baga no mundo (geram em grupos em biomas específicos).
2. Colha as bagas dos arbustos.
3. **Plante direto no solo** (não precisa de farmland).
4. Aguarde o crescimento — cada baga tem seu tempo próprio.
5. Colha quando maduros. A planta pode se refazer e dar nova colheita.

### Rendimento
- A maioria rende **2 a 3 bagas** por colheita.
- Plantar no bioma favorito da baga dá **+0 a +1** baga bônus.
- Oran Berry: cresce em biomas temperados, leva ~36–44 min, rende 2–3.

### Reflorescimento
Após colher, a planta se refaz em **10 a 20 horas** para uma nova colheita.

---

## Mutações

Ao plantar certas bagas próximas umas das outras, a planta pode mutar e gerar uma baga diferente. Exemplo (Oran Berry):

| Baga ao Lado | Resultado da Mutação |
|-------------|---------------------|
| Cheri, Chesto, Pecha, Rawst ou Aspear | **Lum Berry** |
| Razz, Bluk, Nanab, Wepear ou Pinap | **Leppa Berry** |

---

## Efeitos das Bagas em Pokémon

Bagas dadas ao Pokémon como item segurado ativam automaticamente em batalha:

| Tipo de Baga | Efeito |
|-------------|--------|
| **Oran Berry** | Restaura **10 HP** quando HP cai abaixo de 50% |
| **Sitrus Berry** | Restaura **33% do HP máximo** quando HP cai abaixo de 50% |
| **Portion Berry** (genérica) | Restaura **33% do HP máximo** |
| **Leppa Berry** | Restaura **10 PP** de um golpe quando ele chega a 0 |
| Bagas de Status (Cheri, Chesto, Pecha, Rawst, Aspear, Lum) | Curam veneno, sono, queimadura, etc. automaticamente |
| Bagas de Resistência (Occa, Passho, Wacan, etc.) | Reduzem dano superefetivo de tipos específicos pela metade |
| **Starf Berry** | Aumenta um stat aleatório drasticamente |
| **Salac Berry** | Aumenta Velocidade quando HP está baixo |
| **Petaya Berry** | Aumenta Sp. Atk quando HP está baixo |

Amizade ao usar baga no Pokémon:
- Abaixo de 100 amizade: +10 por uso
- Entre 100–200: +5 por uso
- Acima de 200: +1 por uso

---

## Alimentar Pokémon Selvagens (Pokésnack)

Pokémon selvagens no mundo podem ser alimentados com bagas. Isso pode acalmá-los (reduzir fuga), ou aumentar amizade com Pokémon da equipe ao observar.

---

## Mulches (Adubos)

Mulches são craftados e aplicados nas plantas de baga para modificar o crescimento:

| Mulch | Efeito |
|-------|--------|
| **Loamy Mulch** | Favorece certos tipos de baga |
| **Peat Mulch** | Favorece outros tipos |
| **Coarse Mulch** | Altera velocidade de crescimento |
| **Rich Mulch** | Aumenta rendimento |
| **Sandy Mulch** | Adapta para biomas secos |
| **Humid Mulch** | Adapta para biomas úmidos |
| **Growth Mulch** | Acelera crescimento |
| **Surprise Mulch** | Efeito aleatório |

**Crafting base do Mulch:** Use `mulch_base.json` como receita base + ingrediente específico.

---

## Suco de Baga (Aprijuice)

Bagas podem ser transformadas em **Aprijuice** (suco) para ser dado a Pokémon montáveis. O suco modifica temporariamente as **estatísticas de montaria** (não os stats de batalha):

| Apricorn no Suco | Bônus | Penalidade |
|-----------------|-------|-----------|
| **Blue** | +2 Skill | -1 Jump |
| **Green** | +2 Jump | -1 Speed |
| **Pink** | +2 Speed | -1 Acceleration |
| **Red** | +2 Acceleration | -1 Stamina |
| **Yellow** | +2 Stamina | -1 Skill |
| **Black** | Sem efeito | — |
| **White** | -2 em todos os stats | — |

Stats de montaria afetados: **Speed**, **Acceleration**, **Jump**, **Stamina**, **Skill**.

Qualidade do suco depende do processo de preparo: LOW, MEDIUM ou HIGH. Qualidade alta requer mais pontos de preparo (8+ pontos).
