# Mecânicas Especiais — Claims 3D, Bordas e Proteções Avançadas

## Claims 3D — Controle Total da Vertical

### O que é um Claim 3D?

No modo padrão (2D), um claim se estende automaticamente **10 blocos para baixo** da superfície onde você clicou. Isso protege contra tunelamento superficial, mas não cobre grandes profundidades.

No modo 3D, você define manualmente a **altura mínima e máxima** do claim, dando controle total sobre a vertical. Ideal para bases subterrâneas, torres altas ou estruturas que precisam de proteção precisa em altura.

### Como Ativar o Modo 3D

```
/flan switchMode default.3d
```

Para subclaims 3D:
```
/flan switchMode subclaim.3d
```

Para voltar ao modo normal:
```
/flan switchMode default
```

### Como Criar um Claim 3D

Com o modo 3D ativo e a **Enxada Dourada** na mão:

1. Clique com botão direito no **primeiro bloco** — define um canto (inclui coordenada Y)
2. Vá até o canto oposto em outra altura
3. Clique com botão direito no **segundo bloco** — o claim cobre toda a caixa entre os dois pontos

**Requisito:** Diferença mínima de **10 blocos de altura** entre os dois pontos.

### Custo de Claims 3D

Claims 3D custam blocos de claim com base no **volume**: largura × comprimento × altura.
Exemplo: uma área de 20×20 com 15 blocos de altura custa 6.000 blocos de claim.

---

## Proteção de Borda com Água

A permissão `flan:water_border` controla se **água pode cruzar as bordas do claim**.

- **Ativado (padrão):** Água de fora pode fluir para dentro do claim e vice-versa
- **Desativado:** Água é bloqueada na borda do claim

Para desativar fluxo de água pelas bordas do seu claim:
```
/flan permission global flan:water_border false
```

Isso é útil para proteger fazendas de irrigação e estruturas subaquáticas contra griefing por desvio de água.

---

## Proteção Contra Pistões

A permissão `flan:piston_border` controla se **pistões de fora podem mover blocos para dentro do claim** (e vice-versa).

- **Ativado (padrão):** Pistões podem empurrar blocos através das bordas
- **Desativado:** Pistões são bloqueados na borda do claim

Para bloquear pistões externos:
```
/flan permission global flan:piston_border false
```

Evita máquinas de grief usando pistões para mover blocos para dentro do seu claim.

---

## Explosões

A permissão `flan:explosions` controla se **explosões danificam blocos** dentro do claim.

- **Ativado:** TNT, creepers e outras explosões destroem blocos normalmente
- **Desativado:** Explosões dentro ou fora do claim não destroem blocos

Para desativar dano de explosões no seu claim:
```
/flan permission global flan:explosions false
```

> **Nota:** Isso não protege contra dano a jogadores — apenas aos blocos.

---

## Fogo

A permissão `flan:fire_spread` controla se **fogo se espalha** dentro do claim.

- **Ativado:** Fogo se espalha normalmente entre blocos inflamáveis
- **Desativado:** Fogo não se espalha (mas blocos ainda podem ser acesos individualmente)

Para desativar propagação de fogo:
```
/flan permission global flan:fire_spread false
```

---

## Wither

A permissão `flan:wither` controla se **o Wither pode destruir blocos** dentro do claim.

- **Ativado:** Wither destrói blocos normalmente ao atacar e se mover
- **Desativado:** Wither não causa dano a blocos no claim

Para proteger seu claim contra o Wither:
```
/flan permission global flan:wither false
```

---

## Raios

A permissão `flan:lightning` controla se **raios têm efeito** dentro do claim.

- **Ativado:** Raios podem acender fogo, transformar mobs (porcos em piglins, etc.) e causar outros efeitos
- **Desativado:** Raios caem mas não causam efeitos secundários

---

## Spawn de Mobs

### Bloquear Mobs Hostis

Para impedir que mobs hostis spawnem no seu claim:
```
/flan permission global flan:disable_monster_spawn true
```

> **Padrão do servidor:** Mobs hostis spawnam normalmente em todos os claims. Você precisa ativar essa permissão manualmente se quiser bloqueá-los.

### Bloquear Todos os Mobs

Para impedir qualquer mob de spawnar:
```
/flan permission global flan:disable_mob_spawn true
```

> Isso bloqueia tanto mobs hostis quanto passivos (animais, aldeões, etc.).

---

## Itens Travados ao Morrer

A permissão `flan:lock_items` está **sempre ativa no servidor**. Isso significa que quando você morre, seus itens ficam no chão **bloqueados** — outros jogadores não conseguem pegar, mesmo que estejam no mesmo claim.

Para desbloquear seus itens manualmente e permitir que outros os peguem:
```
/flan unlockDrops
```

Para desbloquear os itens de outro jogador específico (se você tiver permissão):
```
/flan unlockDrops <nome_do_jogador>
```

---

## PvP (Batalha entre Jogadores)

A permissão `flan:hurt_player` controla se **jogadores podem atacar outros jogadores** dentro do claim.

- **Desativado (padrão para Visitors):** Jogadores não conseguem causar dano uns aos outros
- **Ativado:** PvP é permitido dentro do claim

Para ativar PvP na sua arena ou área de combate:
```
/flan permission global flan:hurt_player true
```

---

## Ficando Preso em um Claim

Se você ficar preso dentro de um claim de outro jogador sem conseguir sair, use:

```
/flan trapped
```

Após **5 segundos**, você é teleportado para fora do claim automaticamente. Só funciona se você realmente não conseguir se mover para fora do claim.

---

## Endermen e Blocos

A permissão `flan:enderman` controla se **Endermen podem pegar e colocar blocos** dentro do claim.

- **Desativado:** Endermen não pegam nem colocam blocos — protege contra roubo de blocos decorativos ou funcionais
- **Ativado:** Comportamento padrão do jogo

Para proteger seu claim contra Endermen:
```
/flan permission global flan:enderman false
```
