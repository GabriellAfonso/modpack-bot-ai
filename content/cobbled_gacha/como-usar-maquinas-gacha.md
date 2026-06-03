# Como Usar as Máquinas Gacha

As máquinas gacha do mod Cobbled Gacha — que muitos jogadores chamam de **cassino** (ou casino) — funcionam todas da mesma forma básica: você insere um item de moeda até atingir o custo total da máquina, e então ela dispensa a recompensa. Este guia explica o processo passo a passo.

---

## Passo a passo básico

1. **Identifique a moeda correta** para a máquina que você quer usar. Cada máquina aceita apenas um tipo de item. Se você inserir o item errado, aparece uma mensagem de erro no chat mostrando o que a máquina realmente aceita.

2. **Segure a moeda na mão principal** (mão direita por padrão).

3. **Clique com botão direito** na máquina. Cada clique insere **1 moeda** no progresso da máquina.

4. Uma mensagem aparece na tela (no action bar) mostrando o progresso atual, no formato `[X/Y]` — onde X é quantas moedas já foram inseridas e Y é o total necessário.

5. Quando X atinge Y (último custo), a máquina **gira automaticamente**:
   - Aparece a mensagem "Gotcha!" na tela
   - A máquina toca um som
   - A recompensa é dispensada na frente da máquina (na direção para onde ela está virada)
   - O progresso volta para zero

---

## Inserção em massa (bulk use)

Para inserir múltiplas moedas de uma vez sem precisar clicar várias vezes, use a **mão esquerda (off-hand)**:

- Segure a moeda na mão principal
- **Clique com o botão direito enquanto a moeda estiver na mão principal** — o mod detecta se você está usando a mão off-hand
- Na prática: para bulk, clique com a mão principal segurando o suficiente para completar o custo restante

**Comportamento do bulk:** Ao usar bulk, o mod tenta inserir moedas suficientes para completar o custo restante da máquina de uma só vez, consumindo do seu inventário. Isso é útil para máquinas com custo alto como o Cram O' Matic (20 apricorns).

---

## Onde a recompensa aparece

Por padrão, as cápsulas e itens de recompensa **caem no chão** na frente da máquina — no bloco para o qual ela está virada quando foi colocada.

Se o servidor tiver configurado `"pickup": true`, a recompensa vai diretamente para o seu inventário. Se o inventário estiver cheio, o item cai no chão mesmo assim.

---

## Mensagens da máquina

| Mensagem | Significado |
|---|---|
| `[X/Y]` | Progresso atual (X moedas inseridas de Y necessárias) |
| `Gotcha!` | A máquina girou com sucesso |
| `Invalid currency inserted. Needs: [item]` | O item que você tentou inserir não é aceito por essa máquina |
| `Hold on! You can use this machine again in Xs.` | A máquina está em cooldown, onde X é o tempo restante em segundos |
| `Looks like the machine malfunctioned and needs a fix!` | A tabela de loot da máquina está vazia ou mal configurada (dud) |
| `Score! An extra item dropped down! It's a [item].` | A tabela de loot gerou múltiplas recompensas |

---

## Tipo "Specific" (moeda travada)

Algumas máquinas são do tipo **specific** (como o Plush-O-Matic). Nestas máquinas:

- A primeira moeda inserida **trava** a máquina para aquele tipo específico de moeda
- Todas as moedas seguintes do mesmo giro precisam ser do mesmo tipo
- Tentar inserir um tipo diferente enquanto a máquina está travada gera a mensagem de moeda inválida
- Após a máquina girar, a trava é liberada automaticamente e qualquer yarn pode ser inserido no próximo giro

Isso significa que a recompensa pode variar conforme o tipo de moeda — a máquina consulta uma tabela de loot diferente para cada tipo.

---

## Máquinas do tipo Spawner

Máquinas configuradas como **spawner** (como a Strange Crystallized Machine) têm comportamento diferente:

- Ao completar o custo, **não dispensa cápsulas**
- Em vez disso, um **Pokémon aparece** perto do jogador
- O Pokémon fica solto no mundo — você pode batalhar e capturá-lo normalmente com Pokéballs
- O Pokémon é escolhido aleatoriamente de uma lista configurada pelo servidor para aquela máquina
- Máquinas spawner **não podem ser automatizadas** com hoppers

---

## Cooldown entre usos

Depois de girar a máquina, pode haver um período de espera (cooldown) antes de poder usá-la novamente. Esse cooldown é **individual por jogador** — um jogador em cooldown não bloqueia outros de usar a mesma máquina.

- O cooldown é configurado pelo servidor (em segundos)
- Alguns servidores configuram um número de usos antes do cooldown começar (ex: 3 usos livres antes de 5 minutos de espera)
- Se tentar usar a máquina durante o cooldown, aparece a mensagem `Hold on! You can use this machine again in Xs.`

Para detalhes sobre como o cooldown funciona, veja o arquivo **sistema-de-cooldown.md**.
