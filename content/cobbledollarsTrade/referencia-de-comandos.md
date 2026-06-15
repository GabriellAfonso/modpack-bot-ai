# Referência Completa de Comandos do CobleTrade

Esta página lista todos os comandos do mod CobleTrade, que adiciona comércio entre jogadores usando a moeda CobbleDollars (símbolo ₵). Todos os comandos começam com `/trade`.

## /trade pay — Enviar dinheiro

```
/trade pay <jogador> <valor>
```

Envia CobbleDollars (₵) diretamente para outro jogador, sem trocas nem itens. O `<jogador>` precisa estar online e o `<valor>` precisa ser um número inteiro de pelo menos 1. O valor sai do seu saldo e entra no do destinatário na hora. Falha se você tentar pagar a si mesmo ou se não tiver saldo suficiente.

## /trade offer pokemon — Vender um Pokémon

```
/trade offer pokemon <slot> <preço> <jogador>
```

Cria uma oferta privada para vender um Pokém do seu time. `<slot>` é a posição no time, de 1 a 6. `<preço>` é o valor em ₵ (inteiro, mínimo 1). `<jogador>` é o comprador, que precisa estar online. O Pokémon sai do seu time e fica reservado até a oferta ser respondida. Exige pelo menos 2 Pokémon no time, que o Pokémon seja negociável, e que o slot não esteja vazio. Você não pode ofertar para si mesmo.

## /trade offer item — Vender itens

```
/trade offer item <quantidade> <preço> <jogador>
```

Cria uma oferta privada para vender itens da sua mão principal. Segure o item antes de usar o comando. `<quantidade>` é quantas unidades vender (mínimo 1, no máximo o que você tem na mão). `<preço>` é o valor total em ₵ (inteiro, mínimo 1). `<jogador>` é o comprador, que precisa estar online. Os itens saem da sua mão e ficam reservados até a oferta ser respondida. Você não pode ofertar para si mesmo.

## /trade offers — Ver ofertas recebidas

```
/trade offers
```

Abre um menu com todas as ofertas de venda que outros jogadores enviaram para você. Clicando em uma oferta você vê os detalhes e pode **aceitar** (comprar, debitando o preço do seu saldo) ou **recusar** (devolvendo o conteúdo ao vendedor). Não custa nada apenas abrir e olhar.

## /trade myoffers — Ver ofertas enviadas

```
/trade myoffers
```

Abre um menu com todas as ofertas de venda que você criou e ainda estão pendentes. Clicando em uma oferta você vê os detalhes e pode **cancelar**, recuperando o Pokémon ou item que tinha colocado à venda.

## Observações gerais sobre os comandos

- Todos os preços e valores são números inteiros e precisam ser de pelo menos 1 ₵.
- Os comandos `/trade pay`, `/trade offer pokemon` e `/trade offer item` exigem que o outro jogador esteja **online** no momento de criar a ação.
- Não há nenhum comando que exija permissão de operador (admin) para uso normal; qualquer jogador pode usar todos os comandos acima.
