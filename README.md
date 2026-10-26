# Simulación

Trabajos prácticos de la asignatura **Simulación** (5.º ciclo, FEIRNNR — Carrera de Computación).

## Contenido

| Ruta | Práctica |
| --- | --- |
| `unidad1/practicas/APE1/` | APE 001 — Construcción y simulación computacional de un modelo matemático |
| `unidad1/practicas/APE2/APE2_SIMULACION/` | APE 002 — Comparación de modelos determinísticos, estocásticos, discretos y continuos |
| `unidad1/practicas/APE3/` | APE 003 — Simulación de un sistema de líneas de espera M/M/1 mediante SimPy |
| `unidad1/practicas/APE4/` | APE 004 — Modelo SIR en Java y NetLogo |

## APE 001 — Modelo de probabilidad de lluvia

Modelo del índice atmosférico `I = a·H + b·N + c·Tf`, con `H` humedad normalizada,
`N` nubosidad normalizada y `Tf` factor de temperatura.

- Modelo original: `I = 0.50H + 0.30N + 0.20Tf`
- Modelo ajustado: `I = 0.40H + 0.35N + 0.25Tf` (coeficientes aleatorios que suman 1)

Implementado en **Python** con matplotlib: genera la tabla horaria y las gráficas
en `unidad1/practicas/APE1/dist/`.

Instrucciones de ejecución en
[`unidad1/practicas/APE1/README.md`](unidad1/practicas/APE1/README.md).

## APE 002 — Modelos de crecimiento poblacional

Cuatro paradigmas de simulación del mismo sistema de crecimiento poblacional, comparados
sobre la serie observada `[1000, 1100, 1250, 1400, 1600, 1850, 2100]`:

| Modelo | Ecuación |
| --- | --- |
| Determinístico | `P(t) = P0 · e^(r·t)` |
| Discreto | `P[k+1] = P[k] + r·P[k]` |
| Estocástico | `P[k+1] = P[k] + r·P[k] + ruido`, `ruido ~ Normal(0, σ)` |
| Continuo (Euler) | `P[k+1] = P[k] + Δt·(r·P[k])` |

Implementado en **Python** con NumPy, Matplotlib y pandas. Al estimar la tasa `r` desde los
datos (`r = 0,1318`) el modelo discreto reduce su RMSE de 265,29 a 29,61, lo que muestra
que el mecanismo subyacente de la serie es multiplicativo por período.

Instrucciones, resultados y declaración de uso de IA en
[`unidad1/practicas/APE2/APE2_SIMULACION/README.md`](unidad1/practicas/APE2/APE2_SIMULACION/README.md).
El reporte técnico está en `unidad1/practicas/APE2/APE2_SIMULACION/reporte_tecnico_overleaf.tex`.

## APE 003 — Sistema de líneas de espera M/M/1

Simulación de una fila con **un solo servidor** usando **SimPy**: llegadas de Poisson
(λ), tiempos de servicio exponenciales (μ) y atención FIFO, sobre los tres escenarios
de la guía (ρ = 0,667 / 0,833 / 0,967).

Comparación teoría vs simulación con 10 réplicas por escenario (30 corridas
reproducibles): en los tres escenarios el valor teórico de la espera Wq cae dentro del
intervalo de confianza al 95 % de lo simulado, y la espera y la cola crecen de forma
acelerada al acercarse λ a μ (Wq simulado: 0,67 → 1,81 → 8,57).

Instrucciones de ejecución en
[`unidad1/practicas/APE3/README.md`](unidad1/practicas/APE3/README.md).
El reporte técnico (LaTeX + PDF, con análisis, preguntas de control, conclusiones y
declaración de uso de IA) está en `unidad1/practicas/APE3/reports/`.

## APE 004 — Modelo SIR en Java y NetLogo

Simulación por agentes de una población de 100 personas, con exportación CSV desde Java y comparación visual en NetLogo.

Código e instrucciones en [`unidad1/practicas/APE4/README.md`](unidad1/practicas/APE4/README.md). Esta práctica publica solo los fuentes y el README; el informe y los archivos generados se mantienen fuera del repositorio.
