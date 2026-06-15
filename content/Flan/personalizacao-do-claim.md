# Personalização do Claim — Nome, Mensagens e Home

## Nomear um Claim

Você pode dar um nome ao seu claim para identificá-lo facilmente na lista de claims e para usar em mensagens de entrada/saída.

**Comando:**
```
/flan name <nome>
```

**Exemplo:**
```
/flan name Minha Base Principal
```

O nome aparece quando alguém usa o Graveto para inspecionar a área, no comando `/flan list` e nas mensagens de entrada/saída se você usar `%s` no texto.

---

## Mensagens de Entrada e Saída

Você pode configurar mensagens que aparecem na tela quando um jogador entra ou sai do seu claim. Essas mensagens aparecem como títulos na tela (título e subtítulo).

### Configurar Mensagem de Entrada

**Título principal:**
```
/flan claimMessage enter title string <texto>
```

**Subtítulo:**
```
/flan claimMessage enter subtitle string <texto>
```

### Configurar Mensagem de Saída

**Título principal:**
```
/flan claimMessage leave title string <texto>
```

**Subtítulo:**
```
/flan claimMessage leave subtitle string <texto>
```

### Exemplos

```
/flan claimMessage enter title string Bem-vindo a %s!
/flan claimMessage enter subtitle string Propriedade de %n
/flan claimMessage leave title string Até logo!
```

`%s` é substituído pelo **nome do claim** e `%n` pelo **nome do dono** automaticamente.

### Remover uma Mensagem

Para remover uma mensagem existente:
```
/flan claimMessage enter title string $empty
```

### Usar Texto Formatado

Para usar texto com formatação Minecraft (cores, negrito, etc.), use o argumento `text` em vez de `string`:
```
/flan claimMessage enter title text {"text":"Bem-vindo!","color":"gold","bold":true}
```

> **Nota:** Para editar mensagens, você precisa da permissão `flan:claim_message` no claim (donos têm automaticamente).

---

## Ponto de Home (Teleporte)

Você pode definir um ponto de teleporte dentro do seu claim para voltar rapidamente a ele.

### Definir o Home

Fique no local exato onde quer o ponto de teleporte e use:
```
/flan setHome
```

### Teleportar para o Home

```
/flan teleport self <nome_do_claim>
```

**Exemplo:**
```
/flan teleport self Minha Base Principal
```

> **Atenção:** Por padrão do servidor, apenas o **dono do claim** pode teleportar para o home. Outros jogadores não têm essa permissão habilitada.

---

## Efeitos de Poção no Claim

É possível configurar efeitos de poção que se aplicam automaticamente a jogadores dentro do claim. Essa funcionalidade está **desabilitada por padrão** — apenas administradores podem ativar.

Se um administrador liberar essa permissão para você, use:
```
/flan menu
```
E selecione a opção de **Editar Efeitos de Poção** no menu.

---

## Gerenciar Fake Players

Alguns mods criam "fake players" para automatizar tarefas (como colheita automática). Por padrão, esses fake players não têm permissão de interagir com claims.

Se um fake player tentar interagir com seu claim, você receberá uma notificação com a opção de autorizar aquele fake player específico.

Para adicionar ou remover fake players manualmente:
```
/flan fakePlayer add <uuid>
/flan fakePlayer remove <uuid>
```

Para desativar as notificações de tentativas de fake players:
```
/flan fakePlayerNotification
```

---

## Listas de Exceção (Allow Lists)

Você pode criar exceções específicas para blocos, itens e entidades, independente das permissões globais do grupo.

**Exemplo de uso:** Bloquear interação com todos os contêineres, mas criar uma exceção para um baú específico.

**Via menu:**
```
/flan menu
```
Selecione **Gerenciar Allow Lists**.

**Via comando:**
```
/flan ignoreList add <tipo> <valor>
/flan ignoreList remove <tipo> <valor>
/flan ignoreList state <tipo> <whitelist|blacklist>
```

**Tipos disponíveis:**
- `flan:block_break` — exceções para quebrar blocos
- `flan:block_use` — exceções para usar blocos
- `flan:entity_attack` — exceções para atacar entidades
- `flan:entity_use` — exceções para interagir com entidades
- `flan:item` — exceções por item usado
- `flan:item_drop` — exceções para largar itens
- `flan:item_pickup` — exceções para pegar itens

Cada tipo pode funcionar como **whitelist** (só os listados são permitidos) ou **blacklist** (todos são permitidos exceto os listados).
