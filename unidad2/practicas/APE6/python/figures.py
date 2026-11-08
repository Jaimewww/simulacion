"""
APE 6 - Figures for the technical report.

Generates, per LCG configuration:
  1. Empirical CDF vs theoretical U(0,1) CDF (Kolmogorov-Smirnov view).
  2. Lag-1 scatter (U_n, U_{n+1}) - lattice structure of good vs bad generators.
  3. Observed vs expected bin frequencies (Chi-square view).

Saves PNG (report) and PDF (LaTeX) under ../figures/.
"""

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from lcg import CONFIGS, generate

# headless backend: figure generation must not require a display
plt.switch_backend("Agg")

N = 10_000
K = 10

OUT = pathlib.Path(__file__).resolve().parent.parent / "figures"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sequences = {}
    for cfg in CONFIGS:
        _, values = generate(cfg, N)
        sequences[cfg.name] = np.array(values)

        u = np.sort(sequences[cfg.name])

        # 1. Empirical CDF vs theoretical CDF
        fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=150)
        ax.step(u, np.arange(1, N + 1) / N, where="post", label="Empirical CDF $F_N(x)$")
        ax.plot([0, 1], [0, 1], "r--", lw=1.2, label="Theoretical $F(x)=x$")
        ax.set_xlabel("x")
        ax.set_ylabel("Cumulative probability")
        ax.set_title(f"Kolmogorov-Smirnov: {cfg.name} (n = {N})")
        ax.legend(loc="best")
        fig.tight_layout()
        for fmt in ("png", "pdf"):
            fig.savefig(OUT / f"ks_{cfg.name}.{fmt}")
        plt.close(fig)

        # 2. Lag-1 scatter
        fig, ax = plt.subplots(figsize=(4.6, 4.6), dpi=150)
        v = sequences[cfg.name]
        ax.plot(v[:-1], v[1:], ".", ms=1.5, alpha=0.25, rasterized=True)
        ax.set_xlabel(r"$U_n$")
        ax.set_ylabel(r"$U_{n+1}$")
        ax.set_title(f"Lag-1 pairs: {cfg.name}")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        fig.tight_layout()
        for fmt in ("png", "pdf"):
            fig.savefig(OUT / f"lag1_{cfg.name}.{fmt}")
        plt.close(fig)

        # 3. Observed vs expected frequencies
        observed, _ = np.histogram(sequences[cfg.name], bins=K, range=(0, 1))
        expected = np.full(K, N / K)
        idx = np.arange(1, K + 1)
        fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=150)
        w = 0.38
        ax.bar(idx - w / 2, observed, w, label="Observed")
        ax.bar(idx + w / 2, expected, w, label="Expected", color="tab:red", alpha=0.7)
        ax.set_xlabel("Bin")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Chi-square bins: {cfg.name} (k = {K}, E = {N / K:.0f})")
        ax.set_xticks(idx)
        ax.legend(loc="best")
        fig.tight_layout()
        for fmt in ("png", "pdf"):
            fig.savefig(OUT / f"chi2_{cfg.name}.{fmt}")
        plt.close(fig)

        print(f"figures for {cfg.name}: OK")

    # 4. Side-by-side lag-1 comparison good vs bad
    good = [c.name for c in CONFIGS if c.quality == "good"]
    bad = [c.name for c in CONFIGS if c.quality == "bad"][0]
    fig, axes = plt.subplots(1, len(good) + 1, figsize=(4.2 * (len(good) + 1), 4.4), dpi=150)
    for ax, name in zip(axes, good + [bad], strict=True):
        v = sequences[name]
        ax.plot(v[:-1], v[1:], ".", ms=1.5, alpha=0.25, rasterized=True)
        ax.set_title(name)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    fig.suptitle(r"Lattice structure of $(U_n, U_{n+1})$: good vs bad parameter sets")
    fig.tight_layout()
    for fmt in ("png", "pdf"):
        fig.savefig(OUT / f"lag1_comparison.{fmt}")
    plt.close(fig)
    print("comparison figure: OK")


if __name__ == "__main__":
    main()
