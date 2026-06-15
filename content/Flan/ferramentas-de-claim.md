# Ferramentas de Claim — Enxada Dourada e Graveto

## As Duas Ferramentas

O sistema de claims usa dois itens especiais. Você não precisa fabricar ou ter esses itens no inventário de forma permanente — eles funcionam como ferramentas de interação com o sistema de proteção.

---

## Enxada Dourada — Ferramenta de Criação

A **Enxada Dourada** é usada para criar, visualizar e gerenciar claims.

### O que ela faz quando segurada:
- Exibe as bordas dos claims próximos (em um raio de 24 blocos) com partículas visuais
- Permite selecionar área para criar um novo claim

### Como usar para criar um claim:
1. Segure a Enxada Dourada na mão
2. **Clique com botão direito** em um bloco — esse será o **primeiro canto** da sua área
3. Vá até o canto oposto da área que quer proteger
4. **Clique com botão direito** no segundo bloco — o claim é criado automaticamente

> Você verá uma mensagem confirmando a criação do claim e quantos blocos de claim foram usados.

### Restrições:
- A área mínima é de **100 blocos** (ex: 10×10)
- Você precisa ter blocos de claim suficientes para cobrir a área
- O claim não pode sobrepor outro claim existente

---

## Graveto — Ferramenta de Inspeção

O **Graveto** é usado para verificar quem é dono de qualquer área do mapa.

### Como usar:
1. Segure o Graveto na mão
2. **Clique com botão direito** em qualquer bloco

### O que aparece:
- Se o bloco está dentro de um claim: nome do dono e informações básicas do claim
- Se o bloco não está protegido: mensagem informando que ninguém é dono daquele local

Essa ferramenta é útil para verificar se uma área está livre antes de construir, ou para saber com quem falar caso queira permissão para entrar em algum lugar.

---

## Visualização das Bordas

Quando você segura qualquer uma das duas ferramentas, as bordas dos claims próximos (dentro de 24 blocos) ficam visíveis por **30 segundos**. Após esse tempo, somem — mas voltam a aparecer se você interagir novamente ou se mover enquanto segura a ferramenta.

As bordas são exibidas com partículas coloridas. Claims normais e subclaims podem ter cores diferentes para diferenciá-los.

---

## Modo de Criação 3D

Se você estiver no **modo 3D** (ativado com `/flan switchMode default.3d`), a Enxada Dourada funciona de forma diferente:

1. Clique no primeiro bloco (define um canto em X, Y, Z)
2. Clique no segundo bloco em posição oposta (define o outro canto em X, Y, Z)
3. O claim cobre toda a caixa tridimensional entre os dois pontos

No modo 3D, você controla exatamente a altura mínima e máxima do claim, em vez de usar a profundidade padrão de 10 blocos.
