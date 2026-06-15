# Templo de Snowpoint, os Regis e a Chave Titã

## O que é o Templo de Snowpoint

O Templo de Snowpoint é uma estrutura do mod Legendary Monuments que abriga os Pokémon "Regi" (os golens lendários). O templo é dividido em salas trancadas; cada sala guarda um Regi e só pode ser aberta com a chave correta. Para localizar o templo pelo Arc Phone, você precisa ter **Sucata de Golem** (Golem Scrap). Dentro, você fabrica chaves a partir dos metais de golem, abre as salas, ativa as estátuas Regi para invocar cada golem e recebe Tábuas (Tablets) que, juntas, abrem a sala do Regigigas.

## Os metais de golem e as chaves

A matéria-prima de tudo é a **Sucata de Golem** (Golem Scrap), obtida fundindo (forno ou fornalha de explosão) o minério **Entulho Antigo** (Ancient Rubble Ore), que se gera no subsolo do mundo normal.

Com a Sucata de Golem você fabrica cinco metais de golem, cada um combinando 4 Sucatas de Golem + 1 gema elemental do Cobblemon (receita sem formato fixo, rende 4 lingotes):

- **Lingote de Golem de Aço** (Steel Golem Ingot): 4 Sucata + Gema de Aço (`cobblemon:steel_gem`).
- **Lingote de Golem de Rocha** (Rock Golem Ingot): 4 Sucata + Gema de Rocha (`cobblemon:rock_gem`).
- **Lingote de Golem de Gelo** (Ice Golem Ingot): 4 Sucata + Gema de Gelo (`cobblemon:ice_gem`).
- **Lingote de Golem Elétrico** (Electric Golem Ingot): 4 Sucata + Gema Elétrica (`cobblemon:electric_gem`).
- **Lingote de Golem de Dragão** (Dragon Golem Ingot): 4 Sucata + Gema de Dragão (`cobblemon:dragon_gem`).

Cada metal vira 1 bloco com 9 lingotes (e volta a 9 lingotes ao desfazer). Com cada metal você fabrica a chave correspondente, usando o formato:
```
N B .
B B .
. . B
```
onde N = a gema elemental daquele tipo e B = o lingote de golem daquele tipo. As chaves são:

- **Chave de Golem de Aço** (Steel Golem Key): abre a sala do **Registeel**.
- **Chave de Golem de Rocha** (Rock Golem Key): abre a sala do **Regirock**.
- **Chave de Golem de Gelo** (Ice Golem Key): abre a sala do **Regice**.
- **Chave de Golem Elétrico** (Electric Golem Key) e **Chave de Golem de Dragão** (Dragon Golem Key): abrem a sala do **Regieleki/Regidrago**.

## Estátuas Regi: invocar os golens e ganhar Tábuas

Dentro de cada sala há uma **Estátua Regi** (Regi Statue). Ao interagir com a estátua, abre-se uma tela para escolher qual Regi despertar. Escolhendo o tipo certo, a estátua é ativada: o Regi (nível 70) desperta acima dela com 2% de chance de Shiny, a estátua se desfaz e você recebe a **Tábua** (Tablet) daquele Regi:

- Despertar **Regirock** dá a **Tábua de Regirock** (Regirock Tablet).
- Despertar **Registeel** dá a **Tábua de Registeel** (Registeel Tablet).
- Despertar **Regice** dá a **Tábua de Regice** (Regice Tablet).
- Despertar **Regieleki** dá a **Tábua de Regieleki** (Regieleki Tablet).
- Despertar **Regidrago** dá a **Tábua de Regidrago** (Regidrago Tablet).

As salas dos Regis também têm baús com recompensas temáticas do Cobblemon (pedras, gemas, doces de experiência, itens de tipo, fragmentos Tera etc.).

## Chave Titã e a sala do Regigigas

A **Chave Titã** (Titan Key) abre a sala do **Regigigas**. Ela é fabricada reunindo as cinco Tábuas dos Regis, no formato:
```
A B .
C D .
. . E
```
onde A = Tábua de Registeel, B = Tábua de Regirock, C = Tábua de Regice, D = Tábua de Regieleki, E = Tábua de Regidrago.

Ou seja, para fazer a Chave Titã você precisa antes despertar os cinco Regis e juntar as cinco tábuas. Com a Chave Titã aberta a sala do Regigigas, você ativa a Estátua do Regigigas, que invoca **Regigigas** (nível 70) e te dá o **Núcleo Titã** (Titan Core) — um item extremamente poderoso usado para unir as ombreiras e fabricar o Martelo Titã.

## Resumo da cadeia do Templo de Snowpoint

1. Mine **Entulho Antigo** e funda em **Sucata de Golem**.
2. Use a Sucata de Golem no Arc Phone para localizar o **Templo de Snowpoint**.
3. Fabrique os metais e as **chaves de golem**; abra as salas dos Regis.
4. Ative as **Estátuas Regi** para invocar cada Regi e ganhar as cinco **Tábuas**.
5. Junte as cinco Tábuas para fazer a **Chave Titã**; abra a sala do **Regigigas**.
6. Ative a estátua do Regigigas para invocá-lo e ganhar o **Núcleo Titã**.
7. Use o Núcleo Titã para fabricar o **Martelo Titã** e a **Ombreira Titã** (veja o arquivo de Ombreiras).
