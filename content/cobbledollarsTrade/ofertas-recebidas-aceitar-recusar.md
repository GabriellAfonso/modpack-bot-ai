# Ver e Responder Ofertas Recebidas

## O que são ofertas recebidas

Ofertas recebidas são propostas de venda que outros jogadores enviaram **para você**. Cada oferta é de um Pokémon ou de um item, por um preço em CobbleDollars (₵, a moeda do servidor). Você decide se quer **comprar** (aceitar) ou **recusar** cada uma. Enquanto você não responde, o conteúdo fica reservado com o vendedor e o dinheiro não sai do seu saldo.

## Como abrir a lista de ofertas recebidas

Use o comando no chat:

```
/trade offers
```

Isso abre um menu (uma tela de baú grande) com o título "Ofertas recebidas" e o número total entre parênteses. Cada oferta aparece como um ícone:

- Ofertas de **Pokémon** mostram o próprio Pokémon como ícone.
- Ofertas de **item** mostram o item à venda como ícone.

Passando o mouse sobre cada ícone você vê o nome do conteúdo, quem é o vendedor ("De: \<vendedor\>") e o preço ("Preço: ₵\<valor\>"). Se você não tiver nenhuma oferta, o menu mostra "Nenhuma oferta aqui."

## Como abrir os detalhes de uma oferta

Dentro da lista, **clique** no ícone da oferta que você quer analisar. Isso abre uma tela de detalhe com o título "Oferta de \<vendedor\>", mostrando no centro o Pokémon ou item, o preço e quem está vendendo. Nessa tela aparecem dois botões:

- Um botão verde **Aceitar — ₵\<preço\>** à esquerda.
- Um botão vermelho **Recusar** à direita.

## Como aceitar (comprar) uma oferta

Na tela de detalhe, clique no botão verde **Aceitar**. O que acontece:

- O preço é **debitado do seu saldo** de CobbleDollars.
- O mesmo valor vai para o **vendedor** (mesmo que ele esteja offline; nesse caso o dinheiro é guardado para ele).
- Você recebe o conteúdo:
  - Item: vai para o seu inventário (ou cai no chão ao seu lado se o inventário estiver cheio). Mensagem: "Você comprou \<conteúdo\> por ₵\<preço\>! Verifique seu inventário."
  - Pokémon: vai para o seu time, ou para o seu PC se o time estiver cheio. Mensagem: "Você comprou \<conteúdo\> por ₵\<preço\>! Verifique seu party ou PC."

Se você **não tiver dinheiro suficiente**, a compra é bloqueada com "Saldo insuficiente para comprar \<conteúdo\>." e nada é debitado. Se a oferta já tiver sido cancelada ou aceita por outra via, aparece "Essa oferta não está mais disponível."

## Como recusar uma oferta

Na tela de detalhe, clique no botão vermelho **Recusar**. O que acontece:

- A oferta é removida e o conteúdo **volta para o vendedor**.
  - Pokémon: devolvido ao time do vendedor (ou ao PC dele).
  - Item: devolvido ao inventário do vendedor se ele estiver online; se estiver offline, o item fica guardado e é entregue quando ele voltar a entrar.
- Você vê: "Você recusou a oferta de \<conteúdo\>."
- O vendedor (se online) é avisado de que você recusou e que o conteúdo foi devolvido.

Recusar **não custa nada** a você; nenhum dinheiro é movido.
