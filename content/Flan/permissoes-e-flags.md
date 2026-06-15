# Permissões e Flags — O que Cada Permissão Controla

## Como Funcionam as Permissões

Cada claim tem uma lista de permissões (também chamadas de "flags") que controlam o que é permitido ou bloqueado dentro da área. Você pode configurar essas permissões:

- **Por grupo** — define o que um grupo específico (Visitor, Co-Owner, grupos personalizados) pode fazer
- **Globalmente** — define o comportamento padrão para todos que entram no claim, independente de grupo

Cada permissão tem três estados possíveis:
- **Ativada (true)** — a ação é permitida
- **Desativada (false)** — a ação é bloqueada
- **Padrão (default)** — usa o valor global do servidor

---

## Como Editar Permissões

**Via menu visual** (recomendado):
```
/flan menu
```
Abre o menu do claim onde você clica nos itens para editar permissões de grupos.

**Via comando para grupos:**
```
/flan permission group <nome_do_grupo> <permissão> <true|false|default>
```
Exemplo: `/flan permission group Visitor flan:open_container true`

**Via comando global do claim:**
```
/flan permission global <permissão> <true|false|default>
```
Exemplo: `/flan permission global flan:explosions false`

---

## Permissões de Construção

| Permissão | O que controla |
|---|---|
| `flan:break` | Quebrar blocos |
| `flan:place` | Colocar blocos |
| `flan:trample` | Pisotear plantações e ovos de tartaruga |
| `flan:archeology` | Usar pincel arqueológico em blocos |

---

## Permissões de Contêineres e Interação com Blocos

| Permissão | O que controla |
|---|---|
| `flan:open_container` | Abrir baús, fornalhas, barris, hoppers, etc. |
| `flan:interact_block` | Interagir com blocos em geral (fallback genérico) |
| `flan:interact_sign` | Colorir placas com corante |
| `flan:button_lever` | Usar alavancas e botões |
| `flan:pressure_plate` | Ativar placas de pressão |
| `flan:noteblock` | Alterar blocos de nota |
| `flan:redstone` | Interagir com componentes de redstone |
| `flan:door` | Usar portas |
| `flan:fence_gate` | Usar portões de cerca |
| `flan:trapdoor` | Usar alçapões |
| `flan:bed` | Usar camas |
| `flan:anvil` | Usar bigornas |
| `flan:beacon` | Usar faróis (beacons) |
| `flan:jukebox` | Colocar e retirar discos de música |
| `flan:enchantment` | Usar mesa de encantamento |
| `flan:enderchest` | Usar baús de ender |
| `flan:lectern_take` | Trocar livros em púlpitos (lecterns) |
| `flan:target_block` | Ativar blocos-alvo |
| `flan:itemframe_rotate` | Rotacionar itens em molduras de item |

---

## Permissões de Itens e Inventário

| Permissão | O que controla |
|---|---|
| `flan:drop` | Largar itens no chão |
| `flan:pickup` | Pegar itens do chão |
| `flan:xp` | Pegar orbes de experiência |
| `flan:bucket` | Usar balde para pegar/colocar líquidos |
| `flan:lock_items` | Itens ficam bloqueados no chão ao morrer (padrão do servidor: **sempre ativo**) |

---

## Permissões de Movimento e Teleporte

| Permissão | O que controla |
|---|---|
| `flan:can_stay` | Permite jogadores entrarem no claim (se desativado, jogadores são expulsos ao entrar) |
| `flan:ender_pearl` | Usar pérolas de ender para teleportar |
| `flan:chorus_fruit` | Comer fruta de chorus para teleportar |
| `flan:portal` | Usar portais do Nether |
| `flan:teleport` | Teleportar para o home do claim via comando (padrão do servidor: **desativado**) |
| `flan:flight` | Voar com elytra ou mods de voo (padrão do servidor: **sempre permitido**) |
| `flan:may_flight` | Voar com modo de voo ativado por admin (padrão do servidor: **desativado**) |
| `flan:vehicle_pass` | Veículos (minecarts, barcos) podem cruzar as bordas do claim |
| `flan:boat` | Usar barcos |
| `flan:minecart` | Entrar em minecarts |
| `flan:ender_pearl` | Usar pérolas de ender |
| `flan:wind_charge` | Usar cargas de vento |

---

## Permissões de Entidades e Animais

| Permissão | O que controla |
|---|---|
| `flan:hurt_animal` | Atacar animais passivos (vacas, ovelhas, etc.) |
| `flan:hurt_named` | Atacar mobs com nome (nametagged) |
| `flan:hurt_player` | Atacar outros jogadores (PvP) |
| `flan:animal_interact` | Interagir com animais (tosquiar, ordenhar, montar) |
| `flan:trading` | Negociar com aldeões |
| `flan:armorstand` | Interagir com suportes de armadura |
| `flan:break_non_living` | Quebrar minecarts, barcos ou suportes de armadura |
| `flan:fake_player` | Permitir "fake players" (jogadores criados por mods) interagirem |

---

## Permissões de Eventos e Mecânicas do Mundo

| Permissão | O que controla |
|---|---|
| `flan:explosions` | Explosões causam dano a blocos dentro do claim |
| `flan:wither` | Wither pode destruir blocos no claim |
| `flan:fire_spread` | Fogo se espalha dentro do claim |
| `flan:lightning` | Raios afetam o claim (acendem fogo, afetam animais) |
| `flan:water_border` | Água pode cruzar as bordas do claim |
| `flan:piston_border` | Pistões podem mover blocos através das bordas do claim |
| `flan:enderman` | Endermen podem pegar e colocar blocos no claim |
| `flan:snow_golem` | Golems de neve podem colocar neve no claim |
| `flan:sculk` | Sensores sculk funcionam normalmente |
| `flan:raid` | Raids podem ocorrer no claim |
| `flan:projectiles` | Projéteis (flechas) ativam blocos (botões, alvos) |
| `flan:endcrystal_place` | Colocar cristais do End |

---

## Permissões de Spawn de Mobs

| Permissão | O que controla |
|---|---|
| `flan:disable_monster_spawn` | Impede spawn de mobs hostis no claim (padrão do servidor: **desativado** — mobs hostes spawnam normalmente) |
| `flan:disable_mob_spawn` | Impede spawn de todos os mobs no claim (padrão do servidor: **desativado**) |
| `flan:player_mob_spawn` | Jogadores podem invocar mobs por interação (guardiões, endermitas) |

---

## Permissões Especiais

| Permissão | O que controla |
|---|---|
| `flan:edit_claim` | Editar bordas do claim (expandir, deletar) |
| `flan:edit_perms` | Alterar permissões do claim |
| `flan:claim_message` | Editar mensagens de entrada/saída do claim |
| `flan:no_hunger` | Jogadores não perdem fome no claim (padrão do servidor: **desativado**) |
| `flan:edit_potions` | Editar efeitos de poção que se aplicam no claim (padrão do servidor: **desativado**) |
| `flan:beacon` | Usar beacons |
| `flan:xp` | Pegar orbs de XP |

---

## Resumo dos Padrões do Servidor

Estas permissões têm comportamento fixo em **todos os claims do servidor** independente de configuração individual:

| Permissão | Comportamento Padrão |
|---|---|
| `flan:flight` | **Sempre permitido** — todo jogador pode usar elytra e outros modos de voo |
| `flan:lock_items` | **Sempre ativo** — itens ficam bloqueados no chão ao morrer |
| `flan:disable_monster_spawn` | **Sempre desativado** — mobs hostis spawnam normalmente |
| `flan:teleport` | **Sempre desativado** — jogadores não podem teleportar para homes de claims de outros |
| `flan:no_hunger` | **Sempre desativado** — fome funciona normalmente |
| `flan:may_flight` | **Sempre desativado** — modo de voo admin não é liberado por padrão |
| `flan:edit_potions` | **Sempre desativado** — jogadores não podem adicionar efeitos ao claim |
