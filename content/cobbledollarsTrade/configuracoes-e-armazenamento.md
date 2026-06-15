# Configurações e Armazenamento do CobleTrade

## Opções de configuração disponíveis

O mod CobleTrade **não possui opções de configuração ajustáveis** para o jogador nem para o administrador do servidor. Não há arquivo de configuração com valores para editar, nem limites de preço, taxas, prazos de expiração de ofertas ou quantidade máxima de ofertas. O comportamento é sempre o mesmo descrito nas outras páginas desta wiki:

- Preços e valores são sempre números inteiros de pelo menos 1 CobbleDollar (₵).
- Ofertas de venda não expiram sozinhas; ficam ativas até serem aceitas, recusadas ou canceladas.
- Vender um Pokém exige ter pelo menos 2 Pokémon no time.
- Não há cobrança de taxa: o comprador paga exatamente o preço definido e o vendedor recebe o valor cheio.

## Onde os dados das ofertas ficam salvos

As ofertas e devoluções pendentes são salvas no servidor, na pasta `config/cobletrade/`, em dois arquivos:

- `offers.json` — guarda todas as ofertas de venda ativas (de Pokémon e de itens) com seus vendedores, compradores e preços.
- `pending_items.json` — guarda os itens que precisam ser devolvidos a vendedores que estavam offline quando uma oferta foi recusada.

Esses arquivos são gerenciados automaticamente pelo mod. Como as ofertas ficam salvas em disco, elas **sobrevivem a reinicializações do servidor**: uma oferta criada hoje continuará lá depois de o servidor reiniciar, até alguém respondê-la.

## Mensagens e idioma

As mensagens do CobleTrade (avisos de venda, compra, recusa e cancelamento) são exibidas em **português** dentro do jogo. O símbolo de moeda usado em todas as mensagens é o ₵, representando os CobbleDollars do servidor.
