# Morte e Drops — Proteção de Itens ao Morrer

## Como Funciona a Proteção de Drops

Quando você morre no servidor, seus itens caem no chão normalmente — mas ficam **bloqueados para outros jogadores**. Mesmo que outro jogador esteja no mesmo lugar, ele não consegue pegar seus itens.

Essa proteção está sempre ativa no servidor, independente de qual claim você morreu (mesmo fora de qualquer claim).

---

## Pegar Seus Próprios Itens

Após morrer, volte ao local onde morreu e pegue seus itens normalmente. Ninguém mais pode pegar enquanto eles estão bloqueados.

---

## Desbloquear Seus Itens Para Outros

Se você quiser que outros jogadores possam pegar seus itens de morte (por exemplo, para alguém devolver seus itens a você), use:

```
/flan unlockDrops
```

Após executar esse comando, qualquer jogador pode pegar seus itens do chão.

---

## Desbloquear Itens de Outro Jogador

Se um administrador ou alguém com permissão especial precisar liberar os drops de outro jogador:

```
/flan unlockDrops <nome_do_jogador>
```

---

## Mods de Tumba

O servidor tem mods de tumba configurados (como `universal_graves` e `yigd`). Esses mods podem guardar seus itens em uma tumba ao invés de simplesmente jogar no chão. Se isso estiver ativo, os itens ficam ainda mais seguros — verifique com os admins do servidor qual comportamento está ativo.

As tumbas desses mods são **sempre acessíveis** pelo dono, mesmo dentro de claims de outros jogadores. O sistema de claim não bloqueia o acesso a tumbas de morte.

---

## Itens que Ficam Bloqueados

Todos os itens do inventário ficam bloqueados ao morrer, incluindo:
- Itens na mão e armadura
- Itens no inventário principal
- Itens no offhand

A proteção dura até que os itens desapareçam naturalmente do jogo (tempo padrão do Minecraft é 5 minutos) ou até você desbloquear manualmente com `/flan unlockDrops`.

---

## Claims e Proteção de PvP

Dentro de claims, por padrão, a permissão `flan:hurt_player` está **desativada para Visitors**. Isso significa que em claims normais, outros jogadores não conseguem te atacar.

Se um dono de claim ativar PvP no claim dele (`flan:hurt_player = true`), você pode morrer dentro do claim. Seus itens ainda ficam bloqueados pelo sistema de drops.

Fora de claims (áreas sem proteção), PvP é definido pelas configurações gerais do servidor, não pelo Flan.
