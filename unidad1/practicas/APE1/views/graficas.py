"""Generate the practice charts and save them as PNG files."""

import os

import matplotlib

matplotlib.use("Agg")  # headless: render straight to file, no window needed
import matplotlib.pyplot as plt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "dist")


def _horas(filas):
    return [f["hora"] for f in filas]


def _asegurar_salida():
    os.makedirs(SALIDA, exist_ok=True)


def grafica_indice(corridas, titulo, archivo):
    """Line chart of the index over time for one or more model runs."""
    _asegurar_salida()
    plt.figure(figsize=(9, 5))
    for etiqueta, filas in corridas:
        plt.plot(_horas(filas), [f["indice"] for f in filas], marker="o", label=etiqueta)
    plt.axhline(0.40, color="gray", linestyle="--", linewidth=1, label="Limite 0.40")
    plt.axhline(0.60, color="orange", linestyle="--", linewidth=1, label="Limite 0.60")
    plt.axhline(0.75, color="red", linestyle="--", linewidth=1, label="Limite 0.75")
    plt.title(titulo)
    plt.xlabel("Hora")
    plt.ylabel("Indice atmosferico I")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SALIDA, archivo), dpi=150)
    plt.close()


def grafica_variables(filas, archivo):
    """Line chart of the normalized variables H, N and Tf over time."""
    _asegurar_salida()
    plt.figure(figsize=(9, 5))
    plt.plot(_horas(filas), [f["H"] for f in filas], marker="o", label="Humedad (H)")
    plt.plot(_horas(filas), [f["N"] for f in filas], marker="s", label="Nubosidad (N)")
    plt.plot(_horas(filas), [f["Tf"] for f in filas], marker="^", label="Factor temp. (Tf)")
    plt.title("Variables del modelo por hora")
    plt.xlabel("Hora")
    plt.ylabel("Valor normalizado")
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SALIDA, archivo), dpi=150)
    plt.close()


def grafica_barras(filas, titulo, archivo):
    """Bar chart of the index per hour, useful to spot the rainy window."""
    _asegurar_salida()
    plt.figure(figsize=(9, 5))
    plt.bar(_horas(filas), [f["indice"] for f in filas], color="#3b82f6", alpha=0.85)
    plt.axhline(0.75, color="red", linestyle="--", linewidth=1, label="Lluvia (>= 0.75)")
    plt.axhline(0.60, color="orange", linestyle="--", linewidth=1, label="Probable (>= 0.60)")
    plt.title(titulo)
    plt.xlabel("Hora")
    plt.ylabel("Indice atmosferico I")
    plt.ylim(0, 1)
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SALIDA, archivo), dpi=150)
    plt.close()


def generar(original, ajustado):
    """Produce every chart for both model runs and return their paths."""
    grafica_indice(
        [("Modelo original", original)],
        "Indice atmosferico - modelo original (0.50H + 0.30N + 0.20Tf)",
        "indice_original.png",
    )
    grafica_indice(
        [("Modelo ajustado", ajustado)],
        "Indice atmosferico - modelo ajustado (0.40H + 0.35N + 0.25Tf)",
        "indice_ajustado.png",
    )
    grafica_indice(
        [("Original", original), ("Ajustado", ajustado)],
        "Comparacion del indice atmosferico por hora",
        "indice_comparacion.png",
    )
    grafica_variables(original, "variables_hora.png")
    grafica_barras(original, "Indice por hora - modelo original", "barras_original.png")
    grafica_barras(ajustado, "Indice por hora - modelo ajustado", "barras_ajustado.png")
    return sorted(os.listdir(SALIDA))
