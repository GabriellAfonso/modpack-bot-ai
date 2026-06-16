# Shiny Hunting por Breeding — Método Masuda e Outros

O Cobbreeding oferece três métodos de aumento de chances de shiny ao chocar ovos. Cada método pode ter seu multiplicador ajustado pelo servidor. Os multiplicadores são **multiplicativos** entre si — se dois métodos se aplicam ao mesmo tempo, o efeito combinado é muito maior que a soma.

**Exemplo:** Método Masuda (×4) + Crystal (×4 pois ambos os pais são shiny) = ×16 no total, não ×8.

## Método Masuda

**Condição:** Os dois pais foram originalmente capturados ou criados por **treinadores diferentes** (OTs diferentes).

**Multiplicador padrão:** ×4 (a chance base de shiny é dividida por 4, ficando 4× mais fácil).

**Como usar:** Use Pokémon de jogadores diferentes no Pasto. Em um servidor, isso significa usar um Pokémon capturado/chocado por outro jogador como parceiro de breeding.

## Método Crystal

**Condição:** Um ou ambos os pais são **shiny**.

**Multiplicador padrão:** ×1 por padrão (inativo), configurável pelo servidor.

- Se um pai for shiny, o multiplicador é aplicado uma vez.
- Se ambos os pais forem shiny, o multiplicador é aplicado **duas vezes** (de forma multiplicativa).

**Observação:** O multiplicador padrão é ×1, o que significa que o método Crystal está efetivamente desativado até que o servidor o configure com um valor maior.

## Método Always

**Condição:** Sempre ativo, aplicado a todos os ovos independentemente dos pais.

**Multiplicador padrão:** ×1 (inativo por padrão).

Este método serve para que o servidor aplique um aumento global nas chances de shiny para todos os ovos chocados, independentemente dos pais.

## Como os multiplicadores interagem

Os três métodos são aplicados à **taxa base de shiny do servidor** (configurada no Cobblemon, não no Cobbreeding). Cada método ativo divide essa taxa pelo seu multiplicador:

```
chance_final = taxa_base / (masuda × crystal × always)
```

Por exemplo, com taxa base de 1/4096, Masuda ×4 e Crystal ×4 (1 pai shiny):
```
1/4096 / (4 × 4 × 1) = 1/4096 / 16 = 1/65536 → ainda raro, mas muito mais fácil
```

## Dicas práticas para shiny hunting

- **Método Masuda** é o mais fácil de ativar: basta usar um Pokémon de outro jogador como parceiro de breeding.
- Combine Masuda com um pai shiny (se tiver) para empilhar os multiplicadores.
- O Método Crystal com multiplicador alto recompensa quem já tem shinies e quer usar breeding para criar shinies específicos.
