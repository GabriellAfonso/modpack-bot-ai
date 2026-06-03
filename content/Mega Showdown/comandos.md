# Comandos do Mega Showdown

Todos os comandos do mod começam com `/msd`. Alguns exigem permissão de operador (nível 4, ou seja, admin do servidor).

## /msd hard_reset

- **O que faz**: reverte **todos** os seus Pokémon (tanto os do time/party quanto os guardados no PC) de volta às formas normais. Isso desfaz Mega Evolução, Dinamax, Gigantamax e Terastalização que tenham ficado travadas, voltando o tamanho e a forma originais.
- **Quem pode usar**: qualquer jogador (não precisa ser operador).
- **Quando usar**: quando um Pokémon fica preso numa forma transformada por causa de algum erro, crash ou batalha interrompida.

## /msd reload

- **O que faz**: recarrega o arquivo de configuração do mod (`config/mega_showdown/config.json`) sem precisar reiniciar o jogo, aplicando as mudanças feitas no arquivo.
- **Quem pode usar**: apenas operadores (nível 4).

## /msd apply &lt;tipo&gt; &lt;resource_id&gt;

- **O que faz**: ferramenta de administrador/criador de datapack. Aplica um "componente" de dados ao item que você está segurando na mão, marcando-o como um item de um sistema específico (por exemplo, transformar um item num item de Mega, de fusão, de mudança de forma, etc.). É usado para criar/configurar itens customizados.
- **Quem pode usar**: apenas operadores (nível 4).
- **Tipos disponíveis** (primeiro argumento): `solo_fusion`, `du_fusion`, `mega`, `showdown_item`, `held_form_change`, `form_change_interact`, `form_change_toggle_interact`, `z_crystal_item`.
- **Como usar**: segure na mão o item que quer marcar, escolha o tipo e depois o identificador (resource_id) sugerido pelo autocompletar, que lista as opções registradas para aquele tipo.

## Observação para jogadores comuns

No dia a dia, o único comando que você vai realmente precisar é o `/msd hard_reset`, para destravar Pokébolas que ficaram numa forma especial. Os comandos `reload` e `apply` são voltados para administradores de servidor e criadores de conteúdo/datapacks.
