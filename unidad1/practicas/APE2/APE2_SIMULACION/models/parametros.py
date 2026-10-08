"""Input data and default parameters for the population simulation (APE2).

The observed series comes from the practice guide. Its first value is the
initial population used by every model, and it is also the reference used to
compute the RMSE of each model.
"""

import numpy as np

# Observed reference series from the guide (7 points -> 6 periods).
datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]

# Default parameters (overridable from the CLI).
P0 = datos[0]
R = 0.08
SIGMA = 40.0
DT = 0.1
PERIODOS = len(datos) - 1
SEED = 42


def rng(seed=SEED):
    """Return a seeded numpy random generator so runs are reproducible."""
    return np.random.default_rng(seed)
