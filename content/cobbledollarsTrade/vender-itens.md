# Vender Itens para Outro Jogador

## O que é uma oferta de item

Uma oferta de item é uma proposta de venda privada onde você coloca uma quantidade de um item do seu inventário à venda por um preço em CobbleDollars (₵, a moeda do servidor) para um jogador específico. Só o jogador escolhido pode aceitar. Enquanto a oferta existe, os itens são **retirados da sua mão** e ficam guardados pelo sistema até a oferta ser aceita, recusada ou cancelada.

## Como criar uma oferta de item

Primeiro, **segure na mão principal** o item que você quer vender. Depois use o comando no chat:

```
/trade offer item <quantidade> <preço> <jogador>
```

- `<quantidade>` é quantas unidades do item segurado você quer vender. Precisa ser pelo menos 1 e não pode passar da quantidade que você tem na mão.
- `<preço>` é o valor total em ₵ que você cobra por essa quantidade, um número inteiro de pelo menos 1.
- `<jogador>` é o nome do jogador que vai receber a oferta. Ele precisa estar **online**.

Exemplo: segurando um maço de Poké Bolas, `/trade offer item 10 800 Brock` coloca 10 Poké Bolas à venda por 800 ₵ para o jogador Brock.

## Requisitos para vender itens

Para a oferta ser criada, todas estas condições precisam ser verdadeiras:

- Você precisa estar **segurando um item na mão principal**. Com a mão vazia aparece "Você precisa segurar o item na mão principal."
- A quantidade pedida **não pode ser maior** que o número de itens na sua mão. Se você pedir mais do que tem, aparece "Você só tem \<quantidade\>x \<item\> na mão."
- Você **não pode enviar a oferta para si mesmo**.

## O que acontece ao criar a oferta

Quando a oferta é criada com sucesso:

- A quantidade vendida é **removida da sua mão** na hora e fica guardada pelo sistema (com todas as características do item, como encantamentos e nome personalizado, preservadas).
- Você vê: "Oferta de \<quantidade\>x \<item\> por ₵\<preço\> enviada para \<jogador\>!"
- O jogador escolhido recebe: "\<você\> enviou uma oferta de \<quantidade\>x \<item\> por ₵\<preço\>! Use /trade offers para ver."

A oferta fica pendente até o comprador decidir. Você pode cancelá-la a qualquer momento pelo menu de ofertas enviadas (comando `/trade myoffers`), e os itens voltam para você.

## Para onde os itens vão ao ser vendidos

Quando o comprador aceita a oferta, os itens vão para o **inventário** dele. Se o inventário do comprador estiver cheio, os itens são **largados no chão** ao lado dele para não se perderem.
