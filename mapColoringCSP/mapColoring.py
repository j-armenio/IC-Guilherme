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

# Retorna falso se alguma inconsistência de arco é encontrada e verdadeiro caso contrário
def ac_3(domains, constraints):
    queue = deque(constraints)
    processed_arcs = set()

    while queue:
        (r1, r2) = queue.popleft()

        if revise(r1, r2, domains, constraints):
            if not domains[r1]:
                return False
            
        for r in domains:
            if r != r1 and ((r, r1) in constraints or (r1, r) in constraints) and (r, r1) not in processed_arcs:
                queue.append((r, r1))
                processed_arcs.add((r, r1))

    return True

# Verifica se a 'color' em 'region' atende as restrições
def is_consistent(region, color, assignment, constraints):
    for r1, r2 in constraints:
        if r1 == region: # Apenas regiões da restrição atual
            if assignment[r2] == color: # Verifica se a cor da restrição é igual
                return False
        
        if r2 == region:
            if assignment[r1] == color:
                return False
    return True

# Backtracking sem AC-3
def backtrack(assignment, constraints, domains): # Retorna ou a solução ou falha
    # Base da recursão
    if all(value is not None for value in assignment.values()): # Verifica se todas as variáveis foram atribuídas
        return assignment

    # Escolhe variável não atribuída
    region = next(r for r in assignment if assignment[r] is None)
    
    # Passo da recursão
    for color in domains[region]:
        if is_consistent(region, color, assignment, constraints):
            assignment[region] = color

            # Chamada recursiva
            result = backtrack(assignment, constraints, domains)
            if result:
                return result

            assignment[region] = None
        
    return None # Não há solução

# Backtracking com AC-3
def backtrack2(assignment, constraints, domains):
    # Base da recursão
    if all(value is not None for value in assignment.values()): # Verifica se todas as variáveis foram atribuídas
        return assignment

    # Escolhe uma variável
    region = next(r for r in assignment if assignment[r] is None)
    
    # Tenta cada cor no domínio
    for color in domains[region]:
        if is_consistent(region, color, assignment, constraints):
            assignment[region] = color

            # Faz uma cópia do domínio para backtracking
            new_domains = {r: domains[r][:] for r in domains}
            if ac_3(new_domains, constraints):
                result = backtrack2(assignment, constraints, new_domains)
                if result:
                    return result

            # Reverte a atribuição se não for arc-consistency
            assignment[region] = None

    return None


# =============== INPUT ===============

regions = [
    'AC', 'AM', 'RR', 'RO', 'PA', 'AP', 'TO', 
    'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA',
    'MT', 'MS', 'GO', 'DF', 
    'MG', 'ES', 'RJ', 'SP',
    'PR', 'SC', 'RS'
]

domain = ['red', 'green', 'blue']

constraints = [
    ('AC', 'AM'), ('AC', 'RO'),
    ('AM', 'RR'), ('AM', 'PA'), ('AM', 'RO'), 
    ('RR', 'PA'), 
    ('RO', 'MT'), ('RO', 'TO'),
    ('PA', 'TO'), ('PA', 'MT'), ('PA', 'MA'), ('PA', 'AP'),
    ('TO', 'MT'), ('TO', 'MA'), ('TO', 'PI'), 
    ('MA', 'PI'), ('MA', 'PA'),
    ('PI', 'CE'), ('PI', 'BA'), 
    ('CE', 'RN'), ('CE', 'PB'), ('CE', 'PE'), 
    ('RN', 'PB'), 
    ('PB', 'PE'), 
    ('PE', 'AL'), ('PE', 'BA'), 
    ('AL', 'SE'), ('AL', 'BA'), 
    ('SE', 'BA'),
    ('BA', 'MG'), ('BA', 'GO'), ('BA', 'ES'),
    ('MT', 'MS'), ('MT', 'GO'),
    ('MS', 'GO'), ('MS', 'PR'),
    ('GO', 'DF'), ('GO', 'MG'),
    ('DF', 'GO'), 
    ('MG', 'ES'), ('MG', 'SP'), ('MG', 'RJ'),
    ('ES', 'RJ'),
    ('RJ', 'SP'),
    ('SP', 'PR'),
    ('PR', 'SC'),
    ('SC', 'RS')
]

assignment = {
    'AC': None, 'AM': None, 'RR': None, 'RO': None, 'PA': None, 'AP': None, 'TO': None,
    'MA': None, 'PI': None, 'CE': None, 'RN': None, 'PB': None, 'PE': None, 'AL': None, 'SE': None, 'BA': None,
    'MT': None, 'MS': None, 'GO': None, 'DF': None,
    'MG': None, 'ES': None, 'RJ': None, 'SP': None,
    'PR': None, 'SC': None, 'RS': None
}

domains = {}
for region in regions:
    domains[region] = domain[:] # Cria uma cópia da lista de cores

# ===== Teste com consistência de arco =====
if ac_3(domains, constraints):
    result = backtrack2(assignment, constraints, domains)
    print(result)
else:
    print("Problema inconsistente.")

# ===== Teste sem consistência de arco =====
# print(backtrack(assignment, constraints, domains))
