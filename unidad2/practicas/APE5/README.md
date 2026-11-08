# Práctica 05 — Implementación y análisis del Generador Congruencial Lineal (LCG) en Python y Java

| Campo | Detalle |
| --- | --- |
| Asignatura | Simulación |
| Ciclo | 5.º ciclo — FEIRNNR, Carrera de Computación |
| Unidad | U2 — Generación de números pseudoaleatorios |
| Práctica | Nro. 05 (Guía APE Nro. 004) |
| Docente | José O. Guamán Q. |
| Estudiante | Jaime A. Landazuri |

## 1. Descripción

Implementación, en dos lenguajes, del generador congruencial lineal (LCG) definido por la
recursión `X(n+1) = (a · X(n) + c) mod m` con normalización `U(n) = X(n)/m`, usando los
parámetros de la guía:

- Multiplicador `a = 1664525`
- Incremento `c = 1013904223`
- Módulo `m = 2^32`
- Semillas evaluadas: `12345` y `54321`

**Propósito:** verificar que ambas implementaciones producen exactamente la misma secuencia
de 10 000 valores, analizar estadísticamente la secuencia (media, desviación, histograma,
correlación serial de pares consecutivos) y demostrar que el período es completo (`m = 2^32`)
mediante la hipótesis de Hull–Dobell.

## 2. Estructura

```
APE5/
├── LCG.java            # implementación espejo del LCG en Java
├── lcg.py              # implementación del LCG en Python (genera CSV y gráficos)
├── resultados/         # CSV de primeras 20 observaciones y de las 10 000 por semilla
│   ├── java_10000_12345.csv, java_10000_54321.csv
│   ├── java_primeras20_12345.csv, java_primeras20_54321.csv
│   ├── python_10000_12345.csv, python_10000_54321.csv
│   ├── python_primeras20_12345.csv, python_primeras20_54321.csv
│   └── lcg_seed12345.png, lcg_seed54321.png
├── reportes/
│   └── reporte_tecnico_APE005.pdf   # reporte técnico compilado
└── README.md
```

## 3. Requisitos

- Python ≥ 3.10 con `matplotlib` (`pip install matplotlib`)
- JDK (compilado y ejecutado con OpenJDK 27)
- Linux o macOS

## 4. Ejecución

```bash
# Python (semilla por defecto 12345; acepta semilla opcional)
python3 lcg.py          # o: python3 lcg.py 54321

# Java
javac LCG.java
java LCG
```

Cada ejecución imprime el resumen estadístico y genera los CSV de la secuencia completa
(`*_10000_*.csv`), las primeras 20 observaciones (`*_primeras20_*.csv`) y el gráfico
cuadriculado (evolución, dispersión `U(n) vs U(n+1)`, histograma y resumen).

## 5. Resultados principales

| Verificación | Semilla 12345 | Semilla 54321 |
| --- | --- | --- |
| Diferencias primeras 20 (Python vs Java) | 0 / 20 | 0 / 20 |
| Diferencias en 10 000 valores (Python vs Java) | 0 / 10 000 | 0 / 10 000 |
| Media de U (teórico `0.5`) | 0.498770 | 0.498870 |
| Desviación estándar (teórica `1/√12 ≈ 0.288675`) | 0.288132 | 0.289131 |

- Las secuencias de Python y Java son idénticas valor a valor (mismo `X(n)` entero y misma
  `U(n)` normalizada): el algoritmo, no la plataforma, define la secuencia.
- El cambio de semilla produce un flujo completamente distinto, sin valores compartidos
  dentro de las 10 000 observaciones, y con estadísticos equivalentes.
- Con `c` impar (coprimo con `2^32`) y `a − 1 ≡ 0 (mod 4)`, los parámetros cumplen la
  hipótesis de Hull–Dobell, por lo que el período teórico es completo: `2^32 ≈ 4.29 × 10^9`;

  empíricamente se validó el criterio con módulos pequeños (`m = 16`).

El análisis completo, tablas de las primeras 20 observaciones, gráficas, preguntas de control
y conclusiones están en el reporte técnico: [`reportes/reporte_tecnico_APE005.pdf`](reportes/reporte_tecnico_APE005.pdf).

## 6. Nota de implementación Java

El producto `a · X(n)` excede el rango de `int` y de los productos intermedios de `long` con
signo de 32 bits, por lo que la multiplicación modular se descompuso en productos parciales
de 16 bits y se aplicó la máscara `& 0xFFFFFFFFL` en cada paso. De esta forma Java replica
el comportamiento de Python sin recurrir a `BigInteger`.
