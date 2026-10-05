"""Core math for the atmospheric-rainfall model."""

import models.datasets as datasets


def tf_dict(temp, tabla_tf):
    """Return the temperature factor for a temperature in Celsius.

    Uses the nearest 2 °C step and clamps to the table's range.
    """
    if temp <= 10:
        return tabla_tf[10]
    if temp >= 28:
        return tabla_tf[28]
    temp_par = round(temp / 2) * 2
    return tabla_tf[temp_par]


def indice(H, N, Tf, coeficientes=None):
    """Atmospheric index I = aH + bN + cTf.

    Defaults to the original guide coefficients (0.5, 0.3, 0.2).
    """
    if coeficientes is None:
        coeficientes = datasets.COEFICIENTES_ORIGINAL
    return (
        (coeficientes["H"] * H)
        + (coeficientes["N"] * N)
        + (coeficientes["Tf"] * Tf)
    )


def I(H, N, Tf):
    """Backwards-compatible alias for the original base code."""
    return indice(H, N, Tf)


def clasificar(valor):
    """Map an index value to its rain state following the guide rules."""
    for limite, estado in datasets.REGLAS_LLUVIA:
        if limite is None or valor < limite:
            return estado
    return datasets.REGLAS_LLUVIA[-1][1]
