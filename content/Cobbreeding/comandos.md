# Comandos do Cobbreeding

O Cobbreeding adiciona um comando ao jogo, disponível para administradores e operadores do servidor.

## /givepokemonegg

**Descrição:** Dá um ovo de Pokémon diretamente para um jogador, com as propriedades especificadas.

**Permissão necessária:** Nível de permissão de cheat commands (operador do servidor / OP).

**Sintaxe:**
```
/givepokemonegg <jogador> <propriedades>
```

**Parâmetros:**
- `<jogador>` — Nome ou seletor do jogador que receberá o ovo.
- `<propriedades>` — Propriedades do Pokémon no formato do Cobblemon (mesma sintaxe do `/givepokemon`). A espécie é obrigatória; outros valores como forma, IVs e natureza são opcionais.

**Exemplos:**
```
/givepokemonegg Steve pikachu
/givepokemonegg @p eevee shiny=true
/givepokemonegg Jogador123 charmander ivs=31,31,31,31,31,31
```

**Comportamento:**
- O ovo gerado terá o timer de chocagem calculado normalmente com base nos ciclos de ovo da espécie.
- Se a espécie não for reconhecida, o comando falha silenciosamente e o jogador recebe uma mensagem de erro.
- O ovo vai diretamente para o inventário do jogador especificado.
