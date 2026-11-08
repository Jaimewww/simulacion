# Práctica 06 — Validación estadística de números pseudoaleatorios mediante Chi-cuadrado y Kolmogorov-Smirnov

| Campo | Detalle |
| --- | --- |
| Asignatura | Simulación |
| Ciclo | 5.º ciclo — FEIRNNR, Carrera de Computación |
| Unidad | U2 — Generación de números pseudoaleatorios |
| Práctica | Nro. 06 |
| Docente | José O. Guamán Q. |
| Estudiante | Jaime A. Landazuri |

## 1. Descripción

Generación de secuencias pseudoaleatorias con tres configuraciones clásicas de LCG y su
validación estadística de uniformidad sobre `U(0,1)` con `n = 10 000` y `α = 0.05`:

| Configuración | Referencia | `m` | `a` | `c` | Semilla |
| --- | --- | --- | --- | --- | --- |
| `glibc` | libc GNU/Linux | `2^32` | `1103515245` | `12345` | 1 |
| `java_random` | `java.util.Random` | `2^48` | `25214903917` | `11` | 42 |
| `zx81_bad` | ZX81 BASIC (mala calidad) | `2^17+1` | `75` | `74` | 1 |

**Pruebas aplicadas** (implementadas desde cero, sin librerías estadísticas):

- **Chi-cuadrado:** `k = 10` intervalos de igual amplitud, `Ei = 1000`, `gl = 9`; valor `p`
  con la gamma incompleta regularizada.
- **Kolmogorov-Smirnov:** comparación de la FDE empírica contra `F(x) = x`; estadístico
  `D = max(D+, D−)` y valor `p` con la forma asintótica de Kolmogorov.

**Propósito:** evaluar si cada generador es compatible con una uniforme `[0,1]`, comparar el
comportamiento entre configuraciones y verificar que la secuencia generada en Python y en
Java es idéntica con los mismos parámetros.

## 2. Estructura

```
APE6/
├── java/src/main/java/ape6/     # Lcg.java, Pruebas.java, Main.java
├── python/                      # lcg.py, pruebas.py, main.py, figures.py, check_parity.py
├── results/                     # estadísticos, frecuencias y secuencias de paridad
│   ├── stats_python.json, stats_java.json
│   ├── observed_*_{java,python}.csv
│   ├── parity_*_{java,python}.csv
│   └── parity_zx81_bad_*.csv
├── reportes/
│   └── reporte_tecnico_APE6.pdf # reporte técnico compilado
└── README.md
```

## 3. Requisitos

- Python ≥ 3.10 con NumPy y Matplotlib
- JDK (compilado y ejecutado con OpenJDK 27)
- Linux o macOS

## 4. Ejecución

```bash
# Python: genera secuencias, pruebas y estadísticos en results/
cd python
python3 main.py              # acepta --outdir ../results

# Python: figuras del informe (KS, lag-1, chi-cuadrado) en figures/
python3 figures.py

# Python: comparación de paridad entre implementaciones
python3 check_parity.py

# Java
cd java
javac -d out src/main/java/ape6/*.java
java -cp out ape6.Main
```

## 5. Resultados principales

| Configuración | χ² (gl=9) | p (χ²) | D (KS) | p (KS) | Decisión |
| --- | --- | --- | --- | --- | --- |
| glibc | 2.4360 | 0.9826 | 0.007134 | 0.3111 | No se rechaza H₀ |
| java_random | 11.1140 | 0.2680 | 0.007012 | 0.2907 | No se rechaza H₀ |
| zx81_bad | 7.8600 | 0.5483 | 0.011633 | 0.8665 | No se rechaza H₀ |

- Las tres configuraciones pasan ambas pruebas de uniformidad con `n = 10 000`.
- **Hallazgo clave:** `zx81_bad` viola las condiciones de Hull–Dobell (su ciclo cubre solo
  21 845 estados) y aun así aprueba las pruebas de uniformidad; su defecto real es de
  agregación serial (pares consecutivos concentrados en líneas), visible en el diagrama de
  dispersión `U(n) vs U(n+1)` del informe. Una prueba de bondad de ajuste valida propiedades,
  no demuestra aleatoriedad.
- **Paridad Python/Java:** los primeros 200 estados, las frecuencias, `χ²` y `D` coinciden
  bit a bit para las tres configuraciones (`check_parity.py` sobre `results/parity_*.csv`).

El análisis completo, gráficas (KS, χ², lag-1), preguntas de control, conclusiones y
bibliografía están en el reporte técnico: [`reportes/reporte_tecnico_APE6.pdf`](reportes/reporte_tecnico_APE6.pdf).
