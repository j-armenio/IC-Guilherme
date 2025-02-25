# Constraint Satisfaction Problems CSP

Um problema é resolvido quando cada variável tem um valor que satisfaz todos *constraints*/restrições aplicados na variável.

*X* conjunto de variáveis {X1,...,Xn}.
*D* conjunto de domínios {D1,...,Dn}, um para cada variável.
*C* conjunto de restrições que especifica combinações possíveis de valores.

Um domínio Di consiste de um conjunto de valores possíveis {v1,...,vk} para a variável Xi.

Restrições Cj são definidas por um par <scope,rel>. Ex: <(X1,X1),X1>X2>
scope: tupla de variaveis que participam da relação;
rel: relação que define o valor que essas variáveis podem ter;

**Atribuições** de valores a variáveis que não violam restrições são chamados **consistentes**.

Tipos de restrições:
* Unary constraint: restringe o valor de uma única variável. Ex: <(X),X != green>
* Binary constraint: relaciona duas variáveis. Ex: X != Y
    * Um CSP binário é um que possue apenas restrições unaries and binarias. Pode ser representado como um grafo de restrições.
* Higher-order constraints

## Forma mais simples de se resolver um problema formulado em CSP

### Backtracking puro

1. Selecionar uma variável não atribuída: escolhe a próxima variável que ainda não foi atribuida um valor
2. Escolher um valor para a variável: escolhe um valor do domínio da variável
3. Verificar se a atribuição é consistente: verifica se a atribuição respeita as retrições
    * Se for consistente, avança para próxima variável
    * Se não for consistente, tenta outro valor do domínio
4. Se todas variáveis forem atribuídas, retorna solução
5. Se não houver valores disponíveis, retroceder/backtrack para variável anterior e tentar outra atribuição
6. Repetir até encontrar uma solução ou concluir que nenhuma solução é possível

```python
def backtracking(atribuicoes, variaveis, dominios, restricoes)
    # (4) Se todas variaveis foram atribuidas, retorna solucao 
    if len(atribuicoes) == len(variaveis):
        return atribuicoes

    # (1) Escolhe uma variavel nao atribuida
    var = selecione_variavel_sem_valor(atribuicoes, variaveis)

    # (2) Percorre valores possiveis para a variavel 
    for valor in dominios[var]:
        # (3) Verifica se a atribuição do valor à variavel respeita as restrições
        if eh_consistente(var, valor, atribuicoes, restricoes):
            atribuicoes[var] = valor # Atribui valor
            # (6) Chama recursivamente para a próxima variável
            resultado = backtracking(atribuicoes, variaveis, dominios, restricoes)
            if resultado is not None: # (4) Se encontrou uma solução, retorna
                return resultado
            atribuicoes.pop(var) # (5) Reomve atribuicao para fazer backtrack
        
    # (6) Nenhuma solucao encontrada
    return None
```

## Constraint Propagation: Inferencia em CSP

Existe um tipo de inferência chamado de **constraint propagation**: usa restrições para reduzir o número de legal values para uma variável, o que pode reduzir os legal values de outra variável e assim em diante. Isso reduz a quantidade de escolhas a se considerar quando for fazer a próxima atribuição de uma variável. 

A ideia chave é **consistência local**.

### Node consistency

Cada variável individualmente satisfaça todas as restrições unárias que se aplicam a ela.

Se houver uma restrição P(X) (uma condição que restringe os valores possíveis para X), então todos valores no domínio de X devem satisfazer P(X). Se um valor v ∈ Dom(X) não satisfaz a restrição unária, ele deve ser removido do domínio.

### Arc Consistency (AC)

Cada variável individualmente satisfaça todas as restrições binárias que se aplicam a ela.

Uma variável Xi é arco-consistente com respeito a outra variável Xj se para cada valor no domínio atual Di existe algum valor Dj que satisfaz a restrição binária do arco (Xi,Xj).

Um grafo é arco-consistente se toda variável é arco-consistente com toda outra variável.

Ex: restrição: Y = X², onde o domínio de X e Y é o conjunto de digitos decimais, explicitamente 
<(X,Y),{(0,0),(1,1),(2,4),(3,9)}>

Para fazer X arco-consistente com respeito a Y, reduzimos o dominio de X para {0,1,2,3}, em seguida, para fazer Y arco-consistente com respeito a X, reduzimos o dominio de Y para {0,1,4,9} e assim todo CSP é arco-consistente.

Dominio inicial: X = Y = {0,1,2,3,4,5,6,7,8,9}
Dominio após consistência de arco: X = {0,1,2,3}, Y = {0,1,4,9}

### Generalized Arc Consistency (GAC)

Consistência de arco para restrições não-binárias.

* A melhor complexidade que pode ser encontrada para um algoritmo que aplica GAC em uma rede sem tipos de restrições é *O(erd^r)*, onde *e* é o número de restrições e *r* é a maior aridade de uma restrição e *d* é o tamanho máximo do domínio de uma variável.

#### AC-3

É o algoritmo mais popular que aplica consistência de arco. Ele gera uma **fila de arcos** que faz iterações sucessivas removendo valores inconsistentes até que o problema esteja arc-consistente.

* Proposto para binary normalized networks e alcança a 2-consistency.

* O principal componente do GAC3 é a revisão de um arco, isso é, a atualização do domínio de uma restrição.

* O algoritmo principal é um loop simples que revisa todos arcos até que não ocorra nenhuma mudança, para garantir que todos dominios estão consistentes com todas restrições.

* Tem tempo *O(er³d^(r+1))* e espaço *O(er)*, onde r é a maior aridade entre as restrições.

1. Coloca todos arcos na fila. (Cada restrição binária se torna dois arcos, um em cada sentido);
2. Processamento de arcos:
    * Pega um arco (X,Y) da fila/
    * Para cada valor v em X, verifica se há pelo menos um valor w em Y que satisfaça a restrição.
    * Se **não houver tal valor**, remove v do domínio de X.
    * Se o domínio de X for alterado, adicionamos todos os arcos relacionados a X de volta na fila.
3. Repete o processo até que nenhum valor possa ser removido.

pseudo:
```pseudo
function REVISE(csp,Xi,Xj) returns true if we revise the domain of Xi
    revised <- false
    for each x in Di do
        if no value y in Dj allows(x,y) to satisfy the constraint between Xi and Xj then
            delete x from Di
            revised <- true
    return revised

function AC-3(csp) returns false iff an inconsistency is found and true otherwise
    queue <- a queue of arcs, initially all the arcs in csp

    while queue is not empty do
        (Xi,Xj) <- POP(queue)
        if REVISE(csp, Xi,Xj) then
            if size of Di = 0 then return false
            for each Xk in Xi.neighbors-{Xj} do
                add(Xk,Xi) to queue
    return true
```
python:
```python
def revise(csp, X, Y):
    revised = False
    for x in set(csp.dominios[X]): # Para cada valor x em X
        if not any(csp.satisfaz(x, y) for y in csp.dominios[Y]): # Se não há y válido
            csp.dominios[X].remove(x) # Remove x do domínio de X
            revised = True
    
    return revised

def ac3(csp):
    fila = deque(csp.restricoes) # Inicializa fila com todos arcos (X, Y)

    while fila:
        (X, Y) = queue.popleft() # Pega um arco da fila

        if revise(csp, X, Y): # Verifica se precisa remover valores do dominio de X
            if not csp.dominios[X]: # Se o dominio de X ficou vazio, nao ha solucao
                return False

            for Z in csp.vizinhos[X]: # Adiciona de volta os arcos que dependem de X
                if Z != Y:
                    queue.append((Z, X))

    return True # CSP ficou arco-consistente
```

* **Complexidade**: Assuma um CSP com *n* variáveis, cada uma com um domínio de tamanho máximo *d*, e com *c* restrições binárias (arcos). Cada arco (Xk,Xi) pode ser inserido na fila apenas *d* vezes, pois Xi tem no máximo *d* valores para deletar. Pode ser feito em tempo *O(d²)*, e *O(cd³)* no tempo do pior caso.

##### Diferenças Backtracking puro e AC-3:

* Backtracking é um método de busca recursivo que tenta atribuir valores e verifica as restrições **depois de cada atribuição**. Se uma atribuição viola a restrição, ele **desfaz a escolha e tenta outro valor**.
* AC-3 reduz o espaço de busca **antes da tentativa de atribuições**.
* AC-3 **não** necessariamente resolve o problema sozinho, só reduz o espaço de busca, eliminando valores impossíveis.

* Grande diferença é no momento e forma como tratar restrições: o AC-3 remove valores incosistentes antes de começar a busca, enquanto o Backtracking só percebe incosistências depois de atribuir valores e testar as restrições.

##### Problema do AC3

A time complexity do AC3 não é ótima. A função `Revise` não se lembra de suas computações anteriores e refaz verificações que já foram realizadas.

**Ex**:

* Variáveis: x,y,z
* Restrições: c1(x,y), c2(y,z)
* Domínios: D(x) = D(y)

Considere que as revisões:
1. Revise(x, c1): sucesso, sem alterações.
2. Revise(y, c1): sucesso, sem alterações.
3. Revise(y, c2): afeta o domínio de y, e como y tem restrições que afetam x, o arco (x, c1) deve ser adicionado novamente a fila.
4. Revise(z, c2): sucesso, sem alterações.
5. Revise(x, c1): se revisa novamente esse arco, porém, a maior parte das verificações já foram feitas anteriormente. 

#### AC-4

