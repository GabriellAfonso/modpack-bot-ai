# Ciclo e Reset de Cristais de Raid

## Limite de Vitórias

Cada Cristal de Raid tem um número máximo de vezes que pode ser vencido antes de ser desativado. Após atingir esse limite:
- O cristal entra em estado **inativo**.
- Jogadores que tentarem interagir verão a mensagem *"A toca de raid não está ativa no momento."*
- O cristal aguarda o tempo de reset para voltar a funcionar.

**Limite padrão por tier:** 3 vitórias para todos os tiers (configurável individualmente).

> Por padrão, **derrotas não contam** para o limite. Apenas vitórias decrementam o contador. Isso pode ser alterado com `max_clears_include_fails: true`.

---

## Reset Automático

Após ser desativado, o cristal reseta automaticamente em **2 horas** (padrão; configurável via `reset_time` em segundos). Ao resetar:
- O contador de vitórias volta a 0.
- O Pokémon-chefe e/ou o tipo podem mudar, dependendo do **Modo de Ciclo**.
- O cristal fica ativo novamente para novos jogadores.

Use `reset_time: -1` para desativar o reset automático — o cristal some permanentemente após atingir o limite.

---

## Modos de Ciclo

O **Modo de Ciclo** (`cycle_mode`) controla o que muda quando o cristal reseta. Pode ser configurado globalmente ou por cristal individualmente.

### `NONE`
- Chefe e tipo **nunca mudam**.
- Sempre o mesmo Pokémon, sempre o mesmo tipo visual.
- Ideal para cristais decorativos ou raids fixas.

### `LOCK_BOTH`
- Chefe e tipo travados no valor que tinham quando foram **criados ou gerados pela primeira vez**.
- Iguais ao `NONE` na prática para cristais naturais (surgem com valores fixos).

### `LOCK_TIER`
- O Pokémon-chefe é **fixo**, mas o **tipo visual** pode mudar entre resets.
- Bom para servidores que querem um chefe específico, mas com aparência variável.

### `LOCK_TYPE`
- O **tipo visual** é fixo, mas o **Pokémon-chefe** pode mudar entre resets.
- Bom para raids temáticas (ex: cristal sempre de Fogo, mas o Pokémon varia).

### `BUCKET`
- Usa uma **pool com pesos** para sortear o próximo chefe ao resetar.
- Permite criar grupos de chefes possíveis para determinado cristal.
- Configuração avançada feita pelo admin nos arquivos de boss.

### `ALL` (padrão)
- Tanto o **chefe** quanto o **tipo** são sorteados livremente a cada reset.
- Máxima variedade — cada reset pode trazer um Pokémon completamente diferente.

---

## Cristais Colocados por Admins

Quando um admin cria um cristal via comando `/crd dens`, ele pode especificar:
- Se o cristal **pode resetar** (`can_reset: true/false`).
- O **modo de ciclo** desejado para aquele cristal específico.

Cristais criados com `can_reset: false` são **permanentes** — nunca desativam e o chefe nunca muda, independentemente do limite de vitórias.

---

## Identificando o Estado do Cristal

Com o mod **Jade** ou **WTHIT** instalado, ao apontar para um Cristal de Raid você vê:
- Se está **ativo** ou **inativo**.
- O tier, tipo e feature do cristal.

Sem esses mods, você só descobre ao tentar interagir — se estiver inativo, uma mensagem aparece informando.
