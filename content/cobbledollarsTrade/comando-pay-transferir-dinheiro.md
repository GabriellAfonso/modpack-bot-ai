# Transferir Dinheiro com /trade pay

## O que é o pagamento direto

O comando `/trade pay` permite enviar CobbleDollars (₵, a moeda do servidor) diretamente para outro jogador, sem precisar de itens, ofertas ou trocas. É a forma mais rápida de dar dinheiro a alguém, como pagar uma dívida, dividir lucros ou fazer uma doação.

## Como usar o comando de pagamento

Use o comando no chat com este formato:

```
/trade pay <jogador> <valor>
```

- `<jogador>` é o nome do jogador que vai receber o dinheiro. Ele precisa estar **online** no servidor.
- `<valor>` é a quantia em ₵ que você quer enviar. Precisa ser um número inteiro de pelo menos 1.

Exemplo: `/trade pay Ash 500` envia 500 ₵ para o jogador chamado Ash.

## O que acontece ao pagar

Quando o pagamento dá certo:

- O valor é **debitado** do seu saldo de CobbleDollars na hora.
- O mesmo valor é **creditado** no saldo do jogador que recebeu.
- Você vê a mensagem: "Você enviou ₵\<valor\> para \<jogador\>." (em verde).
- O jogador que recebeu vê: "Você recebeu ₵\<valor\> de \<você\>." (em verde).

A transferência é imediata e não precisa de confirmação do outro lado.

## Erros possíveis ao pagar

O pagamento é bloqueado e nada acontece nestes casos:

- **Pagar a si mesmo:** se você tentar enviar dinheiro para o seu próprio nome, aparece "Você não pode pagar a si mesmo."
- **Saldo insuficiente:** se você não tem ₵ suficiente para cobrir o valor, aparece "Saldo insuficiente." e nenhum dinheiro é movido.
- **Jogador offline ou inexistente:** o comando exige um jogador online; se o nome não corresponder a alguém conectado, o comando falha.
