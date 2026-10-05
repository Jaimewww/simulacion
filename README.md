# Simulación

Trabajos prácticos de la asignatura **Simulación** (5.º ciclo, FEIRNNR — Carrera de Computación).

## Contenido

| Ruta | Práctica |
| --- | --- |
| `unidad1/practicas/APE1/` | APE 001 — Construcción y simulación computacional de un modelo matemático |

## APE 001 — Modelo de probabilidad de lluvia

Modelo del índice atmosférico `I = a·H + b·N + c·Tf`, con `H` humedad normalizada,
`N` nubosidad normalizada y `Tf` factor de temperatura.

- Modelo original: `I = 0.50H + 0.30N + 0.20Tf`
- Modelo ajustado: `I = 0.40H + 0.35N + 0.25Tf` (coeficientes aleatorios que suman 1)

Se implementa en **Python** y **Java**, ambos generan la tabla horaria y las gráficas
en `unidad1/practicas/APE1/dist/`.

Instrucciones de ejecución en
[`unidad1/practicas/APE1/README.md`](unidad1/practicas/APE1/README.md).
