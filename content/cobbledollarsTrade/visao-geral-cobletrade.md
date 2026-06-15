# Visão Geral do CobleTrade

## O que é o mod CobleTrade

O CobleTrade é um mod (addon) para servidores de Minecraft que adiciona um sistema de comércio direto entre jogadores usando a moeda **CobbleDollars** (símbolo ₵). Ele permite três coisas principais:

- **Transferir dinheiro** diretamente para outro jogador com um comando.
- **Vender Pokémon** do seu time para outro jogador por um preço em CobbleDollars.
- **Vender itens** do seu inventário para outro jogador por um preço em CobbleDollars.

Todas as vendas funcionam por **ofertas privadas**: você envia uma proposta para um jogador específico, e só aquele jogador pode aceitar ou recusar. Não é um mercado público ou leilão aberto; cada oferta tem um vendedor e um comprador definidos.

## Mods necessários para funcionar

O CobleTrade depende de outros mods instalados no servidor. Sem eles o mod não carrega:

- **CobbleDollars** (versão 2.0.0 ou superior): fornece a moeda ₵ usada em todas as transações.
- **Cobblemon** (versão 1.7.0 ou superior): fornece os Pokémon que podem ser vendidos.
- **Fabric Loader** (0.16.5 ou superior) e **Fabric API**, rodando em **Minecraft 1.21.1**.

## Como o dinheiro funciona no CobleTrade

Toda transação usa o saldo de CobbleDollars (₵) de cada jogador. Quando você paga, vende ou compra algo, o valor é debitado ou creditado automaticamente no seu saldo. Você não precisa carregar a moeda como item; é um valor numérico ligado à sua conta.

O preço de qualquer oferta ou pagamento é sempre um número inteiro de pelo menos 1 ₵. Não é possível enviar valores zero, negativos ou fracionados.

## Resumo dos comandos disponíveis

O CobleTrade tem um único comando base, `/trade`, com várias funções:

- `/trade pay <jogador> <valor>` — envia dinheiro direto para outro jogador.
- `/trade offer pokemon <slot> <preço> <jogador>` — oferece um Pokém do seu time para venda.
- `/trade offer item <quantidade> <preço> <jogador>` — oferece o item da sua mão para venda.
- `/trade offers` — abre o menu das ofertas que **você recebeu**.
- `/trade myoffers` — abre o menu das ofertas que **você enviou**.

Cada um desses sistemas é explicado em detalhe nas outras páginas da wiki.

## O que acontece quando alguém está offline

O CobleTrade foi feito para lidar com jogadores desconectados. Se você vende algo e o comprador aceita enquanto você está offline, o seu dinheiro é guardado e creditado mesmo assim. Se uma oferta sua de item é recusada enquanto você está offline, o item fica guardado e é entregue automaticamente quando você voltar a entrar no servidor. Pokémon recusados de vendedores offline vão direto para o PC do vendedor.
