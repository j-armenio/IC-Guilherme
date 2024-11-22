# Problema: Colorir mapa

O problema consiste em:

1. Cada região em um mapa deve ser colorida.
2. Nenhuma região adjacente pode ter a mesma cor.
3. Cores: **vermelho**, **verde** ou **azul**.

## Mapa da Australia

### Estruturar o problema de CSP

Definir

* **Variáveis**: Cada região do mapa será uma variável que precisa de uma cor.
X = {WA, NT, SA, Q, NSW, V, T}

* **Domínio**: O conjunto de cores possíveis para cada região.
D = {red, green, blue}

* **Restrições**: As restrições entre as variáveis, ou seja, nenhuma região adjacente pode ter a mesma cor.
C = {SA!=WA, SA!=NT, SA!=Q, SA!=NSW, SA!=V, WA!=NT, NT!=Q, Q!=NSW, NSW!=V}

### Entradas:

* Australia

```python
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
```

* Brasil

```python
# Brasil

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
```
