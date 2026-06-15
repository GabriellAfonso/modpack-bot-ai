# Menus Visuais (GUI) — Como Gerenciar Seu Claim pela Interface

## Abrindo o Menu Principal

Para abrir o menu de gerenciamento do claim onde você está:

```
/flan menu
```

Você precisa estar dentro do claim. Se estiver num subclaim, o menu abre com as opções do subclaim.

---

## O que Tem no Menu Principal

O menu abre como uma interface de inventário. Cada item no menu representa uma opção:

| Posição | Item | Função |
|---|---|---|
| Esquerda | Farol (Beacon) | Editar permissões globais do claim |
| Centro-esquerda | Bloco de Esmeralda | Editar grupos de permissão e jogadores |
| Centro | Suporte de Poção | Editar efeitos de poção do claim |
| Centro-direita | Placa | Editar mensagens de entrada/saída |
| Direita | Cabeça de Jogador | Gerenciar Fake Players |
| Canto direito | Barreira | Deletar o claim |
| Baixo-centro | Escudo | Configurar listas de exceção |
| Canto esquerdo | X Vermelho | Fechar o menu |

Clique nos itens para navegar entre as telas.

---

## Tela de Permissões Globais

Mostra todas as permissões do claim em formato de lista. Cada permissão é representada por um item:

- **Item verde / ativado** — permissão está habilitada
- **Item vermelho / desativado** — permissão está bloqueada
- **Item cinza / padrão** — usa o valor padrão do servidor

**Como usar:**
- **Clique esquerdo** — alterna entre ativado/desativado/padrão
- **Clique direito** — pode abrir opções adicionais dependendo da permissão

---

## Tela de Grupos de Permissão

Mostra todos os grupos do claim (Visitor, Co-Owner e grupos personalizados).

**O que você pode fazer aqui:**
- Ver quais jogadores estão em cada grupo
- Clique num grupo para editar suas permissões
- Adicionar ou remover jogadores de um grupo
- Criar novos grupos
- Excluir grupos personalizados

**Dentro de um grupo:**
- Cada permissão aparece como item
- Clique para alternar entre ativado/desativado/padrão
- Há uma seção para ver e editar a lista de membros do grupo

---

## Tela de Efeitos de Poção

Permite configurar efeitos de poção que afetam todos os jogadores dentro do claim.

> Essa tela requer que o administrador tenha liberado a permissão `flan:edit_potions`. Por padrão está desabilitada para jogadores.

**O que pode ser configurado:**
- Tipo de efeito (velocidade, força, lentidão, etc.)
- Duração do efeito
- Amplificador (nível I, II, III...)

---

## Tela de Mensagens

Permite editar as mensagens de título que aparecem quando jogadores entram e saem do claim.

**Campos editáveis:**
- Título de entrada
- Subtítulo de entrada
- Título de saída
- Subtítulo de saída

Clique no item correspondente para editar o texto diretamente.

---

## Tela de Fake Players

Mostra os UUIDs de fake players que têm permissão de interagir com o claim.

**O que você pode fazer:**
- Ver quais fake players estão autorizados
- Remover um fake player autorizado

Para adicionar um fake player, use o comando `/flan fakePlayer add <uuid>` ou clique no link da notificação que aparece quando um fake player tenta interagir.

---

## Tela de Listas de Exceção (Allow Lists)

Permite criar exceções específicas por bloco, item ou entidade.

**Tipos de lista:**
- Quebrar blocos
- Usar/interagir com blocos
- Atacar entidades
- Interagir com entidades
- Usar itens
- Largar itens
- Pegar itens

Para cada tipo, você pode definir se a lista funciona como:
- **Whitelist** — só os itens/blocos listados são permitidos
- **Blacklist** — todos são permitidos exceto os listados

---

## Menu de Grupos Pessoais

Para editar os grupos padrão que aparecem em **todos os claims novos** que você criar:

```
/flan personalGroups
```

Funciona igual à tela de grupos, mas as configurações se aplicam a claims futuros — não altera claims já existentes.

---

## Tela de Confirmação

Para operações destrutivas (como deletar todos os claims), o sistema pede confirmação visual antes de executar.

- Clique no item verde para **confirmar**
- Clique no item vermelho para **cancelar**

Ou use os comandos:
```
/flan confirm confirm
/flan confirm deny
```
