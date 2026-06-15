# Comandos do Flan — Referência Completa para Jogadores

## Como Usar Esta Lista

Todos os comandos começam com `/flan`. Parâmetros entre `<>` são obrigatórios, entre `[]` são opcionais.

---

## Gerenciamento de Claims

| Comando | O que faz |
|---|---|
| `/flan add <pos1> <pos2>` | Cria claim entre duas coordenadas. Formato: `x,y,z` |
| `/flan add rect <largura> <comprimento>` | Cria claim retangular centralizado em você |
| `/flan add all` | Usa todos os blocos disponíveis para criar o maior claim possível ao redor de você |
| `/flan expand <distância>` | Expande o claim atual na direção que você está olhando |
| `/flan delete` | Deleta o claim onde você está |
| `/flan deleteAll` | Deleta todos os seus claims (pede confirmação) |
| `/flan deleteSubClaim` | Deleta o subclaim onde você está (requer modo subclaim ativo) |
| `/flan deleteAllSubClaims` | Deleta todos os subclaims do claim atual (pede confirmação) |
| `/flan transferClaim <jogador>` | Transfere a posse do claim atual para outro jogador |
| `/flan name <nome>` | Define o nome do claim onde você está |

---

## Informações e Listagem

| Comando | O que faz |
|---|---|
| `/flan info` | Mostra detalhes do claim onde você está (dono, coordenadas, subclaims) |
| `/flan list` | Lista todos os seus claims com coordenadas e nomes |
| `/flan claimBlocks` | Mostra seus blocos de claim: total, bônus, em uso e disponíveis |

---

## Grupos e Permissões

| Comando | O que faz |
|---|---|
| `/flan menu` | Abre o menu visual de gerenciamento do claim atual |
| `/flan personalGroups` | Abre menu para editar grupos padrão de claims futuros |
| `/flan group add <nome>` | Cria um novo grupo no claim atual |
| `/flan group remove <nome>` | Remove um grupo do claim atual |
| `/flan group players add <grupo> <jogador>` | Adiciona jogador ao grupo no claim atual |
| `/flan group players remove <grupo> <jogador>` | Remove jogador do grupo no claim atual |
| `/flan permission global <perm> <true\|false\|default>` | Define permissão global do claim atual |
| `/flan permission group <grupo> <perm> <true\|false\|default>` | Define permissão de um grupo no claim atual |
| `/flan permission personal <grupo> <perm> <true\|false\|default>` | Define permissão padrão para claims futuros |

**Exemplos de permissões:** `flan:break`, `flan:open_container`, `flan:hurt_player`, `flan:explosions`

---

## Modos de Criação

| Comando | O que faz |
|---|---|
| `/flan switchMode default` | Modo padrão 2D — claims com profundidade de 10 blocos abaixo |
| `/flan switchMode default.3d` | Modo 3D — você define a altura manualmente |
| `/flan switchMode subclaim` | Modo subclaim 2D — cria subclaims dentro do claim atual |
| `/flan switchMode subclaim.3d` | Modo subclaim 3D — subclaims com altura definida manualmente |

---

## Home e Teleporte

| Comando | O que faz |
|---|---|
| `/flan setHome` | Define o ponto de teleporte no local onde você está (dentro do claim) |
| `/flan teleport self <nome_do_claim>` | Teleporta para o home de um claim seu |

> **Nota:** Por padrão do servidor, apenas o dono do claim pode usar teleporte.

---

## Mensagens do Claim

| Comando | O que faz |
|---|---|
| `/flan claimMessage enter title string <texto>` | Define título que aparece ao entrar no claim |
| `/flan claimMessage enter subtitle string <texto>` | Define subtítulo ao entrar |
| `/flan claimMessage leave title string <texto>` | Define título ao sair do claim |
| `/flan claimMessage leave subtitle string <texto>` | Define subtítulo ao sair |
| `/flan claimMessage enter title string $empty` | Remove a mensagem de entrada |

Use `%s` no texto para inserir o nome do claim automaticamente.
Use `text` em vez de `string` para texto com formatação JSON.

---

## Itens e Drops de Morte

| Comando | O que faz |
|---|---|
| `/flan unlockDrops` | Desbloqueia seus itens de morte para outros jogadores pegarem |
| `/flan unlockDrops <jogador>` | Desbloqueia os itens de morte de outro jogador (requer permissão) |

Por padrão, itens ao morrer ficam travados — só o dono pode pegar. Use esse comando para liberar voluntariamente.

---

## Listas de Exceção

| Comando | O que faz |
|---|---|
| `/flan ignoreList add <tipo> <valor>` | Adiciona item/bloco/entidade à lista de exceção |
| `/flan ignoreList remove <tipo> <valor>` | Remove da lista de exceção |
| `/flan ignoreList state <tipo> <whitelist\|blacklist>` | Define se a lista é whitelist ou blacklist |

**Tipos disponíveis:** `flan:block_break`, `flan:block_use`, `flan:entity_attack`, `flan:entity_use`, `flan:item`, `flan:item_drop`, `flan:item_pickup`

---

## Fake Players

| Comando | O que faz |
|---|---|
| `/flan fakePlayer add <uuid>` | Autoriza um fake player a interagir com o claim |
| `/flan fakePlayer remove <uuid>` | Remove autorização de um fake player |
| `/flan fakePlayerNotification` | Ativa/desativa notificações de tentativas de fake players |

---

## Utilitários

| Comando | O que faz |
|---|---|
| `/flan trapped` | Teleporta você para fora de um claim após 5 segundos se você estiver preso |
| `/flan confirm confirm` | Confirma uma operação que pediu confirmação |
| `/flan confirm deny` | Cancela uma operação que pediu confirmação |
| `/flan help [página]` | Mostra lista de comandos disponíveis |
| `/flan ? cmd <comando>` | Mostra ajuda detalhada para um comando específico |

---

## Resumo das Permissões por Argumento

Quando um comando pede `<perm>`, use um dos nomes abaixo:

**Construção:** `flan:break` `flan:place` `flan:trample`  
**Contêineres:** `flan:open_container` `flan:door` `flan:fence_gate` `flan:trapdoor` `flan:bed` `flan:anvil` `flan:enchantment` `flan:enderchest` `flan:jukebox` `flan:noteblock` `flan:button_lever` `flan:pressure_plate` `flan:redstone` `flan:lectern_take` `flan:beacon` `flan:target_block`  
**Itens:** `flan:drop` `flan:pickup` `flan:xp` `flan:bucket`  
**Entidades:** `flan:hurt_player` `flan:hurt_animal` `flan:hurt_named` `flan:animal_interact` `flan:trading` `flan:armorstand`  
**Movimento:** `flan:can_stay` `flan:ender_pearl` `flan:chorus_fruit` `flan:portal` `flan:boat` `flan:minecart` `flan:vehicle_pass`  
**Mundo:** `flan:explosions` `flan:wither` `flan:fire_spread` `flan:lightning` `flan:water_border` `flan:piston_border` `flan:enderman`  
**Spawn:** `flan:disable_monster_spawn` `flan:disable_mob_spawn`  
**Admin:** `flan:edit_claim` `flan:edit_perms` `flan:claim_message` `flan:no_hunger` `flan:flight` `flan:may_flight` `flan:teleport`
