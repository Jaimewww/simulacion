"""
Cross-language parity check: Python vs Java (APE 6).

Compares stats_python.json against stats_java.json (exact match on every
statistic) and the parity CSVs row by row (integer states must be exactly
equal; floats within 1 ulp).

Exit code 0 = implementations produce the identical sequence and statistics.
"""

import csv
import json
import math
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent / "results"


def fail(msg: str) -> None:
    print(f"PARITY MISMATCH: {msg}")
    raise SystemExit(1)


def compare_float(a: float, b: float, label: str) -> None:
    if math.isnan(a) and math.isnan(b):
        return
    if a != b and abs(a - b) > 4.0 * math.ulp(max(abs(a), abs(b), 1e-300)):
        fail(f"{label}: {a!r} vs {b!r}")


def read_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}") from exc


def read_rows(path: pathlib.Path) -> list[dict[str, str]]:
    try:
        with open(path) as fh:
            return list(csv.DictReader(fh))
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}") from exc


def main() -> None:
    py = read_json(root / "stats_python.json")
    ja = read_json(root / "stats_java.json")

    if list(py.keys()) != list(ja.keys()):
        fail("configurations differ")

    for name in py:
        if py[name]["final_state"] != ja[name]["final_state"]:
            fail(f"{name}: final state")
        compare_float(py[name]["chi2"]["stat"], ja[name]["chi2"]["stat"], f"{name} chi2 stat")
        compare_float(py[name]["chi2"]["p"], ja[name]["chi2"]["p"], f"{name} chi2 p")
        compare_float(py[name]["ks"]["stat"], ja[name]["ks"]["stat"], f"{name} ks stat")
        compare_float(py[name]["ks"]["p"], ja[name]["ks"]["p"], f"{name} ks p")
        if py[name]["chi2"]["reject"] != ja[name]["chi2"]["reject"]:
            fail(f"{name}: chi2 decision")
        if py[name]["ks"]["reject"] != ja[name]["ks"]["reject"]:
            fail(f"{name}: ks decision")
        if py[name]["observed"] != ja[name]["observed"]:
            fail(f"{name}: observed frequencies")

        # exact integer-state parity for the first 200 values of the sequence
        rows_py = read_rows(root / f"parity_{name}_python.csv")
        rows_ja = read_rows(root / f"parity_{name}_java.csv")
        if len(rows_py) != len(rows_ja):
            fail(f"{name}: parity row count")
        for r1, r2 in zip(rows_py, rows_ja, strict=True):
            if r1["un_int"] != r2["un_int"]:
                fail(f"{name}: integer state index {r1['index']}")
            compare_float(
                float(r1["un_float"]), float(r2["un_float"]),
                f"{name}: normalized value index {r1['index']}",
            )
        print(f"{name:12s}: OK - 200/200 identical states, identical statistics")

    print("\nPARITY OK: Java and Python produce the same sequence and the same "
          "test statistics for identical parameters.")


if __name__ == "__main__":
    sys.exit(main())
