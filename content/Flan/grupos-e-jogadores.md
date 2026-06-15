# Grupos e Jogadores — Como Dar Acesso ao Seu Claim

## O que são Grupos?

Grupos são conjuntos de permissões que você aplica a jogadores dentro do seu claim. Em vez de configurar permissão por permissão para cada pessoa, você cria um grupo com as permissões desejadas e adiciona os jogadores nele.

Cada claim tem seus próprios grupos. As configurações de um claim não afetam outro.

---

## Grupos Padrão do Servidor

O servidor já vem com dois grupos configurados automaticamente em todo claim novo:

### Visitor (Visitante)
Qualquer jogador que entrar no seu claim sem estar em nenhum grupo receberá as permissões de Visitor automaticamente.

**O que Visitor pode fazer:**
- Usar camas
- Abrir e fechar portas, portões de cerca e alçapões
- Usar alavancas, botões e placas de pressão
- Usar mesas de encantamento
- Acessar baús de ender (o baú de ender é individual, então não é perigoso liberar)
- Rotacionar itens em molduras de item
- Usar portais
- Negociar com aldeões

**O que Visitor NÃO pode fazer (padrão):**
- Quebrar ou colocar blocos
- Abrir baús, fornalhas, barris ou outros contêineres
- Atacar animais ou jogadores
- Pegar ou largar itens
- Usar ferramentas em blocos

### Co-Owner (Co-Dono)
Jogadores no grupo Co-Owner têm **acesso total** ao claim — praticamente as mesmas permissões do dono.

**O que Co-Owner pode fazer:** Tudo — quebrar/colocar blocos, abrir todos os contêineres, gerenciar permissões, adicionar outros jogadores, editar mensagens de entrada/saída, e muito mais.

> **Cuidado:** Só adicione pessoas de confiança no grupo Co-Owner.

---

## Como Adicionar um Jogador a um Grupo

Dentro do seu claim, use:

```
/flan group players add <grupo> <nome_do_jogador>
```

**Exemplos:**
```
/flan group players add Visitor Steve
/flan group players add Co-Owner Maria
```

O jogador não precisa estar online para ser adicionado.

---

## Como Remover um Jogador de um Grupo

```
/flan group players remove <grupo> <nome_do_jogador>
```

**Exemplo:**
```
/flan group players remove Co-Owner Steve
```

Após a remoção, o jogador volta a ter apenas as permissões de Visitor quando entrar no claim.

---

## Criar um Grupo Personalizado

Você pode criar grupos com permissões específicas para casos como "amigo que só colhe a fazenda" ou "membro que pode abrir baús mas não quebrar blocos".

**Criar o grupo:**
```
/flan group add <nome_do_grupo>
```

**Exemplo:**
```
/flan group add Fazendeiro
```

Depois de criar, configure as permissões do grupo (veja a seção de Permissões e Flags) e adicione jogadores nele.

---

## Remover um Grupo Personalizado

```
/flan group remove <nome_do_grupo>
```

Jogadores que estavam nesse grupo voltam a ter permissões de Visitor.

---

## Gerenciar Grupos pelo Menu Visual

Dentro do seu claim, abra o menu com `/flan menu` e selecione a opção de **Grupos de Permissão**. No menu você pode:

- Ver todos os grupos existentes no claim
- Adicionar e remover jogadores visualmente
- Editar permissões de cada grupo clicando nos itens

---

## Grupos Pessoais Padrão

Você pode configurar quais permissões os grupos terão **por padrão em todos os claims novos que você criar**. Isso evita ter que reconfigurar do zero a cada novo claim.

Para editar essas configurações:

```
/flan personalGroups
```

Abre um menu onde você customiza as permissões padrão dos grupos Visitor, Co-Owner e de qualquer grupo personalizado que você queira.

---

## Resumo dos Comandos de Grupos

| Comando | O que faz |
|---|---|
| `/flan group add <nome>` | Cria um novo grupo no claim atual |
| `/flan group remove <nome>` | Remove um grupo do claim atual |
| `/flan group players add <grupo> <jogador>` | Adiciona jogador ao grupo |
| `/flan group players remove <grupo> <jogador>` | Remove jogador do grupo |
| `/flan personalGroups` | Abre menu para editar grupos padrão de claims futuros |
| `/flan menu` | Abre menu visual para gerenciar grupos e permissões |
