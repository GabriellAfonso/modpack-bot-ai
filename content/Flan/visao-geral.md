# Flan — Visão Geral do Sistema de Claims

## O que é o Flan?

Flan é um mod de proteção de terreno para Minecraft. Com ele, jogadores podem **marcar ("clamar") áreas do mundo** para protegê-las contra outros jogadores: ninguém de fora pode quebrar blocos, abrir baús, atacar animais ou causar danos na sua área, a menos que você permita.

---

## Conceitos Fundamentais

### Claim (Proteção de Terreno)
Um claim é uma área retangular do mapa que pertence a você. Dentro dela, você controla o que outros jogadores podem ou não fazer. Claims são permanentes — existem mesmo quando você está offline.

### Blocos de Claim
Blocos de claim são a "moeda" do sistema. Cada bloco de area que você protege consome 1 bloco de claim. Por exemplo, uma área de 20×20 consome 200 blocos de claim.

- Você começa com **5.000 blocos de claim**
- O limite máximo é **10.000 blocos de claim**
- Você ganha **1 bloco de claim a cada 30 segundos** enquanto está no servidor

### Subclaims
Subclaims são áreas menores dentro de um claim seu. Servem para dar permissões específicas a certas pessoas em partes da sua terra — por exemplo, dar acesso ao seu cofre mas não à sua fazenda.

### Grupos de Permissão
Dentro de cada claim, você pode criar grupos de jogadores com diferentes níveis de acesso. O servidor já vem com dois grupos padrão: **Visitor** (visitante) e **Co-Owner** (co-dono).

---

## Itens Essenciais

| Item | Uso |
|------|-----|
| **Enxada Dourada** | Ferramenta para criar claims |
| **Graveto (Stick)** | Ferramenta para inspecionar claims |

Segure a Enxada Dourada para criar e visualizar claims. Segure o Graveto para ver quem é o dono de qualquer terreno.

---

## Fluxo Básico de Uso

1. **Escolha sua área** — encontre onde quer construir
2. **Segure a Enxada Dourada** — clique com botão direito para marcar o primeiro canto, clique no segundo canto para confirmar a área
3. **Gerencie permissões** — use `/flan menu` para abrir o menu de gerenciamento do claim
4. **Adicione jogadores** — dê permissões a amigos com `/flan group players add <grupo> <jogador>`

---

## Proteções Padrão do Servidor

Por padrão, qualquer pessoa que entre em um claim tem as seguintes permissões de **Visitor** (visitante):
- Usar camas, portas, alçapões, portões de cerca
- Usar mesas de encantamento, baús de ender, alavancas e botões
- Usar placas de pressão e portais
- Rotacionar itens em molduras e negociar com aldeões

Tudo que **não** está na lista acima é **bloqueado para visitantes** — especialmente quebrar/colocar blocos e abrir baús normais.

---

## Limites do Servidor

| Configuração | Valor |
|---|---|
| Blocos de claim iniciais | 5.000 |
| Máximo de blocos de claim | 10.000 |
| Ganho de blocos | 1 a cada 30 segundos |
| Área mínima de um claim | 100 blocos |
| Profundidade padrão do claim | 10 blocos abaixo da superfície |
| Número máximo de claims | Ilimitado |
