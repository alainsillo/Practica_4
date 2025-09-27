"""
practica4_archivo_instruccionesG.py
aqui vamos a ler un archivo de instrucciones y ejecutarlo ~~~!!! :D
Funciones permitidas:
- dibujar_cuadrado(x, y, lado, color)
- dibujar_triangulo(x, y, lado, color)
- dibujar_circulo(x, y, radio, color)
- dibujar_linea(x1, y1, x2, y2, color)
- teleport(x, y)
"""

import ast
import sys
import turtle

# --- Configuración de la ventana ---
turtle.setup(600, 600)
turtle.bgcolor("white")
t = turtle.Turtle()
t.speed(3)

# --- Funciones de dibujo ---
def dibujar_cuadrado(x, y, lado, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(lado)
        t.right(90)
    t.end_fill()

def dibujar_triangulo(x, y, lado, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(3):
        t.forward(lado)
        t.left(120)
    t.end_fill()

def dibujar_circulo(x, y, radio, color):
    t.penup()
    t.goto(x, y - radio)
    t.pendown()
    t.color(color)
    t.begin_fill()
    t.circle(radio)
    t.end_fill()

def dibujar_linea(x1, y1, x2, y2, color):
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.color(color)
    t.goto(x2, y2)

def teleport(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

# Mapeo de funciones permitidas
ALLOWED = {
    "dibujar_cuadrado": dibujar_cuadrado,
    "dibujar_triangulo": dibujar_triangulo,
    "dibujar_circulo": dibujar_circulo,
    "dibujar_linea": dibujar_linea,
    "teleport": teleport,
}

# --- Parser de instrucciones ---
def parse_instruction_line(line):
    try:
        expr = ast.parse(line, mode="eval").body
    except SyntaxError as e:
        raise ValueError(f"SyntaxError: {e}")

    if not isinstance(expr, ast.Call):
        raise ValueError("No es una llamada (Call)")

    if not isinstance(expr.func, ast.Name):
        raise ValueError("Función no es un nombre simple")

    name = expr.func.id
    if name not in ALLOWED:
        raise ValueError(f"Función '{name}' no permitida")

    args = []
    kwargs = {}
    try:
        for a in expr.args:
            args.append(ast.literal_eval(a))
        for kw in expr.keywords:
            if kw.arg is None:
                raise ValueError("**kwargs no soportado")
            kwargs[kw.arg] = ast.literal_eval(kw.value)
    except Exception as e:
        raise ValueError(f"Error evaluando argumentos: {e}")

    return name, args, kwargs

# --- Ejecutar archivo de instrucciones ---
def ejecutar_archivo_de_instrucciones(path):
    if not path:
        raise FileNotFoundError("No se indicó archivo de instrucciones")
    with open(path, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                name, args, kwargs = parse_instruction_line(line)
            except ValueError as e:
                print(f"⚠️ Warning (línea {lineno}): instrucción inválida -> {line}  ({e})")
                continue
            func = ALLOWED.get(name)
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"⚠️ Error ejecutando '{line}' (línea {lineno}): {e}")

# --- Main ---
if __name__ == "__main__":
    import os
    default = os.path.join(os.path.dirname(__file__), "dibujante.txt")
    path = sys.argv[1] if len(sys.argv) > 1 else default
    print(f"Ejecutando instrucciones desde: {path}")
    ejecutar_archivo_de_instrucciones(path)
    print("Turtle terminado. Cierra la ventana para finalizar el programa.")
    turtle.done()
