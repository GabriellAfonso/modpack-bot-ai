# Terastalização

## O que é a Terastalização

Terastalização faz o seu Pokémon ganhar uma "coroa" de cristal e mudar para o seu **Tera Tipo**, deixando os golpes daquele tipo mais fortes. Para usar, basta ter uma **Tera Orb** equipada no seu personagem — diferente dos outros gimmicks, o Pokémon não precisa segurar nenhum item para terastalizar.

## A Tera Orb (dispositivo de ativação)

- **O que é**: o dispositivo que libera a Terastalização nas suas batalhas.
- **Como obter**: fabricada numa bancada com o formato — fileira de cima: Amethyst Shard, Ender Pearl, Amethyst Shard; fileira do meio: Glowstone Dust, Diamante, Glowstone Dust; fileira de baixo: Amethyst Shard, Blaze Powder, Amethyst Shard.
- **Como usar**: segure a Tera Orb na mão e clique com o botão direito para colocá-la no "slot Tera" de acessório. Com ela equipada, o botão de Terastalização aparece nas batalhas.

### Carga da Tera Orb

A Tera Orb tem uma carga que se gasta ao usar e precisa recarregar antes do próximo uso (ela fica indisponível enquanto estiver descarregada). Se você tiver um **Terapagos** no time, a Tera Orb é recarregada automaticamente na hora, sem espera.

## Os Tera Shards (mudar o Tera Tipo)

O Tera Tipo de um Pokémon normalmente é igual ao tipo natural dele, mas você pode **mudar** esse Tera Tipo usando Tera Shards.

- **O que são**: fragmentos de cristal de cada tipo (Bug, Dark, Dragon, Electric, Fairy, Fighting, Fire, Flying, Ghost, Grass, Ground, Ice, Normal, Poison, Psychic, Rock, Steel, Water) e também o raro **Stellar Tera Shard**.
- **Como obter**: derrotando/coletando recompensas de Pokémon selvagens. Cada Pokémon derrotado tem uma chance de soltar o Tera Shard correspondente ao tipo primário dele (10% por padrão), ou uma chance menor de soltar um Stellar Tera Shard (1% por padrão).
- **Como usar**: junte uma pilha de Tera Shards do mesmo tipo e clique com eles num Pokémon seu. São necessários **50 shards** (valor padrão) para mudar o Tera Tipo. Mudar para o tipo Stellar concede uma conquista especial.

Observação: Ogerpon e Terapagos têm Tera Tipo fixo e **não podem** ter o Tera Tipo trocado por Tera Shards. Se você tentar usar um shard do tipo que o Pokémon já tem, nada acontece (mensagem "Your pokemon already has this tera type").

## A Tera Pouch (guardar os shards)

- **O que é**: uma bolsa para organizar e guardar seus Tera Shards. Existe em várias cores (a versão base é a Tera Pouch marrom).
- **Como obter**: fabricada com Couro e Blaze Powder (a versão marrom: Blaze Powder cercado por Couro).
- **Como usar**: abre um inventário próprio para armazenar os Tera Shards.

## A Liko's Pendant (obter um Terapagos)

- **O que é**: um pingente especial que, depois de um tempo equipado, traz um Terapagos para você.
- **Como obter**: fabricado com dois Strings e um Dormant Crystal (formato: String, espaço, String na linha de cima; Dormant Crystal no centro).
- **Como usar**: segure o pingente e clique com o botão direito para equipá-lo no slot Tera. Ele mostra um cronômetro regressivo no item. Quando o tempo acaba (cerca de 1 hora por padrão), o pingente é consumido e **invoca um Terapagos com Tera Tipo Stellar** ao seu lado (com chance de ser shiny). A duração é ajustável pela configuração `likoPendentDuration`.

## Efeitos visuais (Tera Hats)

Quando um Pokémon terastaliza, ele ganha o "chapéu" de cristal visual. Esse efeito pode ser ligado/desligado pela configuração `teraHats` (ligado por padrão). Existe também um efeito visual antigo, controlado pela opção `legacyTeraEffect` (desligado por padrão).

## Como terastalizar na batalha

1. Tenha uma Tera Orb (ou Omni Ring) equipada e carregada.
2. Na batalha, ative a Terastalização antes de escolher o golpe.

## Configurações relacionadas

- `teraShardRequired` (padrão 50): quantos Tera Shards são necessários para mudar o Tera Tipo.
- `teraShardDropRate` (padrão 10.0): chance, em porcentagem, de um Pokémon soltar o Tera Shard do tipo dele.
- `stellarShardDropRate` (padrão 1.0): chance, em porcentagem, de soltar um Stellar Tera Shard.
- `teraHats` (padrão ligado): mostra a coroa de cristal ao terastalizar.
- `legacyTeraEffect` (padrão desligado): usa o efeito visual antigo de terastalização.
- `likoPendentDuration` (padrão ~1 hora): tempo até a Liko's Pendant invocar o Terapagos.
