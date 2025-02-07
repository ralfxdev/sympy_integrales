"""
Advanced Calculator with Graphs
-----------------------------
Una aplicación de calculadora gráfica que permite realizar cálculos matemáticos avanzados
y visualizar los resultados mediante gráficos.

Este módulo implementa una interfaz gráfica usando tkinter para realizar
operaciones matemáticas como integrales, derivadas, límites, áreas, volúmenes
y valores promedio de funciones matemáticas.

Dependencias:
    - tkinter: Para la interfaz gráfica
    - sympy: Para cálculos simbólicos
    - numpy: Para operaciones numéricas
    - matplotlib: Para visualización de gráficos
"""

import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate():
    """
    Realiza el cálculo matemático seleccionado basado en la entrada del usuario.
    
    Procesa la función matemática ingresada según el tipo de cálculo seleccionado
    (integral, derivada, límite, área, volumen o promedio) y muestra tanto el
    resultado numérico como su representación gráfica.
    """
    calculation_type = calculation_var.get()
    function = input_function.get()
    variable = sp.symbols(input_variable.get())

    if calculation_type == "Integral":
        integral = sp.integrate(function, variable)
        simplified_result = sp.simplify(integral)
        result.set(f"Integral: {simplified_result}")
        plot_function_and_result(function, variable, simplified_result, "Integral")
    elif calculation_type == "Derivative":
        derivative = sp.diff(function, variable)
        simplified_result = sp.simplify(derivative)
        result.set(f"Derivative: {simplified_result}")
        plot_function_and_result(function, variable, simplified_result, "Derivative")
    elif calculation_type == "Limit":
        limit_point = sp.sympify(input_limit_point.get())
        limit = sp.limit(function, variable, limit_point)
        result.set(f"Limit: {limit}")
        plot_limit(function, variable, limit_point, limit)
    elif calculation_type == "Area":
        lower_bound = sp.sympify(input_lower_bound.get())
        upper_bound = sp.sympify(input_upper_bound.get())
        area = sp.integrate(function, (variable, lower_bound, upper_bound))
        result.set(f"Area: {area}")
        plot_area(function, variable, lower_bound, upper_bound)
    elif calculation_type == "Volume":
        lower_bound = sp.sympify(input_lower_bound.get())
        upper_bound = sp.sympify(input_upper_bound.get())
        function_sympy = sp.sympify(function)
        volume = sp.pi * sp.integrate(function_sympy**2, (variable, lower_bound, upper_bound))
        result.set(f"Volume: {volume}")
        plot_volume(function, variable, lower_bound, upper_bound)
    elif calculation_type == "Average":
        lower_bound = sp.sympify(input_lower_bound.get())
        upper_bound = sp.sympify(input_upper_bound.get())
        average_value = (1 / (upper_bound - lower_bound)) * sp.integrate(function, (variable, lower_bound, upper_bound))
        result.set(f"Average: {average_value}")
        plot_average(function, variable, lower_bound, upper_bound, average_value)
    elif calculation_type == "Surface Area":
        lower_bound = sp.sympify(input_lower_bound.get())
        upper_bound = sp.sympify(input_upper_bound.get())
        function_sympy = sp.sympify(function)
        area_of_revolution = 2 * sp.pi * sp.integrate(function_sympy, (variable, lower_bound, upper_bound))
        result.set(f"Area of Revolution: {area_of_revolution}")
        plot_surface_area(function, variable, lower_bound, upper_bound)
    elif calculation_type == "Centroid / Center of Mass":
        lower_bound = sp.sympify(input_lower_bound.get())
        upper_bound = sp.sympify(input_upper_bound.get())
        density = 1  # Densidad por defecto = 1

        # Coordenadas del centroide
        x_centroid = sp.integrate(variable * density * sp.sympify(function), (variable, lower_bound, upper_bound)) / sp.integrate(density * sp.sympify(function), (variable, lower_bound, upper_bound))
        y_centroid = sp.integrate(density * sp.sympify(function)**2, (variable, lower_bound, upper_bound)) / (2 * sp.integrate(density * sp.sympify(function), (variable, lower_bound, upper_bound)))

        result.set(f"Centroid: (x̄ = {x_centroid}, ȳ = {y_centroid})")
        plot_centroid(function, variable, lower_bound, upper_bound, x_centroid, y_centroid)
        
    elif calculation_type == "Partial Derivative":
        variable_2 = sp.symbols(input_variable_2.get())
        partial_derivative = sp.diff(function, variable_2)
        simplified_result = sp.simplify(partial_derivative)
        result.set(f"Partial Derivative with respect to {input_variable_2.get()}: {simplified_result}")
        plot_partial(function, variable, simplified_result, "Partial Derivative")


    elif calculation_type == "Chain Rule":
        outer_function = input_outer_function.get()
        inner_function = input_inner_function.get()
        variable_name = input_variable.get()

        # Validación de entradas
        if not outer_function or not inner_function or not variable_name:
            result.set("Error: Debe ingresar ambas funciones (externa e interna) y la variable.")
            return

        # Definir la variable simbólica
        x = sp.symbols(variable_name)

        # Derivada de la función interna
        inner_derivative = sp.diff(inner_function, x)
        
        # Derivada de la función externa
        outer_function_sympy = sp.sympify(outer_function.replace('u', f'({inner_function})'))
        outer_derivative = sp.diff(outer_function_sympy, x)
        
        # Aplicar la regla de la cadena
        chain_rule_result = outer_derivative.subs(x, inner_function) * inner_derivative

        # Mostrar resultado en la interfaz
        result.set(f"Chain Rule Result: {chain_rule_result}")

        # Graficar la función externa y su derivada
        plot_chain_rule(outer_function, inner_function, chain_rule_result, x)


def plot_function_and_result(function, variable, result, plot_type):
    """
    Genera gráficos comparativos de la función original y su resultado.

    Args:
        function (str): Función matemática original
        variable (sympy.Symbol): Variable de la función
        result (sympy.Expr): Resultado del cálculo
        plot_type (str): Tipo de operación realizada
    """
    function_sympy = sp.sympify(function)
    result_sympy = sp.sympify(result)

    # Convertir expresiones simbólicas a funciones numéricas
    f = sp.lambdify(variable, function_sympy, modules=['numpy'])
    g = sp.lambdify(variable, result_sympy, modules=['numpy'])

    # Generar valores para el eje x
    x_vals = np.linspace(-10, 10, 400)
    y_vals_function = f(x_vals)
    y_vals_result = g(x_vals)

    # Crear subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
    ax1.plot(x_vals, y_vals_function, label=f'Function: {function}')
    ax1.legend()
    ax1.set_xlabel(str(variable))
    ax1.set_ylabel('y')
    ax1.set_title('Original Function')
    ax1.grid(True)

    ax2.plot(x_vals, y_vals_result, label=f'{plot_type}: {result}', color='r')
    ax2.legend()
    ax2.set_xlabel(str(variable))
    ax2.set_ylabel('y')
    ax2.set_title(f'{plot_type} of Function')
    ax2.grid(True)

    update_graph(fig)
    
def plot_partial(function, variable, result, plot_type):
        """
        Genera gráficos comparativos de la función original y su resultado.

        Args:
            function (str): Función matemática original
            variable (sympy.Symbol): Variable de la función
            result (sympy.Expr): Resultado del cálculo
            plot_type (str): Tipo de operación realizada
        """
        function_sympy = sp.sympify(function)
        result_sympy = sp.sympify(result)

        # Convertir expresiones simbólicas a funciones numéricas
        f = sp.lambdify((variable, 'y'), function_sympy, modules=['numpy'])
        g = sp.lambdify((variable, 'y'), result_sympy, modules=['numpy'])

        # Generar valores para el eje x e y
        x_vals = np.linspace(-10, 10, 400)
        y_vals = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x_vals, y_vals)

        Z_function = f(X, Y)
        Z_result = g(X, Y)

        # Crear subplots
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(211, projection='3d')
        ax1.plot_surface(X, Y, Z_function, alpha=0.7, rstride=100, cstride=100, label='Function')
        ax1.set_title('Original Function')
        ax1.set_xlabel(str(variable))
        ax1.set_ylabel('y')
        ax1.set_zlabel('f(x, y)')
        ax1.grid(True)


        ax2 = fig.add_subplot(212, projection='3d')
        ax2.plot_surface(X, Y, Z_result, color='r', alpha=0.7, rstride=100, cstride=100)
        ax2.set_title(f'{plot_type} of Function')
        ax2.set_xlabel(str(variable))
        ax2.set_ylabel('y')
        ax2.set_zlabel(f'{plot_type}(x, y)')
        ax2.grid(True)

        update_graph(fig)

def plot_limit(function, variable, limit_point, limit):
    """
    Genera un gráfico que muestra el límite de una función.

    Args:
        function (str): Función matemática
        variable (sympy.Symbol): Variable de la función
        limit_point (float): Punto donde se evalúa el límite
        limit (float): Valor del límite
    """
    function_sympy = sp.sympify(function)
    f = sp.lambdify(variable, function_sympy, modules=['numpy'])

    x_vals = np.linspace(float(limit_point) - 5, float(limit_point) + 5, 400)
    y_vals = f(x_vals)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_vals, y_vals, label=f'Function: {function}')
    ax.plot(limit_point, limit, 'ro', label=f'Limit: {limit}')
    ax.legend()
    ax.set_xlabel(str(variable))
    ax.set_ylabel('y')
    ax.set_title(f'Limit of Function as {variable} approaches {limit_point}')
    ax.grid(True)

    update_graph(fig)

def plot_area(function, variable, lower_bound, upper_bound):
    """
    Genera un gráfico que muestra el área bajo la curva.

    Args:
        function (str): Función matemática
        variable (sympy.Symbol): Variable de la función
        lower_bound (float): Límite inferior de integración
        upper_bound (float): Límite superior de integración
    """
    function_sympy = sp.sympify(function)
    f = sp.lambdify(variable, function_sympy, modules=['numpy'])

    x_vals = np.linspace(float(lower_bound), float(upper_bound), 400)
    y_vals = f(x_vals)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_vals, y_vals, label=f'Function: {function}')
    ax.fill_between(x_vals, y_vals, alpha=0.3)
    ax.legend()
    ax.set_xlabel(str(variable))
    ax.set_ylabel('y')
    ax.set_title(f'Area under the curve from {lower_bound} to {upper_bound}')
    ax.grid(True)

    update_graph(fig)

def plot_volume(function, variable, lower_bound, upper_bound):
    """
    Genera un gráfico 3D que muestra el volumen de revolución.

    Args:
        function (str): Función matemática
        variable (sympy.Symbol): Variable de la función
        lower_bound (float): Límite inferior de integración
        upper_bound (float): Límite superior de integración
    """
    function_sympy = sp.sympify(function)
    f = sp.lambdify(variable, function_sympy, modules=['numpy'])

    x_vals = np.linspace(float(lower_bound), float(upper_bound), 100)
    y_vals = f(x_vals)

    # Crear malla para gráfico 3D
    theta = np.linspace(0, 2 * np.pi, 100)
    x, t = np.meshgrid(x_vals, theta)

    y = np.outer(np.ones(np.size(theta)), y_vals) * np.cos(t)
    z = np.outer(np.ones(np.size(theta)), y_vals) * np.sin(t)
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(x, y, z, alpha=0.7)
    ax.set_xlabel(str(variable))
    ax.set_ylabel('y (cosine projection)')
    ax.set_zlabel('z (sine projection)')
    ax.set_title(f'Volume of revolution from {lower_bound} to {upper_bound}')

    update_graph(fig)

def plot_average(function, variable, lower_bound, upper_bound, average_value):
    """
    Genera un gráfico que muestra el valor promedio de la función.

    Args:
        function (str): Función matemática
        variable (sympy.Symbol): Variable de la función
        lower_bound (float): Límite inferior
        upper_bound (float): Límite superior
        average_value (float): Valor promedio calculado
    """
    function_sympy = sp.sympify(function)
    f = sp.lambdify(variable, function_sympy, modules=['numpy'])

    x_vals = np.linspace(float(lower_bound), float(upper_bound), 400)
    y_vals = f(x_vals)

    average_value_float = float(average_value)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_vals, y_vals, label=f'Function: {function}')
    ax.axhline(y=average_value_float, color='r', linestyle='--', 
               label=f'Average: {average_value_float}')
    ax.fill_between(x_vals, y_vals, average_value_float, 
                   where=(y_vals > average_value_float), alpha=0.3)
    ax.fill_between(x_vals, y_vals, average_value_float, 
                   where=(y_vals <= average_value_float), color='gray', alpha=0.3)
    ax.legend()
    ax.set_xlabel(str(variable))
    ax.set_ylabel('y')
    ax.set_title(f'Average Value of Function from {lower_bound} to {upper_bound}')
    ax.grid(True)

    update_graph(fig)
    
def plot_surface_area(function, variable, lower_bound, upper_bound):
    """
    Genera un gráfico que muestra el área de superficie de revolución.

    Args:
        function (str): Función matemática
        variable (sympy.Symbol): Variable de la función
        lower_bound (float): Límite inferior de integración
        upper_bound (float): Límite superior de integración
    """
    function_sympy = sp.sympify(function)
    f = sp.lambdify(variable, function_sympy, modules=['numpy'])

    x_vals = np.linspace(float(lower_bound), float(upper_bound), 100)
    y_vals = f(x_vals)

    theta = np.linspace(0, 2 * np.pi, 100)
    x, t = np.meshgrid(x_vals, theta)

    y = np.outer(np.ones(np.size(theta)), y_vals) * np.cos(t)
    z = np.outer(np.ones(np.size(theta)), y_vals) * np.sin(t)
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(x, y, z, alpha=0.7)
    ax.set_xlabel(str(variable))
    ax.set_ylabel('y (cosine projection)')
    ax.set_zlabel('z (sine projection)')
    ax.set_title(f'Surface Area of revolution from {lower_bound} to {upper_bound}')

    update_graph(fig)
    
def plot_centroid(function, variable, lower_bound, upper_bound, x_centroid, y_centroid):
    function_sympy = sp.sympify(function)
    f = sp.lambdify(variable, function_sympy, modules=['numpy'])

    x_vals = np.linspace(float(lower_bound), float(upper_bound), 400)
    y_vals = f(x_vals)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Graficar la función
    ax.plot(x_vals, y_vals, color='blue', label=f'Function: {function}', linewidth=2)
    
    # Rellenar el área bajo la curva
    ax.fill_between(x_vals, y_vals, color='lightblue', alpha=0.3, label='Area under curve')

    # Graficar el centroide con un marcador distintivo
    ax.plot(float(x_centroid), float(y_centroid), 'ro', markersize=10, label=f'Centroid: ({x_centroid:.2f}, {y_centroid:.2f})')
    
    # Agregar líneas punteadas para el centroide
    ax.axvline(x=float(x_centroid), color='red', linestyle='--', alpha=0.7)
    ax.axhline(y=float(y_centroid), color='red', linestyle='--', alpha=0.7)
    
    # Mejorar la presentación de los ejes
    ax.set_xlim(float(lower_bound) - 1, float(upper_bound) + 1)
    ax.set_ylim(min(y_vals) - 1, max(y_vals) + 1)
    ax.set_aspect('equal', adjustable='box')

    # Etiquetas y título
    ax.set_xlabel(str(variable), fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Centroid of the Region under the Curve', fontsize=14)
    
    # Activar cuadrícula
    ax.grid(True, linestyle='--', alpha=0.5)

    # Leyenda
    ax.legend(fontsize=10, loc='best')

    # Mostrar gráfica mejorada
    update_graph(fig)
    
def plot_chain_rule(outer_function, inner_function, chain_rule_result, variable):
    """
    Grafica la función original y su derivada.
    """
    # Convertir funciones simbólicas a funciones numéricas
    inner_func_numeric = sp.lambdify(variable, sp.sympify(inner_function), modules=['numpy'])
    outer_func_numeric = sp.lambdify(variable, sp.sympify(outer_function.replace('u', f'({inner_function})')), modules=['numpy'])
    chain_rule_numeric = sp.lambdify(variable, chain_rule_result, modules=['numpy'])

    # Valores para el eje x
    x_vals = np.linspace(-10, 10, 400)
    y_vals_inner = inner_func_numeric(x_vals)
    y_vals_outer = outer_func_numeric(x_vals)
    y_vals_chain = chain_rule_numeric(x_vals)

    # Crear gráficos
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_vals, y_vals_outer, label=f'Outer Function: {outer_function.replace("u", f"({inner_function})")}', color='blue')
    ax.plot(x_vals, y_vals_chain, label='Chain Rule Result', color='red', linestyle='--')
    ax.axhline(0, color='black', lw=0.5, ls='--')
    ax.axvline(0, color='black', lw=0.5, ls='--')
    ax.set_title('Function and its Derivative using Chain Rule')
    ax.set_xlabel(str(variable))
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True)

    # Actualizar el gráfico en la interfaz
    update_graph(fig)


def update_graph(fig):
    """
    Actualiza el widget de gráfico en la interfaz.

    Args:
        fig (matplotlib.figure.Figure): Figura a mostrar
    """
    for widget in graph_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def update_input_fields(*args):
    """
    Actualiza los campos de entrada según el tipo de cálculo seleccionado.
    
    Args:
        *args: Argumentos variables (no utilizados pero requeridos por el trace)
    """
    calculation_type = calculation_var.get()
    
    # Limpiar campos existentes
    for widget in input_frame.winfo_children():
        widget.grid_remove()
    
    # Campos básicos presentes en todos los tipos de cálculo
    ttk.Label(input_frame, text="Function:").grid(column=0, row=0, padx=10, pady=10)
    ttk.Entry(input_frame, textvariable=input_function).grid(column=1, row=0, padx=10, pady=10)
    
    ttk.Label(input_frame, text="Variable:").grid(column=0, row=1, padx=10, pady=10)
    ttk.Entry(input_frame, textvariable=input_variable).grid(column=1, row=1, padx=10, pady=10)
    
    # Campos adicionales según el tipo de cálculo
    if calculation_type in ["Area", "Volume", "Average", "Surface Area", "Centroid / Center of Mass"]:
        ttk.Label(input_frame, text="Lower Bound:").grid(column=0, row=2, padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=input_lower_bound).grid(column=1, row=2, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Upper Bound:").grid(column=0, row=3, padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=input_upper_bound).grid(column=1, row=3, padx=10, pady=10)
    elif calculation_type == "Limit":
        ttk.Label(input_frame, text="Limit Point:").grid(column=0, row=2, padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=input_limit_point).grid(column=1, row=2, padx=10, pady=10)
        
    elif calculation_type == "Partial Derivative":

        ttk.Label(input_frame, text="Variable 2:").grid(column=0, row=2, padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=input_variable_2).grid(column=1, row=2, padx=10, pady=10)

    elif calculation_type == "Chain Rule":
        ttk.Label(input_frame, text="Outer Function:").grid(column=0, row=2, padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=input_outer_function).grid(column=1, row=2, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Inner Function:").grid(column=0, row=3, padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=input_inner_function).grid(column=1, row=3, padx=10, pady=10)


# Configuración de la ventana principal
window = tk.Tk()
window.title("Advanced Calculator with Graphs")

# Variables de control
calculation_var = tk.StringVar()
input_function = tk.StringVar()
input_variable = tk.StringVar()
input_lower_bound = tk.StringVar()
input_upper_bound = tk.StringVar()
input_limit_point = tk.StringVar()
input_variable_2 = tk.StringVar()
input_outer_function = tk.StringVar()
input_inner_function = tk.StringVar()
result = tk.StringVar()

# Frames para organizar la interfaz
menu_frame = ttk.Frame(window)
menu_frame.grid(column=0, row=0, padx=10, pady=10)
input_frame = ttk.Frame(window)
input_frame.grid(column=0, row=1, padx=10, pady=10)
result_frame = ttk.Frame(window)
result_frame.grid(column=0, row=2, padx=10, pady=10)
graph_frame = ttk.Frame(window)
graph_frame.grid(column=0, row=3, padx=10, pady=10)

# Menú de selección de tipo de cálculo
calculation_types = ["Integral", "Derivative", "Limit", "Area", "Volume", "Surface Area", "Average","Centroid / Center of Mass","Partial Derivative", "Chain Rule"]
ttk.Label(menu_frame, text="Calculation Type:").grid(column=0, row=0, padx=10, pady=10)
calculation_menu = ttk.Combobox(menu_frame, textvariable=calculation_var, values=calculation_types)
calculation_menu.grid(column=1, row=0, padx=10, pady=10)
calculation_menu.set("Integral")

# Inicialización de campos de entrada
update_input_fields()

ttk.Button(result_frame, text="Calculate", command=calculate).grid(column=0, row=0, padx=10, pady=10)

ttk.Label(result_frame, textvariable=result).grid(column=1, row=0, padx=10, pady=10)

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(3, weight=1)

calculation_var.trace("w", update_input_fields)

window.mainloop()
