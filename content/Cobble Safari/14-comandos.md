# Comandos do CobbleSafari

## Comandos para Jogadores

Esses comandos podem ser usados por qualquer jogador sem permissões especiais:

| Comando | Efeito |
|---------|--------|
| `/safariexit` | Sai da Safari Zone e retorna ao ponto de origem (onde você entrou). Útil se quiser sair antes do timer acabar. |

---

## Comandos de Timer (Staff)

Gerenciamento do timer de sessão dos jogadores na Safari Zone e nas Dungeons:

### Timer da Safari Zone

| Comando | Efeito |
|---------|--------|
| `/cobblesafari timer safari add <jogador> <segundos>` | Adiciona tempo ao timer do jogador na Safari Zone |
| `/cobblesafari timer safari remove <jogador> <segundos>` | Remove tempo do timer |
| `/cobblesafari timer safari set <jogador> <segundos>` | Define o timer para um valor exato |
| `/cobblesafari timer safari get <jogador>` | Mostra o tempo restante do jogador |
| `/cobblesafari timer safari toggle <jogador>` | Ativa/desativa o bypass de timer (jogador fica sem limite de tempo) |

### Timer de Dimensão Específica (Dungeons)

| Comando | Efeito |
|---------|--------|
| `/cobblesafari timer dimension add <jogador> <segundos> <dimensão>` | Adiciona tempo em dimensão específica |
| `/cobblesafari timer dimension remove <jogador> <segundos> <dimensão>` | Remove tempo |
| `/cobblesafari timer dimension set <jogador> <segundos> <dimensão>` | Define tempo |
| `/cobblesafari timer dimension get <jogador> <dimensão>` | Verifica tempo restante |

IDs de dimensão: `cobblesafari:domedimension` (Safari), `cobblesafari:dungeon_underground`, `cobblesafari:dungeon_distortion`, `cobblesafari:dungeon_jump`

---

## Comandos de Reset (OP Nível 4)

**Atenção**: Esses comandos são destrutivos e afetam todos os jogadores.

| Comando | Efeito |
|---------|--------|
| `/cobblesafari reset safari` | Reseta a dimensão Safari Zone e todos os timers dos jogadores |
| `/cobblesafari reset dungeon` | Limpa todas as dimensões de dungeon ativas |
| `/cobblesafari refresh` | Recarrega todos os arquivos de configuração do mod sem reiniciar o servidor |

---

## Comandos de Dungeon (Staff)

| Comando | Efeito |
|---------|--------|
| `/cobblesafari dungeon spawn` | Força o spawn de um portal de dungeon aleatório perto de você |
| `/cobblesafari dungeon spawn force [jogador] [id_dungeon]` | Força spawn de uma dungeon específica perto do jogador |
| `/cobblesafari dungeon list` | Lista todos os portais de dungeon ativos |
| `/cobblesafari dungeon list force` | Escaneia o mundo e lista todos os portais |
| `/cobblesafari dungeon dimensions` | Lista todas as dungeons registradas no sistema |

IDs de dungeon: `dungeon_underground`, `dungeon_distortion`, `dungeon_jump`

---

## Comandos de NPC Trader (OP Nível 2)

| Comando | Efeito |
|---------|--------|
| `/cobblesafari summon <nome> <variante>` | Spawna um NPC trader com template específico |
| `/cobblesafari summon_template <nome> <variante>` | Spawna usando template de trader |

Exemplos de traders disponíveis:
- `hiker small` — Hiker com esferas pequenas
- `hiker large` — Hiker com esferas grandes
- `hiker treasure` — Hiker que compra fósseis
- `hexmaniac ghost_relics` — Hex Maniac com itens fantasma

---

## Comandos de Donut (OP Nível 4)

| Comando | Efeito |
|---------|--------|
| `/donut random <sabor> <tier> <quantidade>` | Gera donuts aleatórios com o sabor e tier definidos |
| `/donut custom <bonus1> <bonus2> <bonus3> <quantidade>` | Cria donuts com bônus específicos |

Sabores válidos: `sweet`, `dry`, `sour`, `spicy`, `bitter`
Formato de bônus: `poder:nivel:tipo` (ex: `capture:2:dry`)

---

## Notas Importantes

- Comandos sem nível de OP especificado podem ser usados por qualquer jogador (ou requerem permissão configurada pelo servidor).
- O comando `/cobblesafari refresh` permite que a staff atualize configurações sem reiniciar — útil para ajustes rápidos.
- Usar `/safariexit` não consome o timer — ele apenas te teleporta de volta.
