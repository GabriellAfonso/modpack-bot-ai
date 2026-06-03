# Dinamax e Gigantamax

## O que é o Dinamax

Dinamax faz o seu Pokémon crescer enorme e ficar muito mais forte por alguns turnos da batalha. Para usar você precisa de uma **Dynamax Band** equipada **e** estar perto de um bloco **Power Spot**. O Pokémon aumenta de tamanho (por um fator de escala configurável, 4x por padrão) durante a transformação.

## A Dynamax Band (dispositivo de ativação)

- **O que é**: o dispositivo que libera o Dinamax nas suas batalhas.
- **Como obter**: fabricada numa bancada com o formato — fileira de cima: três Pink Apricorns; fileira do meio: Ferro, Wishing Star, Ferro; fileira de baixo: três Blue Apricorns.
- **Como usar**: segure a Dynamax Band na mão e clique com o botão direito para colocá-la no "slot Dynamax" de acessório. Com ela equipada e estando perto de um Power Spot, o botão de Dinamax aparece nas batalhas.

## O Power Spot (área onde o Dinamax funciona)

- **O que é**: um bloco que cria uma zona de energia. O Dinamax só pode ser ativado se você estiver dentro do alcance de um Power Spot (20 blocos por padrão).
- **Como obter**: fabricado numa bancada com Redstone nos cantos/laterais, um Max Mushroom em cima, uma Wishing Star no centro e Stone na fileira de baixo (formato: Redstone, Max Mushroom, Redstone / Redstone, Wishing Star, Redstone / Stone, Stone, Stone).
- **Como usar**: coloque o Power Spot no mundo e batalhe perto dele para poder usar o Dinamax. O alcance é configurável (`powerSpotRange`).

Se você ativar a opção `dynamaxAnywhere`, o Dinamax passa a funcionar em qualquer lugar, sem precisar de Power Spot.

## A Wishing Star

- **O que é**: um material-chave usado para fabricar a Dynamax Band e o Power Spot.
- **Como obter**: encontrada no mundo quebrando o bloco **Wishing Star Crystal** e explorando a estrutura **Wishing Weald**.
- **Como usar**: ingrediente das receitas de Dynamax Band, Power Spot e Omni Ring.

## O Max Mushroom

- **O que é**: um cogumelo gigante que cresce no mundo, usado em várias receitas do sistema Dinamax.
- **Como obter**: encontrado/cultivado no mundo. Ele cresce sozinho em estágios (de pequeno até totalmente crescido), como uma plantação. Você o colhe quebrando o bloco.
- **Como usar**: ingrediente do Dynamax Candy, do Power Spot e dos caldos Max Soup / Sweet Max Soup.

## O Dynamax Candy (subir o Nível de Dinamax)

- **O que é**: um doce que aumenta o **Nível de Dinamax** de um Pokémon. Quanto maior o nível, mais HP o Pokémon ganha ao dinamaxar. O nível vai de 0 até 10.
- **Como obter**: fabricado com um Max Mushroom no centro cercado por quatro Exp. Candy S (formato de cruz).
- **Como usar**: clique com o doce num Pokémon seu para subir o Nível de Dinamax em 1. Ao chegar no nível 10, aparece a mensagem de nível máximo e uma conquista. Pokémon que não podem dinamaxar não aceitam o doce.

## O que é o Gigantamax

Gigantamax (G-Max) é uma versão especial do Dinamax, com aparência única e um golpe G-Max exclusivo, disponível só para certas espécies que têm o "fator Gigantamax". Você precisa ativar esse fator no Pokémon antes de poder Gigantamaxar.

### Max Soup (ativar o fator Gigantamax)

- **O que é**: um caldo que liga ou desliga o fator Gigantamax de um Pokémon.
- **Como obter**: fabricado com três Max Mushrooms em cima de uma Bowl (tigela).
- **Como usar**: clique com o caldo num Pokémon capaz de Gigantamaxar. Se o fator estava desligado, ele liga (mensagem "Your pokemon can gmax now"); se estava ligado, desliga (mensagem "Your pokemon can no longer gmax"). O caldo é consumido e devolve a tigela vazia. Não funciona em Urshifu.

### Sweet Max Soup (exclusivo do Urshifu)

- **O que é**: a versão do caldo feita especialmente para o Urshifu, que ativa/desativa o fator Gigantamax dele.
- **Como obter**: fabricado com Max Honey em cima, três Max Mushrooms no meio e uma Bowl embaixo.
- **Como usar**: clique no seu Urshifu para ligar ou desligar o fator Gigantamax dele.

### Max Honey

- **O que é**: ingrediente usado na receita do Sweet Max Soup.
- **Como obter**: coletado no mundo (associado a colmeias/abelhas e aos Max Mushrooms).

## Como dinamaxar na batalha

1. Tenha uma Dynamax Band (ou Omni Ring) equipada.
2. Esteja perto de um Power Spot (ou ative `dynamaxAnywhere`).
3. Na batalha, ative o Dinamax antes de escolher o golpe. Se o Pokémon tiver o fator Gigantamax ligado e for de espécie compatível, ele Gigantamaxa.

## Configurações relacionadas

- `dynamax` (padrão ligado): liga/desliga todo o sistema de Dinamax.
- `powerSpotRange` (padrão 20): alcance, em blocos, do Power Spot.
- `dynamaxAnywhere` (padrão desligado): permite dinamaxar sem Power Spot.
- `dynamaxScaleFactor` (padrão 4.0): o quanto o Pokémon cresce ao dinamaxar.

## Reverter formas travadas

Se um Pokémon ficar preso em forma Dinamax ou Gigantamax, o comando `/msd hard_reset` reverte todos os seus Pokémon de volta ao tamanho e à forma normais.
