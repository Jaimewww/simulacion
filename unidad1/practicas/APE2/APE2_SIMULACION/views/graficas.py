"""Charts for the population simulation practice (APE2, matplotlib).

All figures are saved to ``dist/`` next to the package, so the project works
from any current working directory. Labels are in Spanish (what the student
hands in); code and comments stay in English.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import controller.modelos as modelos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "dist")


def _asegurar_salida():
    """Create the dist/ output directory, reporting a clear error if it fails."""
    try:
        os.makedirs(SALIDA, exist_ok=True)
    except OSError as error:
        raise RuntimeError(f"No se pudo crear el directorio de salida {SALIDA}") from error


def _guardar(fig, archivo, mostrar):
    """Save a figure to dist/ at dpi=150, optionally show it, then close it."""
    _asegurar_salida()
    fig.savefig(os.path.join(SALIDA, archivo), dpi=150)
    if mostrar:
        plt.show()
    plt.close(fig)
    return archivo


def grafica_comparacion(resultados, mostrar):
    """The four models plus the observed series over periods 0..6."""
    fig, ax = plt.subplots(figsize=(10, 6))
    periodos = resultados["periodos"]

    ax.plot(periodos, resultados["observado"], "ko-", label="Observado")
    ax.plot(periodos, resultados["deterministico"], "o-", label="Deterministico")
    ax.plot(periodos, resultados["discreto"], "s-", label="Discreto")
    ax.plot(periodos, resultados["estocastico"], "^-", label="Estocastico")
    ax.plot(periodos, resultados["euler"], "d-", label="Euler (continuo)")

    ax.set_xlabel("Tiempo (periodos)")
    ax.set_ylabel("Población")
    ax.set_title("Comparación de los cuatro modelos de población")
    ax.grid(True)
    ax.legend()
    return _guardar(fig, "comparacion_modelos.png", mostrar)


def grafica_crecimiento_decrecimiento(p0, periodos, mostrar):
    """Growth vs decay: deterministic and discrete for r = +0.12 and r = -0.12."""
    fig, ax = plt.subplots(figsize=(10, 6))
    t = np.arange(periodos + 1, dtype=float)

    for r in (0.12, -0.12):
        etiqueta = "crecimiento" if r > 0 else "decrecimiento"
        ax.plot(
            t,
            modelos.determinista_periodos(p0, r, periodos),
            "o-",
            label=f"Deterministico r = {r:+.2f} ({etiqueta})",
        )
        ax.plot(
            t,
            modelos.discreto(p0, r, periodos),
            "s--",
            label=f"Discreto r = {r:+.2f} ({etiqueta})",
        )

    ax.set_xlabel("Tiempo (periodos)")
    ax.set_ylabel("Población")
    ax.set_title("Crecimiento y decrecimiento según la tasa r")
    ax.grid(True)
    ax.legend()
    return _guardar(fig, "crecimiento_decrecimiento.png", mostrar)


def grafica_influencia_r(p0, periodos, mostrar):
    """Deterministic model for several growth rates on a fine time grid."""
    fig, ax = plt.subplots(figsize=(10, 6))
    t = np.linspace(0.0, float(periodos), 200)

    for r in (-0.10, 0.0, 0.05, 0.10, 0.15):
        ax.plot(t, modelos.determinista(p0, r, t), label=f"r = {r:.2f}")

    ax.set_xlabel("Tiempo (periodos)")
    ax.set_ylabel("Población")
    ax.set_title("Influencia de la tasa de crecimiento r (modelo deterministico)")
    ax.grid(True)
    ax.legend()
    return _guardar(fig, "influencia_r.png", mostrar)


def grafica_ajuste(p0, observado, periodos, mostrar):
    """Fit both growth rates to the observed series and compare them with r = 0.08.

    The rates come from :func:`controller.modelos.estimar_r`: the discrete rate
    drives the discrete model and the continuous rate drives the deterministic
    one. The guide's default rate is drawn as a dashed reference line.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    t = np.arange(periodos + 1, dtype=float)
    observado = np.asarray(observado, dtype=float)[: periodos + 1]

    estimado = modelos.estimar_r(observado)
    r_est = estimado["discreto"]
    r_cont = estimado["continuo"]

    ax.plot(t, observado, "ko-", label="Observado")
    ax.plot(
        t,
        modelos.discreto(p0, r_est, periodos),
        "s-",
        label=f"Discreto ajustado (r = {r_est:.4f})",
    )
    ax.plot(
        t,
        modelos.determinista_periodos(p0, r_cont, periodos),
        "^-",
        label=f"Deterministico ajustado (r = {r_cont:.4f})",
    )
    ax.plot(
        t,
        modelos.determinista_periodos(p0, 0.08, periodos),
        "d--",
        label="Deterministico por defecto (r = 0.08)",
    )

    ax.set_xlabel("Tiempo (periodos)")
    ax.set_ylabel("Población")
    ax.set_title("Ajuste de la tasa r a la serie observada")
    ax.grid(True)
    ax.legend()
    return _guardar(fig, "ajuste_r.png", mostrar)


def grafica_efecto_sigma(p0, r, periodos, seed, mostrar, corridas=30):
    """Stochastic model for several sigma values: mean curve and +-1 std band."""
    fig, ax = plt.subplots(figsize=(10, 6))
    generador = np.random.default_rng(seed + 1)
    t = np.arange(periodos + 1)

    for sigma in (0, 20, 50, 100):
        simulaciones = np.array(
            [modelos.estocastico(p0, r, sigma, periodos, generador) for _ in range(corridas)]
        )
        media = simulaciones.mean(axis=0)
        desviacion = simulaciones.std(axis=0)
        (linea,) = ax.plot(t, media, "o-", label=f"sigma = {sigma} (media de {corridas} corridas)")
        ax.fill_between(
            t,
            media - desviacion,
            media + desviacion,
            alpha=0.2,
            color=linea.get_color(),
            label=f"sigma = {sigma} (+-1 desv. est.)",
        )

    ax.set_xlabel("Tiempo (periodos)")
    ax.set_ylabel("Población")
    ax.set_title("Efecto del ruido sigma en el modelo estocastico")
    ax.grid(True)
    ax.legend(fontsize="small")
    return _guardar(fig, "efecto_sigma.png", mostrar)


def grafica_efecto_dt(p0, r, periodos, mostrar):
    """Continuous Euler vs the exact exponential for several step sizes dt."""
    fig, ax = plt.subplots(figsize=(10, 6))
    t_fino = np.linspace(0.0, float(periodos), 200)
    exacto = modelos.determinista(p0, r, t_fino)
    ax.plot(t_fino, exacto, "k--", linewidth=2, label="Exacto P0 * exp(r*t)")

    for dt in (1.0, 0.5, 0.1, 0.01):
        t, valores = modelos.continuo_euler(p0, r, dt, float(periodos))
        error = float(np.sqrt(np.mean((valores - modelos.determinista(p0, r, t)) ** 2)))
        ax.plot(t, valores, marker=".", label=f"Euler dt = {dt} (RMSE = {error:.2f})")

    ax.set_xlabel("Tiempo (periodos)")
    ax.set_ylabel("Población")
    ax.set_title("Efecto del paso dt: Euler vs exponencial exacta")
    ax.grid(True)
    ax.legend()
    return _guardar(fig, "efecto_dt.png", mostrar)


def escribir_csv(resultados):
    """Write the comparison table to dist/resultados.csv with pandas."""
    _asegurar_salida()
    tabla = pd.DataFrame(
        {
            "periodo": resultados["periodos"],
            "observado": resultados["observado"],
            "deterministico": resultados["deterministico"],
            "discreto": resultados["discreto"],
            "estocastico": resultados["estocastico"],
            "euler": resultados["euler"],
        }
    )
    ruta = os.path.join(SALIDA, "resultados.csv")
    tabla.to_csv(ruta, index=False)
    return "resultados.csv"


def generar(resultados, p0, r, sigma, dt, periodos, seed, mostrar=True):
    """Generate every chart and the CSV; return the list of generated files."""
    archivos = [
        grafica_comparacion(resultados, mostrar),
        grafica_crecimiento_decrecimiento(p0, periodos, mostrar),
        grafica_influencia_r(p0, periodos, mostrar),
        grafica_efecto_sigma(p0, r, periodos, seed, mostrar),
        grafica_efecto_dt(p0, r, periodos, mostrar),
        grafica_ajuste(p0, resultados["observado"], periodos, mostrar),
        escribir_csv(resultados),
    ]
    return archivos
