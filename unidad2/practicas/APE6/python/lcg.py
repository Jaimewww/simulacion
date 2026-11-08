"""
Linear Congruential Generator (LCG) - APE 6, Simulation.

X_{n+1} = (a * X_n + c) mod m
U_n = X_{n+1} / m  in [0, 1)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LCGConfig:
    name: str
    m: int  # modulus
    a: int  # multiplier
    c: int  # increment
    seed: int  # X_0
    quality: str  # "good" | "bad" - descriptive label for the report


# Classic LCG parameter sets taken from the course material (Semana 5 slides).
CONFIGS = [
    LCGConfig(name="glibc", m=2**32, a=1103515245, c=12345, seed=1, quality="good"),
    LCGConfig(name="java_random", m=2**48, a=25214903917, c=11, seed=42, quality="good"),
    LCGConfig(name="zx81_bad", m=2**17 + 1, a=75, c=74, seed=1, quality="bad"),
]


def generate(config: LCGConfig, n: int) -> tuple[int, list[float]]:
    """Generate n pseudo-random floats in [0, 1). Returns (final_state, values)."""
    x = config.seed % config.m
    values: list[float] = []
    for _ in range(n):
        x = (config.a * x + config.c) % config.m
        values.append(x / config.m)
    return x, values
