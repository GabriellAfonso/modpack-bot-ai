# Claims 3D — Proteção com Controle Total de Altura

## O que é um Claim 3D?

Um claim 3D é uma área de proteção onde você define manualmente tanto os limites horizontais (largura e comprimento) quanto os limites verticais (altura mínima e máxima). Você especifica exatamente quais camadas do mundo ficam protegidas.

Diferente do claim padrão (2D), que automaticamente protege 10 blocos abaixo da superfície, o claim 3D protege apenas o volume exato que você selecionou.

---

## Quando Usar Claims 3D

- **Base subterrânea profunda:** Se você construiu mais de 10 blocos abaixo da superfície, o claim 2D padrão não protege toda a base. Use 3D para cobrir do teto ao chão.
- **Torre ou estrutura alta:** Proteja exatamente os andares da sua torre.
- **Área específica sem bloquear o subsolo:** Proteja só a superfície de uma fazenda sem impedir mineração abaixo.
- **Galerias de mineração:** Proteja um corredor estreito no subsolo.

---

## Como Ativar o Modo 3D

```
/flan switchMode default.3d
```

O modo fica ativo até você trocar novamente. Para voltar ao modo normal 2D:

```
/flan switchMode default
```

---

## Como Criar um Claim 3D

Com o modo 3D ativo e a **Enxada Dourada** na mão:

1. Vá até um dos cantos da área que quer proteger (em qualquer altura)
2. **Clique com botão direito** no bloco — esse é o primeiro ponto (X, Y, Z)
3. Vá até o canto oposto, na altura oposta
4. **Clique com botão direito** no segundo bloco — o claim cobre toda a caixa entre os dois pontos

**Exemplo:** Clique num bloco em Y=20 num canto, depois num bloco em Y=64 no canto oposto. O claim cobrirá os blocos de Y=20 até Y=64 nessa área.

---

## Custo de um Claim 3D

O custo é calculado pelo **volume** da área: largura × comprimento × altura.

| Dimensões | Custo |
|---|---|
| 10 × 10 × 10 | 1.000 blocos |
| 20 × 20 × 15 | 6.000 blocos |
| 50 × 50 × 5 | 12.500 blocos |

Claims 3D geralmente custam mais blocos que claims 2D para a mesma área de superfície. Planeje com cuidado para não gastar todos os seus blocos.

---

## Altura Mínima

A diferença de altura entre os dois cantos deve ser de pelo menos **10 blocos**. Não é possível criar um claim 3D com menos de 10 blocos de altura.

---

## Subclaims 3D

Para criar subclaims com controle 3D dentro de um claim existente:

```
/flan switchMode subclaim.3d
```

Funciona da mesma forma que criar um claim 3D normal, mas a área deve estar dentro do claim principal. O custo de blocos de subclaims 3D segue o mesmo cálculo de volume.

---

## Via Comando

Para criar um claim 3D por coordenadas:

```
/flan add <x1,y1,z1> <x2,y2,z2>
```

**Exemplo:**
```
/flan add 100,20,200 150,80,250
```

Isso cria um claim de X=100 até X=150, Y=20 até Y=80, Z=200 até Z=250.

---

## Diferença Entre 2D e 3D

| | Claim 2D (Padrão) | Claim 3D |
|---|---|---|
| Altura | Automática: 10 blocos abaixo do clique | Manual: você define |
| Custo | Área (largura × comprimento) | Volume (largura × comprimento × altura) |
| Modo | `/flan switchMode default` | `/flan switchMode default.3d` |
| Ideal para | Bases de superfície simples | Bases subterrâneas, torres, estruturas complexas |

---

## Expandir um Claim 3D

Com o modo 3D ativo e dentro do claim, use:

```
/flan expand <distância>
```

Olhe para a direção que quer expandir (incluindo cima e baixo). O custo da expansão em blocos de claim é calculado pelo novo volume adicionado.
