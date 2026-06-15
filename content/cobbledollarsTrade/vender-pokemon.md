# Vender um Pokémon para Outro Jogador

## O que é uma oferta de Pokémon

Uma oferta de Pokémon é uma proposta de venda privada onde você coloca um Pokémon do seu time à venda por um preço em CobbleDollars (₵, a moeda do servidor) para um jogador específico. Só o jogador escolhido pode aceitar a oferta. Enquanto a oferta existe, o Pokémon fica **reservado fora do seu time**, guardado pelo sistema até a oferta ser aceita, recusada ou cancelada.

## Como criar uma oferta de Pokémon

Use o comando no chat com este formato:

```
/trade offer pokemon <slot> <preço> <jogador>
```

- `<slot>` é a posição do Pokémon no seu time, de **1 a 6** (o slot 1 é o primeiro Pokémon).
- `<preço>` é quanto você quer cobrar em ₵, um número inteiro de pelo menos 1.
- `<jogador>` é o nome do jogador que vai receber a oferta. Ele precisa estar **online**.

Exemplo: `/trade offer pokemon 2 1500 Misty` coloca o Pokémon do slot 2 do seu time à venda por 1500 ₵ para a jogadora Misty.

## Requisitos para vender um Pokémon

Para a oferta ser criada, todas estas condições precisam ser verdadeiras:

- O slot informado precisa **conter um Pokémon**. Se o slot estiver vazio, aparece "Nenhum Pokémon no slot \<número\>."
- O Pokémon precisa ser **negociável**. Alguns Pokémon não podem ser trocados; nesse caso aparece "\<nome\> não pode ser trocado."
- Você precisa ter **pelo menos 2 Pokémon no time**. O sistema não deixa você esvaziar seu time por completo; se você tiver só 1, aparece "Você precisa de pelo menos 2 Pokémon no party para enviar uma oferta."
- Você **não pode enviar a oferta para si mesmo**.

## O que acontece ao criar a oferta

Quando a oferta é criada com sucesso:

- O Pokémon é **removido do seu time** na hora e fica guardado pelo sistema enquanto a oferta estiver ativa.
- Você vê: "Oferta de \<nome do Pokémon\> por ₵\<preço\> enviada para \<jogador\>!"
- O jogador escolhido recebe: "\<você\> enviou uma oferta de \<nome do Pokémon\> por ₵\<preço\>! Use /trade offers para ver."

A oferta fica pendente até o comprador decidir. Você pode cancelá-la a qualquer momento pelo menu de ofertas enviadas (comando `/trade myoffers`), e o Pokémon volta para você.

## Para onde o Pokémon vai ao ser vendido

Quando o comprador aceita a oferta, o Pokémon vai para o **time** dele se houver espaço. Se o time do comprador estiver cheio, o Pokémon vai automaticamente para o **PC** (o armazenamento de Pokémon) dele. Assim a venda nunca falha por falta de espaço no time.
