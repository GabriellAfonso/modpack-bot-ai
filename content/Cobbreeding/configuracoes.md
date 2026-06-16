# Configurações do Cobbreeding

As configurações do mod ficam no arquivo de configuração gerado automaticamente pelo servidor. Esta página lista todas as opções disponíveis com seus valores padrão e o efeito de cada uma.

---

## Configurações de Timing

### minBreedingTimeInTicks
- **Padrão:** `8000`
- **Efeito:** Tempo mínimo (em ticks) entre a ativação do breeding e a geração de um ovo. Com 20 ticks por segundo, 8000 ticks = ~6,7 minutos.
- **Mínimo permitido:** 20 ticks.

### maxBreedingTimeInTicks
- **Padrão:** `14000`
- **Efeito:** Tempo máximo (em ticks) entre ovos. O Pasto escolhe um valor aleatório entre o mínimo e o máximo a cada ovo gerado. 14000 ticks = ~11,7 minutos.
- **Deve ser maior ou igual** a `minBreedingTimeInTicks`.

### mirrorHerbTimeInTicks
- **Padrão:** `600`
- **Efeito:** Intervalo em ticks entre cada verificação de Mirror Herb no Pasto. Com 20 ticks/segundo, 600 ticks = 30 segundos.
- **Mínimo permitido:** 1 tick.

### eggHatchMultiplier
- **Padrão:** `1.0`
- **Efeito:** Multiplicador aplicado ao tempo de chocagem dos ovos. Valores menores que 1.0 fazem os ovos chocar mais rápido; valores maiores os tornam mais lentos. Exemplo: `0.5` faz os ovos chocar em metade do tempo normal.
- **Mínimo permitido:** 0.001.

---

## Configurações de Shiny Hunting

### shinyMethod
- **Padrão:** `{ "masuda": 4.0, "crystal": 1.0, "always": 1.0 }`
- **Efeito:** Define o multiplicador de cada método de shiny hunting. Os multiplicadores são aplicados à taxa base de shiny do Cobblemon. Valores iguais a 1.0 significam que o método está efetivamente inativo.
  - **masuda:** Aplicado quando os dois pais têm OTs diferentes.
  - **crystal:** Aplicado uma vez por pai shiny (duas vezes se ambos forem shiny).
  - **always:** Aplicado em todos os ovos, independentemente dos pais.
- Os multiplicadores são **multiplicativos**: se masuda (×4) e crystal (×2) se aplicam juntos, o resultado é ×8, não ×6.

---

## Configurações de Habilidade

### hiddenAbilitiesEnabled
- **Padrão:** `true`
- **Efeito:** Quando ativado, há uma pequena chance de o filho nascer com sua Hidden Ability mesmo que nenhum dos pais a tenha. Quando desativado, a HA só pode ser herdada se o pai transmissor já a possuir.

### forcedAbilitiesEnabled
- **Padrão:** `false`
- **Efeito:** Quando ativado, se o pai transmissor tiver uma habilidade "forçada" (que normalmente não existe para a espécie filha), essa habilidade é passada ao filho e marcada como forçada. Habilidades forçadas não mudam durante a evolução.

---

## Configurações de Ditto + Ditto

### dittoAndDittoRandomEgg
- **Padrão:** `false`
- **Efeito:** Quando ativado, dois Dittos no Pasto podem produzir ovos de espécies aleatórias. A espécie é revelada apenas quando o ovo choca.

### dittoAndDittoAllowLegendary
- **Padrão:** `false`
- **Efeito:** Permite que ovos de Ditto + Ditto contenham Pokémon Lendários e Míticos. Requer `dittoAndDittoRandomEgg = true`.

### dittoAndDittoAllowParadox
- **Padrão:** `false`
- **Efeito:** Permite que ovos de Ditto + Ditto contenham Pokémon Paradoxo. Requer `dittoAndDittoRandomEgg = true`.

### dittoAndDittoAllowUltraBeast
- **Padrão:** `false`
- **Efeito:** Permite que ovos de Ditto + Ditto contenham Ultra Beasts. Requer `dittoAndDittoRandomEgg = true`.

### dittoAndDittoAllowUndiscovered
- **Padrão:** `false`
- **Efeito:** Permite que ovos de Ditto + Ditto contenham Pokémon do Egg Group Undiscovered (que não sejam lendários, paradoxo ou ultra beasts). Requer `dittoAndDittoRandomEgg = true`.

---

## Configurações Visuais

### customColors
- **Padrão:** `false`
- **Efeito:** Quando ativado, os ovos gerados no Pasto e via comando terão aparência visual diferente conforme o tipo do Pokémon contido (ex: ovo de Pokémon Fogo tem cor avermelhada). Quando desativado, todos os ovos têm a aparência genérica padrão.

---

## Configurações de Pasto

### allowHoppersToPullFromPastureBlock
- **Padrão:** `true`
- **Efeito:** Permite que Hoppers conectados à base do Pasto retirem os ovos automaticamente. Desative se não quiser automação de coleta de ovos.

### maxNumberOfActivatedPasturePerPlayer
- **Padrão:** `-1` (ilimitado)
- **Efeito:** Número máximo de Pastos com breeding ativo por jogador ao mesmo tempo. Use `-1` para ilimitado. Se um jogador tentar ativar breeding em mais Pastos que o limite, receberá uma mensagem de erro.

### pastureInventorySize
- **Padrão:** `5`
- **Efeito:** Número de ovos que um único Pasto pode armazenar. Quando cheio, nenhum novo ovo é gerado até que os existentes sejam coletados.
- **Mínimo permitido:** 1.

---

## Configurações de Herança

### inheritedFeatures
- **Padrão:** `["bagworm_cloak", "color", "dance_style", "fish_stripes", "striped", "magikarp_jump", "mooshtank", "region_bias", "alolan", "galarian", "hisuian", "paldean", "bull_breed", "tatsugiri_texture", "whiscash_nero", "wooper_heart"]`
- **Efeito:** Lista de características que são transmitidas da mãe para o filho. Adicione ou remova entradas para controlar quais aspectos visuais e regionais são herdados.

---

## Configurações de Segurança

### eggEncryptionEnabled
- **Padrão:** `true`
- **Efeito:** Quando ativado, os dados do Pokémon dentro do ovo são criptografados — o jogador não consegue ver qual Pokémon está dentro antes de chocar. Quando desativado, o jogador pode clicar com o botão direito no ovo para revelar os dados. **Recomendado manter ativado em servidores multiplayer.**

---

## Compatibilidade

### cobblemonSizeVariationsCompatEnabled
- **Padrão:** `true`
- **Efeito:** Ativa a compatibilidade com o mod **Cobblemon Size Variations**, aplicando as variações de tamanho ao Pokémon quando o ovo choca. Desative se estiver tendo conflitos com esse mod.
