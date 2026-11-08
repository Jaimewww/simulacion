"""
Statistical tests for pseudo-random numbers - APE 6, Simulation.

- Chi-square goodness-of-fit test (uniformity in k bins of [0, 1]).
- Kolmogorov-Smirnov test (empirical CDF vs theoretical U(0,1) CDF).

p-values are computed from scratch (no scipy):
- Chi-square: regularized upper incomplete gamma function Q(df/2, x/2).
- KS: asymptotic Kolmogorov distribution Q_KS(lambda) = 2*sum (-1)^(k-1) e^(-2 k^2 lambda^2).

Same algorithms are used in the Java implementation so results are comparable.
"""

import math
from collections.abc import Sequence

ALPHA = 0.05


# ---------------------------------------------------------------------------
# Incomplete gamma (Lentz continued fraction + series, Numerical Recipes)
# ---------------------------------------------------------------------------

def _log_gamma(xx: float) -> float:
    """Lanczos approximation of ln(Gamma(x)). Mirrors Java implementation."""
    cof = [
        76.18009172947146, -86.50532032941677, 24.01409824083091,
        -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5,
    ]
    x, y = xx, xx
    tmp = x + 5.5
    tmp -= (x + 0.5) * math.log(tmp)
    ser = 1.000000000190015
    for c in cof:
        y += 1.0
        ser += c / y
    return -tmp + math.log(2.5066282746310005 * ser / x)


def _gser(a: float, x: float, itmax: int = 200, eps: float = 3e-12) -> float:
    """Series representation of P(a, x)."""
    if x <= 0.0:
        return 0.0
    ap = a
    summ = 1.0 / a
    delta = summ
    for _ in range(itmax):
        ap += 1.0
        delta *= x / ap
        summ += delta
        if abs(delta) < abs(summ) * eps:
            break
    return summ * math.exp(-x + a * math.log(x) - _log_gamma(a))


def _gcf(a: float, x: float, itmax: int = 200, eps: float = 3e-12) -> float:
    """Continued fraction representation of Q(a, x) (Lentz)."""
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, itmax + 1):
        an = -1.0 * i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return math.exp(-x + a * math.log(x) - _log_gamma(a)) * h


def gamma_q(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a, x) = Gamma(a,x)/Gamma(a), in [0,1]."""
    if x < 0.0 or a <= 0.0:
        raise ValueError("invalid arguments")
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        return 1.0 - _gser(a, x)
    return _gcf(a, x)


def chi2_sf(stat: float, df: int) -> float:
    """Survival function of the chi-square distribution: P(Chi2_df > stat)."""
    return gamma_q(df / 2.0, stat / 2.0)


def kolmogorov_q(x: float) -> float:
    """Asymptotic survival function of the Kolmogorov distribution.

    Q_KS(x) = 2 * sum_{k=1..} (-1)^(k-1) exp(-2 k^2 x^2)
    """
    if x <= 0.0:
        return 1.0
    if x < 1.18:  # low-x series is more accurate there (Numerical Recipes / scipy)
        # kp = sqrt(2*pi)/x * sum_{j>=1} exp(- (2j-1)^2 pi^2 / (8 x^2))
        s = 0.0
        for j in range(1, 101):
            s += math.exp(-((2 * j - 1) ** 2) * (math.pi ** 2) / (8.0 * x * x))
        return (math.sqrt(2.0 * math.pi) / x) * s
    s = 0.0
    k = 1
    while True:
        term = math.exp(-2.0 * k * k * x * x)
        if term < 1e-16 and k > 1:
            break
        s += (1.0 if k % 2 == 1 else -1.0) * term
        k += 1
        if k > 1000:
            break
    return 2.0 * s


def ks_pvalue(d: float, n: int) -> float:
    """p-value for the one-sample K-S statistic D with sample size n.

    Uses the asymptotic Kolmogorov distribution evaluated at sqrt(n) * D,
    matching scipy.stats.kstest with dist='uniform' (same reference the
    course slides use).
    """
    return min(1.0, kolmogorov_q(math.sqrt(n) * d))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def chi_cuadrado(values: Sequence[float], k: int = 10) -> dict:
    """Chi-square uniformity test over k equal-width bins in [0, 1)."""
    n = len(values)
    e = n / k
    observed = [0] * k
    for v in values:
        idx = min(int(v * k), k - 1)
        observed[idx] += 1
    stat = sum((o - e) ** 2 / e for o in observed)
    df = k - 1
    p = chi2_sf(stat, df)
    return {
        "stat": stat,
        "df": df,
        "p": p,
        "reject": p < ALPHA,
        "observed": observed,
        "expected": e,
    }


def kolmogorov_smirnov(values: Sequence[float]) -> dict:
    """One-sample K-S test against theoretical U(0,1): F(x) = x."""
    n = len(values)
    xs = sorted(values)
    d_plus = max((i + 1) / n - x for i, x in enumerate(xs))
    d_minus = max(x - i / n for i, x in enumerate(xs))
    d = max(d_plus, d_minus)
    p = ks_pvalue(d, n)
    return {
        "stat": d,
        "p": p,
        "reject": p < ALPHA,
    }
