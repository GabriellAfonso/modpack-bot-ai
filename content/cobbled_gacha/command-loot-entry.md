# Command Loot Entry — Executar Comandos como Recompensa

O mod adiciona um tipo especial de entrada em tabelas de loot chamado `cobbledgacha:command_entry`. Ele permite que um **comando de servidor** seja executado como parte de uma recompensa — por exemplo, ao abrir uma cápsula ou ao girar uma máquina gacha.

---

## O que é e para que serve

Normalmente, tabelas de loot podem apenas dar itens. Com o `command_entry`, é possível:

- Executar qualquer comando do servidor como "prêmio"
- Dar dinheiro (se o servidor tiver plugin de economia)
- Adicionar permissões
- Teleportar o jogador
- Enviar mensagens customizadas

Isso é configurado por administradores/criadores de datapack nas tabelas de loot das máquinas e cápsulas.

---

## Como adicionar em uma tabela de loot (para administradores)

Em qualquer arquivo de tabela de loot de máquina ou cápsula, adicione uma entrada com `"type": "cobbledgacha:command_entry"`:

```json
{
  "type": "cobbledgacha:command_entry",
  "command": "give @p minecraft:diamond 1",
  "weight": 5
}
```

O campo `command` é o comando que será executado — sem a barra `/` no início.

---

## Permissão do comando

O comando é executado com nível de permissão 2 (operador de servidor). Isso significa que pode executar a maioria dos comandos, incluindo `/give`, `/effect`, `/teleport`, etc.

O comando é executado no local onde a máquina está posicionada (não na posição do jogador).

---

## Exemplo: cápsula que dá dinheiro

```json
{
  "type": "cobbledgacha:capsule",
  "pools": [
    {
      "rolls": 1,
      "entries": [
        {
          "type": "minecraft:item",
          "name": "cobblemon:poke_ball",
          "weight": 90
        },
        {
          "type": "cobbledgacha:command_entry",
          "command": "eco give @p 500",
          "weight": 10
        }
      ]
    }
  ]
}
```

Neste exemplo, 10% das aberturas da cápsula executam o comando `eco give @p 500` (presumindo que o servidor tenha um plugin de economia que aceite esse comando).

---

## Campos disponíveis no command_entry

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | string | Sim | Sempre `"cobbledgacha:command_entry"` |
| `command` | string | Sim | O comando a executar (sem `/`) |
| `weight` | inteiro | Não | Peso na tabela de loot (padrão = 1) |
| `quality` | inteiro | Não | Modificador de peso por sorte do jogador |
| `conditions` | array | Não | Condições para o entry ser elegível |
| `functions` | array | Não | Funções de loot (geralmente não aplicável a commands) |

---

## Observação

O `command_entry` **não dá item nenhum** ao jogador — apenas executa o comando. Se você quiser que o jogador receba um item E um comando seja executado, use dois entries separados na tabela de loot (um `minecraft:item` e um `cobbledgacha:command_entry`).
