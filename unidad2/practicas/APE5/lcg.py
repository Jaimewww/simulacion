#!/usr/bin/env python3
"""LCG (Linear Congruential Generator) - Practica 05, Simulacion U2.

Implementa el generador congruencial lineal:
    X(n+1) = (a * X(n) + c) mod m
    U(n)   = X(n) / m

Parametros pedidos por la guia:
    a = 1664525, c = 1013904223, m = 2^32, semilla = 12345

Uso:
    python3 lcg.py                 # semilla 12345 (por defecto)
    python3 lcg.py 54321           # otra semilla (experimento de comparacion)
"""

import csv
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Parametros del generador
# ------------------------------------------------------------------
A = 1664525
C = 1013904223
M = 2**32
SEED = 12345
N = 10_000


class LCG:
    """Generador congruencial lineal: X(n+1) = (a * X(n) + c) mod m."""

    def __init__(self, a: int = A, c: int = C, m: int = M, seed: int = SEED):
        self.a, self.c, self.m = a, c, m
        self.state = seed % m  # normaliza la semilla al rango [0, m)

    def next_x(self) -> int:
        """Devuelve el siguiente X entero crudo."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def next_u(self) -> float:
        """Devuelve el siguiente valor normalizado U = X / m en [0, 1)."""
        return self.next_x() / self.m

    def generate(self, n: int) -> tuple[list[int], list[float]]:
        """Genera n pares (X, U). Excluye X0 = semilla, como pide el metodo."""
        xs = [self.next_x() for _ in range(n)]
        us = [x / self.m for x in xs]
        return xs, us


def period_demo(seed: int, a: int, c: int, m: int) -> int | None:
    """Calcula el periodo empiricamente con parametros pequenos.

    Con m = 2^32 seria monstruoso iterar hasta la repeticion de la semilla
    (periodo teorico = m con los parametros de Hull-Dobell: c impar y
    a = 1 mod 4), por eso esta funcion usa un m pequenio solo para verlo.

    Importante: si los parametros no cumplen Hull-Dobell, el estado puede
    entrar en un ciclo que NO contiene a la semilla y nunca regresar a x0;
    por eso se acota con un limite de m*4 iteraciones (devuelve None).
    """
    g = LCG(a, c, m, seed)
    x0 = seed % m
    for count in range(1, m * 4 + 1):
        x = g.next_x()
        if x == x0:
            return count
    return None  # nunca regreso a la semilla: ciclo incompleto o fuera de ciclo


def save_csv(xs, us, path: Path, rows: int = 20) -> None:
    """Guarda las primeras `rows` observaciones (formato tabla comparativa)."""
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "X(n)", "U(n)"])
        for i in range(rows):
            w.writerow([i + 1, xs[i], f"{us[i]:.10f}"])


def save_full_csv(xs, us, path: Path) -> None:
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["index", "X", "U"])
        for i, (x, u) in enumerate(zip(xs, us, strict=True)):
            w.writerow([i, x, f"{u:.10f}"])


def make_plots(xs, us, seed, outdir: Path) -> None:
    tag = f"seed{seed}"
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.suptitle(
        f"LCG  a={A}  c={C}  m=2^32  semilla={seed}", fontsize=12
    )

    # 1) Evolucion de U(n)
    ax = axes[0][0]
    ax.plot(us[:500], lw=0.8)
    ax.set_title("U(n) - primeras 500 iteraciones")
    ax.set_xlabel("n")
    ax.set_ylabel("U(n)")

    # 2) Dispersión U(n) vs U(n+1) -> revela correlaciones seriales
    ax = axes[0][1]
    ax.scatter(us[:-1], us[1:], s=1, alpha=0.3, color="crimson")
    ax.set_title("U(n) vs U(n+1) - correlacion serial")
    ax.set_xlabel("U(n)")
    ax.set_ylabel("U(n+1)")

    # 3) Comparacion con una distribucion uniforme ideal
    ax = axes[1][0]
    bins = math.isqrt(N)
    ax.hist(us, bins=bins, density=True, color="steelblue", edgecolor="white")
    ax.axhline(1.0, color="red", ls="--", lw=1, label="Uniforme ideal (densidad 1)")
    ax.set_title(f"Histograma de U ({bins} bins)")
    ax.set_xlabel("U")
    ax.set_ylabel("frecuencia")
    ax.legend()

    # 4) Media y desviacion teorica vs observada
    ax = axes[1][1]
    ax.axis("off")
    mean_u = sum(us) / len(us)
    var_u = sum((u - mean_u) ** 2 for u in us) / (len(us) - 1)
    sd_u = math.sqrt(var_u)
    ax.text(
        0.02,
        0.85,
        f"Datos generados.......... N = {N}\n"
        f"Media de U............... E[U] = {mean_u:.6f}\n"
        f"Media teorica............ E[U] = 0.500000\n"
        f"Desv. estandar........... S    = {sd_u:.6f}\n"
        f"Desv. teorica U(0,1)..... 1/sqrt(12) = {math.sqrt(1/12):.6f}\n"
        f"Min = {min(us):.5f}   Max = {max(us):.5f}",
        family="monospace",
        fontsize=10,
        verticalalignment="top",
        bbox={"boxstyle": "round", "facecolor": "lavender", "alpha": 0.8},
    )
    ax.set_title("Resumen estadistico")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    out = outdir / f"lcg_{tag}.png"  # los 4 subplots se guardan en una sola figura
    fig.savefig(out, dpi=150)
    print(f"[plot] {out}")


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    outdir = Path(__file__).resolve().parent / "resultados"
    outdir.mkdir(exist_ok=True)

    g = LCG(seed=seed)
    xs, us = g.generate(N)

    short = outdir / f"python_primeras20_{seed}.csv"
    full = outdir / f"python_10000_{seed}.csv"
    save_csv(xs, us, short)
    save_full_csv(xs, us, full)
    make_plots(xs, us, seed, outdir)

    print(f"Parametros: a={A}  c={C}  m={M} (2^32)   semilla={seed}")
    print(f"Generados {N} valores.")
    print("\nPrimeras 10 observaciones:")
    for i in range(10):
        print(f"  X[{i}] = {xs[i]:>10}   U[{i}] = {us[i]:.10f}")

    # Analisis de periodo: demostracion empirica con m pequeno.
    print("\nPeriodo (demostracion con m pequenio, m=2^32 no es iterable):")
    for (a2, c2, m2) in [(5, 3, 16), (5, 2, 16), (4, 3, 16)]:
        p = period_demo(seed, a2, c2, m2)
        cumple = (c2 % 2 == 1) and ((a2 - 1) % 4 == 0)
        sonido = "cumple Hull-Dobell" if cumple else "NO cumple Hull-Dobell"
        if p is None:
            print(f"  a={a2:>2} c={c2:>2} m={m2:>2}  -> el estado nunca vuelve a la "
                  f"semilla: ciclo incompleto ({sonido})")
        else:
            print(f"  a={a2:>2} c={c2:>2} m={m2:>2}  -> periodo = {p}  ({sonido})")
    print(
        "  Teoria (Hull-Dobell): con c impar y a≡1 mod 4 y m=2^k, "
        "periodo completo = m. Con m=2^32 el periodo teorico es 2^32."
    )
    # Verificación empírica directa de Hull-Dobell con los parámetros reales:
    completo = C % 2 == 1 and (A - 1) % 4 == 0  # c coprimo con 2^k y a≡1 (mod 4)
    print(f"  c = {C} es {'impar' if C % 2 == 1 else 'par'} (coprimo con m); "
          f"a-1 = {A-1} ≡ {(A-1) % 4} (mod 4) → a ≡ 1 (mod 4): "
          f"{'✓ SI cumple Hull-Dobell → periodo completo = m = 2^32'
               if completo else '✗ NO cumple Hull-Dobell → periodo < m'}")


if __name__ == "__main__":
    main()
