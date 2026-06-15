# Sistema de Captura da Safari Zone

## Como funciona a captura no Safari

Na Safari Zone, não há batalhas. Quando você encontra um Pokémon, pode usar três tipos de ação:
1. **Arremessar uma Safari Ball** — tenta capturar diretamente.
2. **Usar Bait** — aumenta a disposição do Pokémon, tornando a captura mais fácil mas reduzindo a chance de fuga.
3. **Usar Mud Ball** — irrita o Pokémon, aumentando muito a chance de captura, mas também aumenta a chance de fuga.

Você recebe **16 Safari Balls**, **32 Bait** e **32 Mud Balls** por dia ao entrar na Safari Zone.

---

## Sistema de Humor (Mood)

Cada Pokémon na Safari tem um valor de humor que vai de **-6 (irritado)** até **+6 (satisfeito)**.

- **Bait**: aumenta o humor em +1 (deixa mais satisfeito).
- **Mud Ball**: diminui o humor em -1 (deixa mais irritado).

O humor afeta diretamente a **taxa de captura** e a **taxa de fuga**:

### Efeito do Humor na Taxa de Captura

| Humor | Multiplicador da Captura |
|-------|--------------------------|
| -6 (irritado) | 3,0x (3x mais fácil) |
| -3 | 2,0x |
| 0 (neutro) | 1,0x (normal) |
| +3 | 0,5x (mais difícil) |
| +6 (satisfeito) | ~0,33x (3x mais difícil) |

Fórmula simplificada:
- Humor negativo (irritado): captura = `(3 + |humor|) / 3`
- Humor positivo (satisfeito): captura = `3 / (3 + humor)`

**Estratégia**: Usar Mud Ball deixa o Pokémon irritado e aumenta a captura. É a melhor estratégia para Pokémon difíceis, desde que você consiga capturar antes de ele fugir.

---

## Sistema de Fuga

O Pokémon pode fugir ao final de cada turno se você não capturou. A **taxa de fuga base** é 60 (em uma escala de 0–254).

- Humor negativo (irritado): aumenta a taxa de fuga proporcionalmente.
- Humor positivo (satisfeito): diminui a taxa de fuga.
- Após a Safari Ball quebrar, existe uma **janela de 5 segundos (100 ticks)** durante a qual o Pokémon não foge — essa janela de graça permite que você aja antes de ele escapar.

Quando um Pokémon foge, ele some com um efeito visual de desvanecimento e fica marcado como "não-capturável".

---

## Pokémon Shiny na Safari Zone

Pokémon shiny têm regras especiais neste servidor:
- **Taxa de captura**: 8x mais fácil do que um Pokémon normal.
- **Fuga**: **Shinies não fogem** — você pode tentar quantas vezes quiser sem risco de perder o Pokémon.

Isso significa que, ao encontrar um shiny, o único risco é ficar sem Safari Balls.

---

## Dicas de Captura

- Use **Mud Ball** repetidamente para maximizar a taxa de captura — mas lembre que o risco de fuga também sobe com o humor muito negativo.
- Use **Bait** se quiser reduzir o risco de fuga mas está disposto a ter uma chance de captura menor.
- **Shinies são imunes a fuga** — use todas as Mud Balls que precisar sem medo.
- Se acabar as Safari Balls, você ainda pode usar Bait/Mud Balls mas não consegue tentar capturar.
- Donuts com Capture Power aumentam a taxa de captura (veja a wiki de Donuts para mais detalhes).
