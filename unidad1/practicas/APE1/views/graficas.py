"""Gráficas de la práctica APE1 (matplotlib)."""

import os

import matplotlib.pyplot as plt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "dist")


def _horas(filas):
    return [f["hora"] for f in filas]


def _guardar(archivo):
    """Guarda la figura en dist/ y la muestra en pantalla."""
    os.makedirs(SALIDA, exist_ok=True)
    plt.savefig(os.path.join(SALIDA, archivo), dpi=150)
    plt.show()


def _umbrales():
    """Líneas de referencia de las reglas de lluvia."""
    plt.axhline(y=0.75, color="red", linestyle="--", label="Lluvia (I ≥ 0.75)")
    plt.axhline(y=0.60, color="orange", linestyle="--", label="Lluvia probable (I ≥ 0.60)")
    plt.axhline(y=0.40, color="gray", linestyle="--", label="Baja posibilidad (I ≥ 0.40)")


def grafica_indice(filas, titulo, archivo):
    """Índice atmosférico por hora para un modelo."""
    plt.figure(figsize=(10, 5))

    plt.plot(
        _horas(filas),
        [f["indice"] for f in filas],
        marker="o",
        label="Índice I",
    )
    _umbrales()

    plt.xlabel("Hora")
    plt.ylabel("Índice atmosférico I")
    plt.title(titulo)
    plt.grid(True)
    plt.legend()

    _guardar(archivo)


def grafica_comparacion(original, ajustado, archivo):
    """Compara el índice del modelo original contra el ajustado."""
    plt.figure(figsize=(10, 5))

    plt.plot(
        _horas(original),
        [f["indice"] for f in original],
        marker="o",
        label="Modelo original",
    )
    plt.plot(
        _horas(ajustado),
        [f["indice"] for f in ajustado],
        marker="s",
        label="Modelo ajustado",
    )
    plt.axhline(y=0.75, color="red", linestyle="--", label="Lluvia (I ≥ 0.75)")

    plt.xlabel("Hora")
    plt.ylabel("Índice atmosférico I")
    plt.title("Comparación del índice atmosférico por hora")
    plt.grid(True)
    plt.legend()

    _guardar(archivo)


def grafica_variables(filas, archivo):
    """Evolución de las variables H, N y Tf durante las 24 horas."""
    plt.figure(figsize=(10, 5))

    plt.plot(_horas(filas), [f["H"] for f in filas], marker="o", label="Humedad (H)")
    plt.plot(_horas(filas), [f["N"] for f in filas], marker="s", label="Nubosidad (N)")
    plt.plot(_horas(filas), [f["Tf"] for f in filas], marker="^", label="Factor temperatura (Tf)")

    plt.xlabel("Hora")
    plt.ylabel("Valor normalizado")
    plt.title("Variables del modelo por hora")
    plt.grid(True)
    plt.legend()

    _guardar(archivo)


def generar(original, ajustado):
    """Genera todas las gráficas de la práctica."""
    grafica_indice(
        original,
        "Modelo de probabilidad de lluvia (original: 0.50H + 0.30N + 0.20Tf)",
        "indice_original.png",
    )
    grafica_indice(
        ajustado,
        "Modelo de probabilidad de lluvia (ajustado: 0.40H + 0.35N + 0.25Tf)",
        "indice_ajustado.png",
    )
    grafica_comparacion(original, ajustado, "indice_comparacion.png")
    grafica_variables(original, "variables_hora.png")
    return sorted(os.listdir(SALIDA))
