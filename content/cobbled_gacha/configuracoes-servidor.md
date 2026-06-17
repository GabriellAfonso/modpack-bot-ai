# Configurações do Servidor — server_config.json

O comportamento das máquinas gacha é controlado pelo arquivo `data/cobbledgacha/config/server_config.json`. Este guia lista todas as opções disponíveis, seus valores padrão e o que cada uma faz.

---

## Localização do arquivo

```
data/cobbledgacha/config/server_config.json
```

O arquivo é recarregado automaticamente pelo servidor quando datapacks são recarregados (comando `/reload`).

---

## Opções globais

### `pickup`
- **Tipo:** boolean (true/false)
- **Padrão:** `false`
- **Efeito:** Se `true`, as cápsulas e recompensas das máquinas vão diretamente para o inventário do jogador em vez de cair no chão. Se o inventário estiver cheio, os itens que não couberem ainda caem no chão.

```json
"pickup": false
```

### `automation`
- **Tipo:** boolean (true/false)
- **Padrão:** `false`
- **Efeito:** Se `true`, hoppers podem inserir moedas nas máquinas automaticamente (no slot de entrada). Máquinas do tipo spawner não podem ser automatizadas mesmo com essa opção ativa.

```json
"automation": false
```

---

## Custo de moedas por máquina

Define quantas moedas são necessárias para cada máquina girar. Use o ID da máquina como chave.

- **Padrão (se não configurado):** 5

```json
"gacha_machine_1": 5,
"gacha_machine_2": 20,
"gacha_machine_3": 10,
"gacha_machine_4": 1,
"gacha_machine_11": 1,
"gacha_machine_12": 3
```

IDs das máquinas:
- `gacha_machine` → use `gacha_machine_1` (mapeado internamente como índice 1)
- `gacha_machine_2` através `gacha_machine_12` → use o número correspondente

---

## `cooldowns`

Define o tempo de espera (em segundos) que um jogador precisa aguardar entre usos de cada máquina.

- **Padrão:** 0 (sem cooldown)

```json
"cooldowns": {
  "gacha_machine_1": 300,
  "gacha_machine_2": 600,
  "gacha_machine_11": 60
}
```

O valor é em **segundos**. `300` = 5 minutos, `3600` = 1 hora.

---

## `usesBeforeCooldown`

Define quantos giros completos um jogador pode fazer antes que o cooldown comece. Funciona junto com `cooldowns`.

- **Padrão:** 1 (cooldown começa após o 1º giro)

```json
"usesBeforeCooldown": {
  "gacha_machine_1": 3,
  "gacha_machine_2": 1
}
```

**Exemplo prático:** `usesBeforeCooldown: 3` e `cooldown: 300` → o jogador pode usar a máquina 3 vezes seguidas, e só então precisa esperar 300 segundos.

---

## `types`

Define o tipo de comportamento de cada máquina. Substitui a configuração `special` (mais antiga).

- **Padrão:** `"generic"` (para a maioria das máquinas)

Valores aceitos:
- `"generic"` ou `"normal"` — máquina padrão, dispensa cápsulas
- `"specific"` ou `"contiguous"` — trava o tipo de moeda no primeiro uso, tabela de loot varia por moeda
- `"spawner"` ou `"special"` — spawna um Pokémon em vez de dispensar cápsulas, não pode ser automatizada

```json
"types": {
  "gacha_machine_4": "spawner",
  "gacha_machine_12": "specific"
}
```

---

## `special` (obsoleto)

Forma mais antiga de marcar uma máquina como spawner. Ainda funciona mas é recomendado usar `types`.

```json
"special": {
  "gacha_machine_4": true
}
```

---

## `buckets`

Define os pesos de probabilidade globais para os buckets de raridade usados nos spawn pools (máquinas spawner e Gacha Balls).

- **Padrão:** common=100, uncommon=40, rare=15, ultra_rare=5, legendary=1

```json
"buckets": {
  "common": 100,
  "uncommon": 40,
  "rare": 15,
  "ultra_rare": 5,
  "legendary": 1
}
```

Esses pesos são usados quando um pool de Pokémon não tem seu próprio arquivo `_buckets.json`.

---

## Exemplo completo do arquivo padrão

```json
{
  "pickup": false,
  "automation": false,
  "gacha_machine_4_type": "spawner",
  "gacha_machine_12_type": "specific",
  "gacha_machine_1": 5,
  "gacha_machine_2": 20,
  "gacha_machine_3": 10,
  "gacha_machine_4": 1,
  "gacha_machine_11": 1,
  "gacha_machine_12": 3,
  "buckets": {
    "common": 100,
    "uncommon": 40,
    "rare": 15,
    "ultra_rare": 5,
    "legendary": 1
  }
}
```

---

## Notas

- O arquivo é recarregado com `/reload` — não precisa reiniciar o servidor
- Máquinas não listadas nas seções de custo usam o padrão de 5 moedas
- Máquinas não listadas em cooldowns não têm cooldown
- Você pode usar o formato `"gacha_machine_N_type": "spawner"` diretamente na raiz do JSON como alternativa a `"types"` (suporte legado)
