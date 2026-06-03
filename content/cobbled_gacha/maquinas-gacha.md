# Máquinas Gacha — Todas as 12 Máquinas

O mod adiciona 12 máquinas de gacha diferentes (o **cassino**, ou casino, como muitos jogadores chamam). Cada máquina aceita um tipo de moeda específico, exige uma quantidade de inserções para girar, e entrega um tipo de recompensa. Todas as máquinas ocupam 2 blocos de altura e ficam orientadas para uma direção quando colocadas.

---

## Como obter qualquer máquina

Todas as máquinas são craftadas em uma bancada de trabalho (crafting table). As receitas são detalhadas abaixo. Nenhuma máquina gera naturalmente no mundo — elas precisam ser craftadas ou obtidas por outros meios (como recompensa de máquinas).

---

## 1. Poké Gacha Machine

**O que é:** A máquina principal do mod. Recebe Relic Coin (do Cobblemon) e dispensa cápsulas com recompensas aleatórias do Cobblemon.

**Como craftar (bancada 3×3):**
```
# # #
X P X
# Y #
```
- `#` = Lingote de Ferro (×4)
- `X` = Vidro (×2)
- `P` = Poke Ball
- `Y` = Dispenser

**Moeda aceita:** Relic Coin (Cobblemon)
**Custo padrão:** 5 moedas por giro

---

## 2. Cram O' Matic

**O que é:** Máquina temática de apricorns. Aceita qualquer apricorn (7 tipos diferentes) e dispensa recompensas. Por padrão exige 20 inserções por giro.

**Como craftar (bancada 3×3):**
```
F B S
L Y L
# C #
```
- `F` = Pena (Feather)
- `B` = Corante Azul
- `S` = Graveto (Stick)
- `L` = Carvão (Coal)
- `Y` = Dispenser
- `#` = Lingote de Ferro (×2)
- `C` = Baú (Chest)

**Moeda aceita:** Qualquer apricorn — Red, Blue, Green, Yellow, Pink, Black, White Apricorn
**Custo padrão:** 20 apricorns por giro

---

## 3. Item Printer

**O que é:** Máquina de impressão de itens. Aceita Relic Coin e entrega itens do Cobblemon. Por padrão exige 20 inserções por giro.

**Como craftar (bancada 3×3):**
```
# P #
D G D
Y U Y
```
- `#` = Lingote de Ferro (×2)
- `P` = Poke Ball
- `D` = Diamante (×2)
- `G` = Great Ball
- `Y` = Dispenser
- `U` = Ultra Ball

**Moeda aceita:** Relic Coin (Cobblemon)
**Custo padrão:** 20 moedas por giro

---

## 4. Strange Crystallized Machine

**O que é:** Máquina especial do tipo **spawner** — ao completar o custo, ela faz um Pokémon aparecer perto do jogador em vez de dispensar cápsulas. Usa Diamantes comuns como moeda.

**Como craftar (bancada 3×3):**
```
D N D
# M #
X # X
```
- `D` = Diamante (×2)
- `N` = Nether Star
- `#` = Bloco de Ferro (×3)
- `M` = Master Ball
- `X` = Bloco de Diamante (×2)

**Moeda aceita:** Diamante
**Custo padrão:** 5 diamantes por giro
**Comportamento especial:** Spawna um Pokémon (do pool configurado pelo servidor) em vez de dar cápsulas. A máquina não pode ser automatizada com hoppers.

---

## 5–10. Variantes Coloridas da Poké Gacha Machine

As máquinas 5 a 10 são variantes cosméticas da máquina 1 (Poké Gacha Machine). A mecânica é idêntica, mas cada uma pode ter suas próprias recompensas e cooldowns configurados pelo servidor.

**Como craftar:** Combine a **Poké Gacha Machine** com o corante correspondente na bancada:

| Máquina | Nome | Corante |
|---|---|---|
| Machine 5 | Citrine Poké Gacha Machine | Corante Amarelo |
| Machine 6 | Verdant Poké Gacha Machine | Corante Verde |
| Machine 7 | Azure Poké Gacha Machine | Corante Azul |
| Machine 8 | Roseate Poké Gacha Machine | Corante Rosa |
| Machine 9 | Slate Poké Gacha Machine | Corante Preto |
| Machine 10 | Premier Poké Gacha Machine | Corante Branco |

**Moeda aceita:** Relic Coin (Cobblemon)
**Custo padrão:** 5 moedas por giro (se não configurado de outra forma)

---

## 11. Rocket Prize Master

**O que é:** Máquina temática do Team Rocket. Usa a Koban Coin como moeda — item dropado ao matar um Meowth. Por padrão exige apenas 1 moeda por giro (gira instantaneamente na primeira inserção).

**Como craftar (bancada 3×3):**
```
I R I
U U U
B D B
```
- `I` = Bloco de Ferro (×2)
- `R` = Bloco de Redstone
- `U` = Ultra Ball (×3)
- `B` = Botas de Ferro (×2)
- `D` = Dispenser

**Moeda aceita:** Koban Coin
**Custo padrão:** 1 moeda por giro
**Como obter Koban Coin:** Mate um Meowth — ele dropa a moeda ao morrer.

---

## 12. Plush-O-Matic

**O que é:** Máquina de pelúcias Pokémon. Usa Yarns (fios temáticos) como moeda. É do tipo **specific (contiguous)** — o primeiro yarn inserido trava a máquina para aquele tipo específico, e a recompensa varia conforme o yarn usado. Ao completar o giro, a trava é liberada para o próximo uso.

**Como craftar (bancada 3×3):**
```
W D W
L P _
I # I
```
- `W` = Lã (qualquer cor, ×2)
- `D` = Dispenser
- `L` = Alavanca (Lever)
- `P` = Poke Ball
- `I` = Lingote de Ferro (×2)
- `#` = Bloco de Ouro (×2)

**Moeda aceita:** Qualquer Yarn (11 tipos disponíveis)
**Custo padrão:** 3 yarns do mesmo tipo por giro
**Comportamento especial:** O tipo de pelúcia dispensada depende do yarn usado. Ex: Plain Yarn dá pelúcias de Eevee, Furret, Happiny, Lickitung, Munchlax, Sentret e Snorlax.

Para craftar Yarns, veja o arquivo **plush-o-matic-e-yarns.md**.
