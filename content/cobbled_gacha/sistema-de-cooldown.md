# Sistema de Cooldown das Máquinas Gacha

O Cobbled Gacha tem um sistema de cooldown que limita com que frequência um jogador pode usar cada máquina. O cooldown é **individual por jogador** — se você está em cooldown em uma máquina, outros jogadores ainda podem usá-la normalmente.

---

## Como funciona o cooldown

Depois que você completa um giro (insere todas as moedas e a máquina dispensa a recompensa), um timer de cooldown pode ser ativado. Enquanto o cooldown estiver ativo:

- Tentar inserir moeda na máquina mostra a mensagem: `"Hold on! You can use this machine again in Xs."` (onde X é o tempo restante em segundos)
- O cooldown é contado em tempo real de jogo — ele continua enquanto você estiver online
- O progresso do cooldown é salvo no servidor — deslogar e logar de volta não reseta o timer

---

## Usos antes do cooldown (usesBeforeCooldown)

O servidor pode configurar um número de usos "gratuitos" antes que o cooldown comece. Isso é controlado pela configuração `usesBeforeCooldown`.

**Exemplo:** Se `usesBeforeCooldown` for 3 e o cooldown for 300 segundos:
- 1º giro: livre
- 2º giro: livre
- 3º giro: livre
- 4º giro: cooldown de 300 segundos começa
- Após 300 segundos: o contador de usos gratuitos é reiniciado para 3

**Padrão:** `usesBeforeCooldown = 1` (sem usos gratuitos — cooldown começa após o 1º giro)

---

## Sem cooldown configurado

Se o servidor não configurar cooldown para uma máquina, ela não tem cooldown. O padrão do mod é **0 segundos** (sem cooldown) para todas as máquinas que não estejam listadas na configuração.

---

## Como o cooldown é armazenado

O cooldown de cada jogador em cada máquina é salvo como dados do mundo (world data). Isso significa:

- O cooldown persiste mesmo se o jogador trocar de servidor ou deslogar
- O cooldown não é vinculado ao bloco físico da máquina — é uma relação entre o jogador e o **tipo de máquina**
- Se o servidor remover a configuração de cooldown de uma máquina, cooldowns existentes ainda vão expirar normalmente

---

## Configuração do cooldown (para referência)

Os administradores do servidor controlam os cooldowns no arquivo `server_config.json`:

```json
{
  "cooldowns": {
    "gacha_machine_1": 300,
    "gacha_machine_2": 600
  },
  "usesBeforeCooldown": {
    "gacha_machine_1": 1,
    "gacha_machine_2": 3
  }
}
```

- O valor em `cooldowns` é em **segundos**
- O valor em `usesBeforeCooldown` é o número de giros completos antes do cooldown
- Máquinas não listadas não têm cooldown

---

## Perguntas frequentes

**Posso usar a máquina enquanto estou em cooldown?**
Não. Qualquer tentativa de inserir moeda durante o cooldown é bloqueada e mostra a mensagem de espera.

**O cooldown é por máquina ou por todos os gacha?**
Por tipo de máquina. Você pode estar em cooldown na Poké Gacha Machine mas usar o Cram O' Matic normalmente.

**E se eu usar a mesma máquina em locais diferentes do mundo?**
O cooldown se aplica ao tipo da máquina, não ao bloco específico. Usar o Cram O' Matic em qualquer lugar do mundo usa o mesmo cooldown.
