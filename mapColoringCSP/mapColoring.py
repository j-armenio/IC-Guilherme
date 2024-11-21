from collections import deque

def revise(r1, r2, domains, constraints):
    revised = False

    for color in domains[r1][:]:
        if not any(
            color != other_color
            for other_color in domains[r2]
        ):
            domains[r1].remove(color)
            revised = True

    return revised

# Retorna falso se alguma incosistencia de arco é encontrada e verdadeiro caso contrario
def ac_3(domains, constraints):
    queue = deque(constraints)

    while queue:
        (r1, r2) = queue.popLeft()

        if revise(r1, r2, domains, constraints):
            if not domains[regions]:
                return False
            
            for r in domains:
                if r != r1 and (r, r1) in constraints:
                    queue.append((r, r1))

    return True

# Verifica se a 'color' em 'region' atende as restrições
def is_consistent(region, color, assignment, constraints):
    for r1, r2 in constraints:
        if r1 == region: # Apenas regioes da restrição atual
            if assignment[r2] == color: # Verifica se a cor da restrição é igual
                return False
        
        if r2 == region:
            if assignment[r1] == color:
                return False
    return True

# Backtracking sem AC-3
def backtrack(assignment, constraints, domain): # Retorna ou a solução ou falha
    # Base da recursão
    has_none = 0
    for i in assignment.values():
        if i == None:
            has_none = 1
    if has_none == 0:
        return assignment

    # Escolhe variavel unassigned
    region = None
    for r in assignment:
        if assignment[r] == None:
            region = r
            break
    
    # Passo da recursão
    for color in domain:
        if is_consistent(region, color, assignment, constraints):
            assignment[region] = color

            # Chamada recursiva
            result = backtrack(assignment, constraints, domain)
            if result:
                return result

            assignment[region] = None
        
    return None # Não há solução

# Backtracking com AC-3
def backtrack2(assignment, constraints, domains):
    # base da recursão
    has_none = 0
    for i in assignment.values():
        if i == None:
            has_none = 1
    if has_none == 0:
        return assignment

    # escolhe uma variavel
    region = None
    for r in assignment:
        if assignment[r] is None:
            region = r
            break
    
    # tenta cada cor no dominio
    for color in domains[region]:
        if is_consistent(region, color, assignment, constraints):
            assignment[region] = color

            # faz uma copia do dominio para backtracking
            new_domains = {r: domains[r][:] for r in domains}
            if ac_3(new_domains, constraints):
                result = backtrack(assignment, constraints, new_domains)
                if result:
                    return result

            # reverte a atribuição se não for arc-consistency
            assignment[region] = None

    return None

# Australia

regions = ['WA','NT','Q','NSW','V','SA','T']

domain = ['red', 'green', 'blue']

constraints = [
    ('SA','WA'), ('SA','NT'), ('SA','Q'), ('SA','NSW'), ('SA','V'),
    ('WA','NT'), ('NT','Q'), ('Q','NSW'), ('NSW','V')
]

assignment = {
    'WA': None, 'NT': None, 'SA': None,
    'Q': None, 'NSW': None, 'V': None, 'T': None
}

domains = {}
for r in regions:
    domains[regions] = domain[:] # cria uma cópia da lista de dominio em cada domains[regions]

# domains = 
# {'WA': ['green', 'blue'], 
#  'NT': ['red', 'green', 'blue'], 
#  'SA': ['red', 'green', 'blue']}

if ac_3(domains, constraints):
    result = backtrack(assignment, constraints, domains)
    print(result)
else:
    print("Problema inconsistente.")

# Teste sem consistencia de arco
# print(backtrack(assignment, constraints, domain))
