# IVs, EVs, Natureza e Marcas

---

## IVs (Individual Values)

IVs são valores genéticos ocultos de 0 a 31 em cada stat. Pokémon com IV 31 num stat são "perfeitos" naquele stat. Afetam diretamente o stat final no nível 100.

- Cada Pokémon nasce com IVs aleatórios.
- IVs são visíveis no menu de sumário do Pokémon (no PC ou equipe).
- Não podem ser alterados naturalmente (apenas por criação seletiva de ovos).

---

## EVs (Effort Values)

EVs representam o treinamento do Pokémon. Cada vitória em batalha dá EVs no stat correspondente do inimigo derrotado.

- Máximo de **252 EVs** por stat individual.
- Máximo de **510 EVs** no total (todos os stats combinados).
- Cada 4 EVs equivale a +1 ponto no stat final no nível 100.

### Como Reduzir EVs
Use bagas específicas para reduzir EVs em stats indesejados (reduzem 10 EVs por uso — via mecânica de baga `evLowerAmount = 10`).

---

## Natureza (Nature)

A natureza define qual stat recebe bônus de +10% e qual recebe penalidade de -10%. Existem 25 naturezas no total.

- **Neutras (5):** Sem bônus ou penalidade (Hardy, Docile, Serious, Bashful, Quirky).
- **Demais (20):** Uma stat +10%, outra -10%.

### Mints — Alterar Efeito da Natureza
**Mints** são itens que alteram qual stat recebe bônus/penalidade, sem mudar a natureza exibida. Craftados com a receita de cada mint (ex: Adamant Mint, Modest Mint, Timid Mint).

Cada natureza tem seu mint correspondente. Use no menu de sumário do Pokémon.

---

## Amizade (Friendship)

Vai de 0 a **255**. Afeta:
- Evolução por amizade (mínimo ~160 para a maioria).
- Poder do golpe **Return** (mais forte com amizade alta).
- Poder do golpe **Frustration** (mais forte com amizade baixa).
- Itens de cura têm penalidade de amizade (veja `05-cura-e-maquina-de-cura.md`).

### Como Aumentar Amizade
- Caminhar com o Pokémon na equipe.
- Vencer batalhas sem o Pokémon desmaiar.
- Usar bagas e itens no Pokémon.
- Pokébola **Luxury Ball** aumenta amizade mais rápido.
- Pokébola **Friend Ball** começa com amizade alta.

### Como Baixar Amizade
- Pokémon desmaiar em batalha.
- Usar certos itens de cura que têm penalidade (Antídoto, Heal Powder, etc.).

---

## Marcas (Marks)

Marcas são títulos/selos especiais que Pokémon podem ter. Aparecem no nome do Pokémon quando exibido. Pokémon selvagens podem nascer com marcas aleatórias, e certas atividades garantem marcas específicas.

Exemplo: A mark **"Mightiest Mark"** é dada a Pokémon capturados em Raid Dens de Tier 7.

Marcas são cosméticas — não afetam stats ou batalha, mas identificam a origem do Pokémon.
