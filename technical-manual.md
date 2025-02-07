# Manual Técnico - Calculadora Gráfica con SymPy
pip install -r requirements.txt

## Índice
1. [Sintaxis Básica](#sintaxis-básica)
2. [Operadores y Símbolos](#operadores-y-símbolos)
3. [Funciones Matemáticas](#funciones-matemáticas)
4. [Tipos de Cálculos](#tipos-de-cálculos)
5. [Ejemplos Avanzados](#ejemplos-avanzados)

## Sintaxis Básica

### Operadores y Símbolos

| Operación | Sintaxis SymPy | Ejemplo | Notas |
|-----------|---------------|---------|--------|
| Suma | + | x + 1 | |
| Resta | - | x - 1 | |
| Multiplicación | * | 2*x | El operador es obligatorio |
| División | / | x/2 | |
| Potencia | ** o ^ | x**2 o x^2 | Ambas formas son válidas |
| Paréntesis | () | (x + 1)/(x - 1) | Agrupación de operaciones |
| Valor absoluto | abs() | abs(x) | |
| Infinito | oo | oo | Símbolo de infinito |
| Pi | pi | pi | Constante π |
| Euler | E | E | Constante e |

### Funciones Matemáticas Básicas

| Función | Sintaxis SymPy | Ejemplo | Descripción |
|---------|---------------|---------|-------------|
| Exponencial | exp() | exp(x) | e^x |
| Logaritmo natural | log() | log(x) | ln(x) |
| Logaritmo base 10 | log(x, 10) | log(x, 10) | log₁₀(x) |
| Raíz cuadrada | sqrt() | sqrt(x) | √x |
| Valor absoluto | abs() | abs(x) | \|x\| |

### Funciones Trigonométricas

| Función | Sintaxis SymPy | Inversa |
|---------|---------------|----------|
| Seno | sin(x) | asin(x) |
| Coseno | cos(x) | acos(x) |
| Tangente | tan(x) | atan(x) |
| Secante | sec(x) | asec(x) |
| Cosecante | csc(x) | acsc(x) |
| Cotangente | cot(x) | acot(x) |

### Funciones Hiperbólicas

| Función | Sintaxis SymPy | Inversa |
|---------|---------------|----------|
| Seno hiperbólico | sinh(x) | asinh(x) |
| Coseno hiperbólico | cosh(x) | acosh(x) |
| Tangente hiperbólica | tanh(x) | atanh(x) |

## Tipos de Cálculos

### 1. Integral
```python
# Sintaxis para entrada:
"x**2"        # Integral indefinida de x²
"sin(x)"      # Integral indefinida de sin(x)
"exp(x)*x"    # Integral indefinida de xe^x
```

Ejemplos con resultados:
```python
# Integral de x²
Entrada: "x**2"
Resultado: x³/3 + C

# Integral de e^x
Entrada: "exp(x)"
Resultado: exp(x) + C

# Integral de sin(x)
Entrada: "sin(x)"
Resultado: -cos(x) + C
```

### 2. Derivada
```python
# Sintaxis para entrada:
"x**3"        # Derivada de x³
"sin(x)*x"    # Derivada de x·sin(x)
"exp(x**2)"   # Derivada de e^(x²)
```

Ejemplos con resultados:
```python
# Derivada de x³
Entrada: "x**3"
Resultado: 3x²

# Derivada de sin(x)
Entrada: "sin(x)"
Resultado: cos(x)

# Derivada de e^x
Entrada: "exp(x)"
Resultado: exp(x)
```

### 3. Límite
```python
# Sintaxis para entrada:
Función: "(x**2 - 1)/(x - 1)"
Punto límite: "1"

Función: "sin(x)/x"
Punto límite: "0"
```

### 4. Área
```python
# Sintaxis para entrada:
Función: "x**2"
Límite inferior: "0"
Límite superior: "1"

Función: "sin(x)"
Límite inferior: "0"
Límite superior: "pi"
```

### 5. Funciones Especiales

#### Funciones a Trozos
```python
# Sintaxis:
"Piecewise((x**2, x > 0), (x, x <= 0))"

# Ejemplos:
"Piecewise((x, x > 0), (0, True))"  # Función rampa
"Piecewise((1, x > 0), (-1, x < 0), (0, True))"  # Función signo
```

#### Funciones con Parámetros
```python
# Definir parámetros:
a, b, c = symbols('a b c')
"a*x**2 + b*x + c"
```

## Ejemplos Avanzados

### 1. Cálculo de Integral Definida con Función Trigonométrica
```python
# Entrada:
Función: "sin(x)**2 * cos(x)"
Variable: "x"
Límite inferior: "0"
Límite superior: "pi/2"
```

### 2. Límite de una Función Racional
```python
# Entrada:
Función: "(x**3 - 1)/(x - 1)"
Variable: "x"
Punto límite: "1"
```

### 3. Volumen de Revolución
```python
# Entrada:
Función: "sqrt(1 - x**2)"
Variable: "x"
Límite inferior: "-1"
Límite superior: "1"
```

### 4. Centroide de una Región
```python
# Entrada:
Función: "x**2"
Variable: "x"
Límite inferior: "0"
Límite superior: "1"
```

## Consideraciones Técnicas

### Dominio de Funciones
- Verificar que la función esté definida en el intervalo especificado
- Evitar divisiones por cero
- Considerar el dominio de funciones como sqrt() y log()

### Limitaciones
1. Las funciones trigonométricas usan radianes
2. Los límites de integración deben ser números reales o símbolos matemáticos válidos
3. Las funciones deben ser continuas en el intervalo especificado para integrales definidas

### Optimización
- Usar formas simplificadas de funciones cuando sea posible
- Evitar expresiones innecesariamente complejas
- Considerar la simplificación de fracciones antes de los cálculos

## Mensajes de Error Comunes

| Error | Causa Probable | Solución |
|-------|---------------|-----------|
| "invalid syntax" | Error en la escritura de la función | Verificar paréntesis y operadores |
| "division by zero" | Función indefinida en un punto | Revisar el dominio de la función |
| "could not parse expression" | Sintaxis no reconocida | Usar la sintaxis correcta de SymPy |
| "math domain error" | Operación matemática inválida | Verificar el dominio de la función |

## Referencias Rápidas

### Constantes Matemáticas
```python
pi      # π
E       # e (número de Euler)
oo      # Infinito
I       # Unidad imaginaria
```

### Símbolos Especiales
```python
x, y, z = symbols('x y z')    # Variables
a, b, c = symbols('a b c')    # Parámetros
t = Symbol('t')              # Variable de tiempo
```
