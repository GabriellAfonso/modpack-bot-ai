# Pokédex e Escaneamento

---

## Pokédex

A Pokédex registra automaticamente cada Pokémon que você encontra ou captura. É um item obtido no início do jogo.

### Estados de Registro
- **Desconhecido** — nunca viu.
- **Encontrado** — viu mas não capturou.
- **Capturado** — tem ou já teve um exemplar.

### O que a Pokédex Mostra
Para Pokémon encontrados/capturados:
- Número da Pokédex e nome.
- Tipo(s).
- Descrição de habitat.
- Altura e peso.
- Evoluções.
- Moveset disponível.
- Stats base.

Pokémon ainda não encontrados ficam com nome e modelo ocultos (mostram "???" até você vê-los).

### Configuração do Servidor
- **Pokémon não implementados** ficam visíveis na Pokédex (não são escondidos).
- Nomes de Pokémon desconhecidos não são exibidos fora do menu próprio.

---

## Escaneamento com a Pokédex

A Pokédex pode ser usada como **scanner** para escanear Pokémon selvagens próximos e obter informações sem batalhar.

- **Alcance de escaneamento:** até **15 blocos** de distância.
- Aponte a Pokédex para um Pokémon e use o escaneamento.
- Registra o Pokémon como "Encontrado" e revela suas informações básicas.

---

## HUD de Informação (Jade)

O servidor tem o mod Jade integrado ao Cobblemon que mostra um tooltip ao olhar para Pokémon selvagens. Dependendo do seu conhecimento sobre o Pokémon, exibe:

| Info | Quando aparece |
|------|---------------|
| Status (capturado/encontrado) | Sempre |
| Nome da espécie | Sempre que encontrado |
| Nickname | Se tiver apelido |
| Gênero | Quando encontrado |
| Nível | Sempre |
| HP (barra) | Sempre |
| Tipo(s) | Quando encontrado |
| Treinador dono | Pokémon de jogador |
| Natureza, habilidade, IVs, EVs | Somente se capturado (agachado) |
| Rendimento de EV | Quando encontrado |
