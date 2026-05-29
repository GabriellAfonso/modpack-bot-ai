# GTS / Market — comprar e vender Pokémon e itens (Cobblemon Global Trading System)

> Documento de referência para assistente de IA responder dúvidas de jogadores.
> Mod: Global Trading System para Cobblemon. Permite vender/comprar Pokémon e Items entre jogadores via mercado global
com economia.

## Visão Geral

O GTS é um mercado global. Jogadores listam Pokémon (da party) ou Items (da mão) por um preço. Outros jogadores
compram pagando com a economia do servidor (via Impactor). Anúncios têm duração limitada; ao expirar, o item/Pokémon
volta pro vendedor numa aba de "expirados" para reclamar ou relistar.

**Comando base no servidor: `/market`** (alias: `market`).
Toda a interação é feita por GUI (menus clicáveis) ou pelos subcomandos abaixo.

> Observação: mensagens de ajuda internas do mod ainda exibem o texto antigo `gts ...`. O comando real é `/market`.

## Comandos

| Comando | O que faz | Permissão | Nível |
|---|---|---|---|
| `/market` | Abre a GUI principal com todos os anúncios | `gts.user.base` | 0 |
| `/market pokemon` | Abre a GUI só de Pokémon à venda | `gts.user.base` | 0 |
| `/market item` | Abre a GUI só de Items à venda | `gts.user.base` | 0 |
| `/market <listing-id>` | Abre um anúncio específico pelo ID (UUID) | `gts.user.base` | 0 |
| `/market sell pokemon <slot> <price>` | Lista um Pokémon da party (slot 1–6) | `gts.user.sell` | 0 |
| `/market sell item <price> <amount> [stackSize]` | Lista o item da mão | `gts.user.sell` | 0 |
| `/market manage` | GUI dos seus anúncios ativos (pode cancelar) | `gts.user.manage` | 0 |
| `/market expired` | GUI dos seus anúncios expirados (reclamar/relistar) | `gts.user.expired` | 0 |
| `/market history` | GUI do histórico de vendas | `gts.user.history` | 0 |
| `/market search <texto>` | Busca anúncios por nome | `gts.user.search` | 0 |
| `/market getprice` | Preço médio de venda do item na mão | `gts.user.price` | 0 |
| `/market getprice <slot>` | Preço médio de venda do Pokémon no slot | `gts.user.price` | 0 |
| `/market timeout <player> <days/hours/minutes/seconds> <amount>` | Bane jogador de usar o GTS por um tempo (rodar de
novo no mesmo jogador remove o timeout) | `gts.moderation.timeout` | 2 |
| `/market reload` | Recarrega config e lang | `gts.admin.reload` | 3 |
| `/market saveitem` | Salva o item da mão em `item.json` (admin, para config) | `gts.admin.saveitem` | 3 |
| `/market itemdesc` | Mostra o description ID do item da mão (admin) | `gts.admin.itemdesc` | 3 |
| `/market debug` | Liga/desliga modo debug (anúncios duram 10s) | `gts.admin.debug` | 3 |

> Permissão `gts.moderation.remove` (nível 2) existe para moderadores removerem anúncios alheios pela GUI.

## Como Vender

### Pokémon
`/market sell pokemon <slot> <price>`
- `slot`: posição na party, 1 a 6.
- O Pokémon sai da party assim que listado.
- Regras que **bloqueiam** a venda:
  - Pokémon não-tradeable.
  - Você precisa ter **pelo menos 2 Pokémon** na party (não dá pra ficar sem nenhum).
  - Não pode estar **em batalha**.
  - Não pode estar sob **timeout** (moderação).
  - Pokémon na **lista de banidos** da config.
  - Preço abaixo do **mínimo** ou acima do **máximo**.
  - Já estar no **limite de anúncios** por jogador.

### Item
`/market sell item <price> <amount> [stackSize]`
- Vende o item segurado na **mão principal**.
- `amount`: quantidade total a listar.
- `stackSize` (opcional): tamanho de cada stack. Se informado, cria vários anúncios de `amount / stackSize` cada.
`amount` precisa ser divisível por `stackSize`, e `stackSize` não pode ser maior que `amount`.
- Bloqueios: item banido, sem item na mão, quantidade 0, itens insuficientes no inventário, preço fora do min/max,
limite de anúncios atingido.

## Preço Mínimo (Pokémon)

Neste servidor **não há preço mínimo configurado** — IVs, Hidden Ability, Lendários e Ultra Beasts não impõem nenhum
valor mínimo. O único limite é o preço máximo de **999.999.999**.

O mod suporta preços mínimos por IV/HA/lendário/UB (configuráveis pelo admin), mas estão todos em 0 aqui.

## Compra, Imposto e Economia

- Comprar exige saldo suficiente.
- Neste servidor **não há imposto** (`taxRate = 0%`): o vendedor recebe o valor integral da venda.
- Pokémon comprado vai pra party do comprador; item comprado vai pro inventário.
- A venda é registrada no histórico; preço médio fica disponível via `/market getprice`.

## Duração e Expiração

- Duração padrão: **72 horas** (`listingDuration`, em horas, configurável).
- Se `listingDuration <= 0`, anúncios **não expiram**.
- Em modo debug, anúncios duram 10 segundos.
- Ao expirar, o anúncio vai para **`/market expired`**, onde o vendedor pode **reclamar de volta** ou **relistar** (há
botão "Relist All" para relistar todos).
- Anúncios expirados **contam** para o limite de anúncios por jogador até serem reclamados.

## Limites e Configuração Principal

| Config | Padrão | Descrição |
|---|---|---|
| `maxListingsPerPlayer` | 15 | Máximo de anúncios (ativos + expirados não reclamados) por jogador |
| `listingDuration` | 72 | Duração em horas (≤0 = sem expiração) |
| `taxRate` | 0 | Sem imposto — vendedor recebe 100% do valor |
| `maximumPrice` | 999999999 | Preço máximo de qualquer anúncio |
| `enablePokemonSales` | true | Permite vender Pokémon |
| `enableItemSales` | true | Permite vender Items |
| `broadcastListings` | true | Anuncia novos listings no chat (link clicável) |
| `enablePermissionNodes` | true | Usa nós de permissão (true) ou níveis de operador (false) |
| `enableAsyncSearches` | false | Roda a query da GUI principal de forma assíncrona |
| `showBreedable` | false | Considera a tag "breedable" |
| `bannedItems` | — | Nenhum item banido |
| `bannedPokemon` | — | Pokémon que não podem ser vendidos |
| `customItemPrices` / `customPokemonPrices` | — | Preços mínimos específicos |
| `discord` (webhook) | — | Webhooks de Discord para novos/vendidos |


## Permissões (nós)

- Usuário: `gts.user.base`, `gts.user.sell`, `gts.user.manage`, `gts.user.expired`, `gts.user.history`,
`gts.user.search`, `gts.user.price`.
- Moderação (nível 2): `gts.moderation.timeout`, `gts.moderation.remove`.
- Admin (nível 3): `gts.admin.reload`, `gts.admin.saveitem`, `gts.admin.itemdesc`, `gts.admin.debug`.

Se `enablePermissionNodes` for `false`, usa o nível de OP indicado (0 = todos, 2 = moderador, 3 = admin).

## Perguntas Frequentes (para o assistente)

- **"Como vendo um Pokémon?"** → `/market sell pokemon <slot 1-6> <preço>`. Precisa de ≥2 na party, fora de batalha,
Pokémon tradeable.
- **"Como vendo um item?"** → Segure o item e use `/market sell item <preço> <quantidade> [tamanho do stack]`.
- **"Por que não consigo vender? Preço muito baixo."** → Neste servidor não há preço mínimo configurado. O bloqueio
por preço só ocorre se o valor for 0 ou ultrapassar 999.999.999. Verifique outras restrições (Pokémon não-tradeable,
party com menos de 2, em batalha, limite de anúncios atingido).
- **"Quanto recebo de uma venda?"** → O valor integral — não há imposto neste servidor (taxRate = 0%).
- **"Meu anúncio sumiu."** → Provavelmente expirou (72h). Veja `/market expired` para reclamar ou relistar.
- **"Quantos anúncios posso ter?"** → 15 (ativos + expirados não reclamados juntos).
- **"Quanto vale tal item/Pokémon?"** → `/market getprice` (item na mão) ou `/market getprice <slot>` (Pokémon).
Mostra preço médio histórico; se nunca foi vendido, não há dado.
- **"Não consigo usar o mercado."** → Pode estar sob timeout de moderação. A mensagem mostra o tempo restante.
- **"Como compro?"** → Abra `/market`, `/market pokemon` ou `/market item`, clique no anúncio e confirme (precisa de
saldo).
