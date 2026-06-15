# Subclaims — Divisão de Áreas Dentro do Seu Terreno

## O que é um Subclaim?

Um subclaim é uma área menor criada **dentro** de um claim seu. Ele serve para dar permissões diferentes a pessoas diferentes em partes específicas do seu terreno.

**Exemplo de uso:** Você tem uma grande base. Quer que um amigo possa usar só a fazenda, mas não entrar no seu cofre. Você cria um subclaim na fazenda e dá permissões de quebrar/colocar blocos só nela para esse amigo.

---

## Como Criar um Subclaim

### Passo 1 — Ativar o Modo de Subclaim

```
/flan switchMode subclaim
```

Você precisa estar neste modo para criar subclaims. Para voltar ao modo normal depois, use `/flan switchMode default`.

### Passo 2 — Selecionar a Área

Com o modo subclaim ativo e a **Enxada Dourada** na mão:

1. **Clique com botão direito** no primeiro canto da área dentro do seu claim
2. **Clique com botão direito** no segundo canto oposto

O subclaim é criado automaticamente. A área selecionada deve estar completamente dentro do claim principal.

### Via Comando

```
/flan add <x1,y1,z1> <x2,y2,z2>
```

(Com o modo subclaim ativo)

---

## Subclaims 3D

Para criar subclaims com altura definida manualmente:

```
/flan switchMode subclaim.3d
```

Depois selecione dois blocos em posições opostas (incluindo altura) com a Enxada Dourada. O subclaim cobrirá toda a caixa 3D entre os dois pontos.

---

## Gerenciar Permissões de um Subclaim

Subclaims têm seu próprio sistema de permissões, independente do claim principal. Para editar:

1. Entre no subclaim
2. Use `/flan menu` para abrir o menu de gerenciamento

No menu você pode:
- Editar permissões globais do subclaim
- Criar grupos com permissões específicas
- Adicionar jogadores a grupos

**Herança:** Por padrão, subclaims herdam os grupos padrão do claim pai. Isso significa que se um jogador for Co-Owner do claim principal, ele também terá acesso total ao subclaim — a menos que você configure diferente.

---

## Deletar um Subclaim

Para deletar o subclaim onde você está:

1. Ative o modo subclaim: `/flan switchMode subclaim`
2. Entre no subclaim que quer deletar
3. Use o comando:

```
/flan deleteSubClaim
```

Para deletar **todos os subclaims** de um claim de uma vez, entre no claim principal (fora dos subclaims) e use:

```
/flan deleteAllSubClaims
```

Esse comando pede confirmação. Confirme com `/flan confirm confirm` ou cancele com `/flan confirm deny`.

---

## Expandir um Subclaim

Com o modo subclaim ativo e dentro do subclaim, olhe na direção que quer expandir e use:

```
/flan expand <distância>
```

**Limitação:** O subclaim não pode ultrapassar as bordas do claim principal.

---

## Diferença entre Claim e Subclaim

| | Claim Principal | Subclaim |
|---|---|---|
| Criado por | Qualquer jogador | Dono ou Co-Owner do claim principal |
| Cobre | Área livre do mapa | Área dentro de outro claim |
| Custo | Blocos de claim do dono | Sem custo adicional |
| Permissões | Independentes | Independentes, herdam do pai por padrão |
| Pode ter subclaims dentro | Sim | Não |

---

## Ver Informações de um Subclaim

Dentro do subclaim:

```
/flan info
```

Mostra coordenadas, dono do claim principal e informações específicas do subclaim.

---

## Casos de Uso Comuns

- **Loja pública dentro da base:** Crie um subclaim na área da loja com permissão para interagir com blocos de comércio, mas sem permissão para quebrar blocos.
- **Quarto de hóspede:** Subclaim em uma parte da casa onde um amigo pode colocar e quebrar blocos livremente.
- **Fazenda compartilhada:** Subclaim na fazenda com permissão de colheita para membros do grupo.
- **Cofre privado:** Crie um subclaim no seu cofre sem dar acesso a ninguém, mesmo que o resto da base seja compartilhado.
