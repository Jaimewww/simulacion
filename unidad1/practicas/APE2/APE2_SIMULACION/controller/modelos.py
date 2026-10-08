"""The four population models and the comparison/metric helpers (APE2).

Every model receives the initial population ``p0`` and returns one value per
period so that all the series can be compared on the same integer grid.
"""

import numpy as np


def determinista(p0, r, t):
    """Deterministic exponential model ``P(t) = P0 * exp(r * t)``.

    ``t`` may be a scalar or any array-like time grid, which allows both the
    smooth curve (fine grid) and the evaluation on the integer periods.
    """
    t = np.asarray(t, dtype=float)
    return p0 * np.exp(r * t)


def determinista_periodos(p0, r, periodos):
    """Deterministic model evaluated on the integer period grid ``0..periodos``."""
    return determinista(p0, r, np.arange(periodos + 1, dtype=float))


def discreto(p0, r, periodos):
    """Discrete model: ``P[k+1] = P[k] + r * P[k]`` in fixed intervals."""
    valores = np.empty(periodos + 1, dtype=float)
    valores[0] = p0
    for k in range(periodos):
        valores[k + 1] = valores[k] + r * valores[k]
    return valores


def estocastico(p0, r, sigma, periodos, generador):
    """Stochastic model: discrete growth plus normal noise ``Normal(0, sigma)``.

    Negative populations are clipped to zero, as stated by the guide.
    """
    valores = np.empty(periodos + 1, dtype=float)
    valores[0] = p0
    for k in range(periodos):
        ruido = generador.normal(0.0, sigma)
        nueva_poblacion = valores[k] + r * valores[k] + ruido
        if nueva_poblacion < 0:
            nueva_poblacion = 0.0
        valores[k + 1] = nueva_poblacion
    return valores


def continuo_euler(p0, r, dt, tiempo):
    """Continuous model integrated with Euler over ``[0, tiempo]``, step ``dt``.

    Returns ``(t, valores)`` with ``int(tiempo / dt) + 1`` samples.
    """
    pasos = int(tiempo / dt)
    t = np.arange(pasos + 1, dtype=float) * dt
    valores = np.empty(pasos + 1, dtype=float)
    valores[0] = p0
    for k in range(pasos):
        valores[k + 1] = valores[k] + dt * r * valores[k]
    return t, valores


def euler_periodos(p0, r, dt, periodos):
    """Euler solution sampled on the integer period grid for a fair comparison."""
    t, valores = continuo_euler(p0, r, dt, float(periodos))
    periodos_t = np.arange(periodos + 1, dtype=float)
    return np.interp(periodos_t, t, valores)


def estimar_r(observado):
    """Estimate the growth rate from the observed series.

    Returns the discrete rate (arithmetic mean of the period-over-period
    ratios minus one), the continuous rate (least-squares slope of ``ln(P)``
    against the period index) and the mean growth factor. Non-positive values
    are rejected because both the ratios and the logarithm would be undefined.
    """
    observado = np.asarray(observado, dtype=float)
    if observado.size < 2:
        raise ValueError("Se necesitan al menos dos valores observados para estimar r")
    if np.any(observado <= 0):
        raise ValueError("La serie observada debe ser estrictamente positiva para estimar r")

    ratios = observado[1:] / observado[:-1]
    factor_medio = float(np.mean(ratios))
    periodos = np.arange(observado.size, dtype=float)
    pendiente = float(np.polyfit(periodos, np.log(observado), 1)[0])
    return {
        "discreto": factor_medio - 1.0,
        "continuo": pendiente,
        "factor_medio": factor_medio,
    }


def comparar(p0, r, sigma, dt, periodos, observado, seed):
    """Return the four model series and the observed data on periods ``0..periodos``."""
    generador = np.random.default_rng(seed)
    observado = np.asarray(observado, dtype=float)[: periodos + 1]
    return {
        "periodos": np.arange(periodos + 1),
        "observado": observado,
        "deterministico": determinista_periodos(p0, r, periodos),
        "discreto": discreto(p0, r, periodos),
        "estocastico": estocastico(p0, r, sigma, periodos, generador),
        "euler": euler_periodos(p0, r, dt, periodos),
    }


def error_cuadratico_medio(serie, observado):
    """Root mean square error between a model series and the observed data."""
    serie = np.asarray(serie, dtype=float)
    observado = np.asarray(observado, dtype=float)
    n = min(serie.size, observado.size)
    return float(np.sqrt(np.mean((serie[:n] - observado[:n]) ** 2)))


def metricas(resultados, r):
    """Final value and RMSE per model, plus the discrete growth factor ``1 + r``."""
    observado = resultados["observado"]
    nombres = ("deterministico", "discreto", "estocastico", "euler")
    resumen = {}
    for nombre in nombres:
        serie = resultados[nombre]
        resumen[nombre] = {
            "final": float(serie[-1]),
            "rmse": error_cuadratico_medio(serie, observado),
        }
    return {"modelos": resumen, "factor_crecimiento": 1.0 + r}
