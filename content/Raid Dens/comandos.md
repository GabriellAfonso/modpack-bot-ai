# Comandos do Cobblemon Raid Dens

Todos os comandos do mod usam o prefixo `/crd`. São comandos administrativos que exigem permissão de operador (nível de comando equivalente a `CHEAT_COMMANDS_AND_COMMAND_BLOCKS`).

---

## `/crd dens`

**Cria um Cristal de Raid manualmente em uma posição específica.**

```
/crd dens <x> <y> <z> [random] [cycle_mode] [can_reset]
```

- `<x> <y> <z>` — Coordenadas onde o cristal será criado.
- `[random]` — Se presente, sorteia um Pokémon-chefe aleatório. Se ausente, usa o chefe padrão.
- `[cycle_mode]` — Como o chefe e o tipo mudam entre resets. Opções: `NONE`, `LOCK_BOTH`, `LOCK_TIER`, `LOCK_TYPE`, `BUCKET`, `ALL`. Se omitido, usa o valor global do config.
- `[can_reset]` — `true` ou `false`. Se `true`, o cristal pode resetar após o número máximo de vitórias.

**Exemplos:**
```
/crd dens 100 64 200
/crd dens 100 64 200 random ALL true
```

---

## `/crd resetclears`

**Reseta o contador de vitórias de um cristal de raid ou de um jogador.**

```
/crd resetclears <jogador>
/crd resetclears <x> <y> <z> [dimensão]
```

- `<jogador>` — Nome ou seletor do jogador (@s, @a, etc.) cujas vitórias serão resetadas.
- `<x> <y> <z>` — Coordenadas do cristal a resetar.
- `[dimensão]` — Dimensão do cristal (ex: `minecraft:overworld`). Se omitido, usa todas as dimensões.

**Exemplos:**
```
/crd resetclears @s
/crd resetclears Steve
/crd resetclears 100 64 200 minecraft:overworld
```

**Para que serve:** Se um jogador atingiu o limite de vitórias num cristal e você quer permitir que ele jogue novamente antes do reset automático.

---

## `/crd refresh`

**Remove um jogador de todos os estados de raid ativos.**

```
/crd refresh [jogador]
```

- `[jogador]` — Nome ou seletor do jogador. Se omitido, afeta o próprio executor do comando.

**Exemplos:**
```
/crd refresh
/crd refresh @s
/crd refresh Steve
```

**Para que serve:** Use quando um jogador ficar preso em estado de "em raid" por causa de bug, desconexão ou erro. Limpa a fila e a participação ativa do jogador.

> **Nota:** Não pode ser usado em jogadores que estão ativamente no meio de uma batalha de raid. A mensagem *"Você não pode atualizar um jogador que está no meio de uma raid."* aparece nesses casos.

---

## `/crd forceclear`

**Força o encerramento de uma raid em andamento para um jogador específico.**

```
/crd forceclear [jogador]
```

- `[jogador]` — Nome ou seletor do jogador. Se omitido, afeta o executor do comando.

**Exemplos:**
```
/crd forceclear
/crd forceclear @s
/crd forceclear Steve
```

**Para que serve:** Encerra qualquer raid em andamento para o jogador especificado, teleportando-o de volta e concluindo a raid forçadamente. Útil para situações de erro ou para destravar jogadores presos na dimensão de raid.

---

## Mensagens de Erro Comuns

| Mensagem | Causa |
|----------|-------|
| *"Você já está hospedando outra raid."* | Tentou iniciar uma raid enquanto já está hospedando outra. Use `/crd refresh` para resolver. |
| *"Dimensão inválida."* | Dimensão especificada no comando não existe. |
| *"Ainda há jogadores nessa dimensão."* | Tentou encerrar uma dimensão de raid que ainda tem jogadores dentro. |
| *"Você não pode usar esse comando em uma raid."* | Alguns comandos ficam bloqueados durante batalhas de raid. |
