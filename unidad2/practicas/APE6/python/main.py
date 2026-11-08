"""
APE 6 - Main experiment driver (Python implementation).

Generates 10,000 LCG values per configuration and runs Chi-square and
Kolmogorov-Smirnov uniformity tests. Saves JSON stats (same schema as Java)
for cross-language comparison parity.

Usage: python3 main.py [--outdir ../results]
"""

import argparse
import csv
import json
import pathlib

from lcg import CONFIGS, generate
from pruebas import chi_cuadrado, kolmogorov_smirnov

N = 10_000
K = 10


def write_csv(path: pathlib.Path, rows: list[list]) -> None:
    """Write rows to a CSV file, failing loudly if the path is not writable."""
    try:
        with open(path, "w", newline="") as fh:
            csv.writer(fh).writerows(rows)
    except OSError as exc:
        raise SystemExit(f"cannot write {path}: {exc}") from exc


def write_json(path: pathlib.Path, data: dict) -> None:
    try:
        with open(path, "w") as fh:
            json.dump(data, fh, indent=2)
    except OSError as exc:
        raise SystemExit(f"cannot write {path}: {exc}") from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="../results")
    args = parser.parse_args()
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    all_stats = {}
    for cfg in CONFIGS:
        state, values = generate(cfg, N)

        chi = chi_cuadrado(values, k=K)
        ks = kolmogorov_smirnov(values)

        stats = {
            "n": N,
            "k": K,
            "params": {"m": cfg.m, "a": cfg.a, "c": cfg.c, "seed": cfg.seed,
                       "quality": cfg.quality},
            "final_state": state,
            "chi2": {"stat": chi["stat"], "df": chi["df"], "p": chi["p"],
                     "reject": chi["reject"]},
            "ks": {"stat": ks["stat"], "p": ks["p"], "reject": ks["reject"]},
            "observed": chi["observed"],
        }
        all_stats[cfg.name] = stats

        print(f"== {cfg.name} (m={cfg.m}, a={cfg.a}, c={cfg.c}, X0={cfg.seed}) ==")
        print(f"   X_10000 final state = {state}")
        print(f"   first 5 values      = {values[:5]}")
        print(f"   mean = {sum(values) / N:.6f}  min = {min(values):.6f}  "
              f"max = {max(values):.6f}")
        print(f"   Chi2: stat={chi['stat']:.4f} df={chi['df']} p={chi['p']:.6f} "
              f"-> {'REJECT H0' if chi['reject'] else 'DO NOT REJECT H0'}")
        print(f"   KS:   D={ks['stat']:.6f} p={ks['p']:.6f} "
              f"-> {'REJECT H0' if ks['reject'] else 'DO NOT REJECT H0'}")

        # observed frequencies per bin
        rows: list[list] = [["bin", "low", "high", "observed", "expected"]]
        for i, o in enumerate(chi["observed"]):
            rows.append([i + 1, i / K, (i + 1) / K, o, N / K])
        write_csv(outdir / f"observed_{cfg.name}_python.csv", rows)

        # first sample of values for cross-language sequence parity check
        rows = [["index", "un_int", "un_float"]]  # type: list[list]
        x = cfg.seed % cfg.m
        for i in range(200):
            x = (cfg.a * x + cfg.c) % cfg.m
            rows.append([i + 1, x, repr(x / cfg.m)])
        write_csv(outdir / f"parity_{cfg.name}_python.csv", rows)

    write_json(outdir / "stats_python.json", all_stats)
    print(f"\nStats saved to {outdir / 'stats_python.json'}")


if __name__ == "__main__":
    main()
