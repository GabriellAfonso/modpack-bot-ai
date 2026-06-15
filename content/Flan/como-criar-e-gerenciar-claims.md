# Como Criar e Gerenciar Claims

## O que é um Claim?

Um claim é uma área retangular do mapa registrada como sua propriedade. Dentro dela, você controla o que outros jogadores podem fazer. Claims são permanentes e continuam protegidos mesmo quando você está offline.

---

## Criar um Claim com a Enxada Dourada

1. Pegue uma **Enxada Dourada** na mão
2. **Clique com botão direito** no primeiro canto da área que quer proteger
3. Vá até o canto oposto da área
4. **Clique com botão direito** no segundo canto — o claim é criado

**Requisitos:**
- A área deve ter no mínimo **100 blocos** (ex: 10×10)
- Você precisa de blocos de claim suficientes (1 por bloco de área)
- A área não pode sobrepor outro claim existente

---

## Criar um Claim por Comando

Se preferir usar comandos, há três formas:

```
/flan add <x1,y1,z1> <x2,y2,z2>
```
Cria um claim entre duas coordenadas específicas.

```
/flan add rect <largura> <comprimento>
```
Cria um claim retangular centralizado na sua posição atual.

```
/flan add all
```
Usa todos os seus blocos de claim disponíveis para criar o maior claim quadrado possível ao redor de onde você está.

---

## Expandir um Claim Existente

Para aumentar um claim que já existe:

1. Entre no claim que quer expandir
2. Olhe para a direção que quer expandir (Norte, Sul, Leste, Oeste, cima ou baixo)
3. Use o comando:

```
/flan expand <distância>
```

Exemplo: `/flan expand 10` adiciona 10 blocos na direção que você está olhando.

**Requisitos:**
- Você deve estar dentro do claim
- A expansão não pode sobrepor outro claim existente
- Você precisa de blocos de claim suficientes para cobrir a área adicionada

---

## Ver Informações de um Claim

Para ver informações do claim onde você está:

```
/flan info
```

Mostra: dono, coordenadas dos cantos, número de subclaims e nome do claim (se tiver).

Para listar todos os seus claims:

```
/flan list
```

---

## Renomear um Claim

Dentro do claim que quer renomear:

```
/flan name <nome>
```

Exemplo: `/flan name Minha Base`

---

## Deletar um Claim

Para deletar o claim onde você está:

```
/flan delete
```

Os blocos de claim usados são devolvidos para você.

Para deletar **todos** os seus claims de uma vez:

```
/flan deleteAll
```

Esse comando pede confirmação antes de executar. Confirme com `/flan confirm confirm` ou cancele com `/flan confirm deny`.

---

## Transferir um Claim para Outro Jogador

```
/flan transferClaim <nome_do_jogador>
```

O claim passa a pertencer ao outro jogador. Os blocos de claim usados saem da sua conta e entram na conta do novo dono.

---

## Profundidade do Claim (Para Baixo)

Por padrão, claims em modo 2D (normal) se estendem **10 blocos para baixo** a partir da superfície onde você clicou. Isso protege contra tunelamento por baixo da sua base.

Para proteção total da vertical, use o **modo 3D** (veja a seção sobre Subclaims e Claims 3D).

---

## Modos de Criação

Você pode estar em diferentes modos ao criar claims:

| Modo | Comando para Ativar | O que faz |
|---|---|---|
| **Normal 2D** | `/flan switchMode default` | Cria claims com profundidade fixa (10 blocos) |
| **Normal 3D** | `/flan switchMode default.3d` | Você define a altura manualmente |
| **Subclaim 2D** | `/flan switchMode subclaim` | Cria subclaims dentro do seu claim |
| **Subclaim 3D** | `/flan switchMode subclaim.3d` | Cria subclaims 3D dentro do seu claim |

O modo atual afeta o que acontece quando você usa a Enxada Dourada. Para criar um claim normal, certifique-se de estar no modo `default`.

---

## Ver Seus Blocos de Claim Disponíveis

```
/flan claimBlocks
```

Mostra quantos blocos você tem, quantos estão em uso e quantos ainda estão disponíveis.

---

## Teleportar para um Claim

Se você definiu um ponto de teleporte no claim com `/flan setHome`, pode voltar para ele com:

```
/flan teleport self <nome_do_claim>
```

> Por padrão, teleporte está desabilitado para outros jogadores. O dono do claim pode usar o teleporte nos próprios claims.
