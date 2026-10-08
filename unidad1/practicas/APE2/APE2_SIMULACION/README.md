# APE 002 — Comparación de modelos determinísticos, estocásticos, discretos y continuos

Práctica experimental Nro. 002 de **Simulación** (5.º ciclo, FEIRNNR — Carrera de
Computación). El sistema de estudio es el **crecimiento poblacional** y el objetivo es
diferenciar los cuatro paradigmas de simulación construyendo el mismo sistema con cada uno
y comparando sus resultados.

- Guía: `../ape_guia simulacion semana 2-firmado-signed.pdf`
- Reporte técnico: `reporte_tecnico_overleaf.tex` (fuente LaTeX para Overleaf)
- Declaración de uso de IA: al final de este README y en el reporte

## 1. Modelos implementados

Todos los modelos parten de la misma población inicial `P0` y devuelven un valor por
período, de modo que las cuatro series se comparan sobre la misma malla entera `0..6`.

| # | Modelo | Ecuación | ¿Aleatorio? | Naturaleza del tiempo |
| --- | --- | --- | --- | --- |
| 1 | Determinístico | `P(t) = P0 · e^(r·t)` | No | Continuo (solución exacta) |
| 2 | Discreto | `P[k+1] = P[k] + r·P[k]` | No | Discreto (períodos fijos) |
| 3 | Estocástico | `P[k+1] = P[k] + r·P[k] + ruido`, `ruido ~ Normal(0, σ)`; si el resultado es negativo se fija en `0` | **Sí** | Discreto (períodos fijos) |
| 4 | Continuo (Euler) | `P[k+1] = P[k] + Δt·(r·P[k])` | No | Continuo aproximado numéricamente |

Observaciones de diseño:

- El modelo **discreto** es un sistema *iterativo*: el incremento se recalcula sobre la
  población que ya creció, por eso equivale al factor multiplicativo `(1 + r)` aplicado
  `k` veces.
- El modelo **continuo con Euler** reproduce el mismo incremento proporcional, pero con
  paso `Δt`; al ser un método numérico de primer orden introduce un error que decrece al
  reducir `Δt` (ver `dist/efecto_dt.png`).
- El modelo **estocástico** es el único con comportamiento aleatorio; el ruido se modela
  como una normal de media cero, por lo que en promedio el sistema sigue la tendencia
  discreta pero cada corrida individual se dispersa.

## 2. Datos de entrada

La serie observada que indica la guía es el «arreglo de entrada» de la práctica:

```python
datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]
```

Representa la población observada en 7 períodos consecutivos (índices `0` a `6`). Cumple
tres funciones en la simulación:

1. **Condición inicial:** `P0 = datos[0] = 1000`.
2. **Horizonte:** define el número de períodos, `6`.
3. **Referencia de validación:** permite medir qué tan cerca queda cada modelo de la
   realidad mediante el error cuadrático medio (RMSE).

## 3. Estructura del proyecto

```text
APE2_SIMULACION/
├── models/
│   ├── __init__.py
│   └── parametros.py       # serie observada y parámetros por defecto
├── controller/
│   ├── __init__.py
│   └── modelos.py          # los cuatro modelos, estimación de r y métricas
├── views/
│   ├── __init__.py
│   ├── graficas.py         # las seis gráficas y el CSV (matplotlib + pandas)
│   └── main.py             # punto de entrada por consola
├── dist/                   # salidas generadas: PNG + CSV
├── requirements.txt
├── referencias.bib
├── reporte_tecnico_overleaf.tex
├── reporte_tecnico_overleaf.pdf    # reporte compilado (11 páginas)
└── reporte_tecnico_overleaf_logo.png
```

La carpeta `dist/` se resuelve de forma relativa al paquete, así que el proyecto se puede
ejecutar desde cualquier directorio de trabajo.

## 4. Requisitos e instalación

Solo se necesita Python 3.10 o superior.

```bash
cd unidad1/practicas/APE2/APE2_SIMULACION

python -m venv venv                    # crear el entorno virtual
source venv/bin/activate               # activarlo (Linux / macOS)

pip install -r requirements.txt        # instalar dependencias
```

Dependencias declaradas en `requirements.txt`:

| Paquete | Uso |
| --- | --- |
| `numpy` | cálculo vectorial, `exp`, generador aleatorio y `polyfit` |
| `matplotlib` | generación de las gráficas |
| `pandas` | escritura de `dist/resultados.csv` |

> **Nota:** la guía menciona además `scipy` y `pynetlogo` en su línea de instalación. Esta
> implementación es Python + NumPy puro (el pseudocódigo de la guía es íntegramente Python
> y las gráficas se generan con Matplotlib), por lo que esas dos librerías son opcionales y
> **no** se importan ni se declaran: declarar dependencias sin uso sería ruido.

## 5. Ejecución

```bash
# Corrida por defecto: P0=1000, r=0.08, sigma=40, dt=0.1, seed=42
python -m views.main

# Sin abrir ventanas (útil para servidores o para el reporte)
python -m views.main --no-show

# Usar la tasa r estimada a partir de la serie observada
python -m views.main --no-show --ajustar-r

# Cambiar los parámetros de la corrida
python -m views.main --no-show --r 0.15 --sigma 60 --dt 0.05 --seed 7

# Escenario de decrecimiento
python -m views.main --no-show --r -0.10
```

Banderas disponibles:

| Bandera | Por defecto | Descripción |
| --- | --- | --- |
| `--p0` | `1000` | Población inicial |
| `--r` | `0.08` | Tasa de crecimiento (negativa ⇒ decrecimiento) |
| `--sigma` | `40.0` | Nivel de ruido del modelo estocástico |
| `--dt` | `0.1` | Paso de integración de Euler |
| `--periodos` | `6` | Número de períodos simulados |
| `--seed` | `42` | Semilla del generador aleatorio (reproducibilidad) |
| `--ajustar-r` | desactivado | Reemplaza `--r` por la tasa estimada desde `datos` |
| `--no-show` | desactivado | No abre las figuras en pantalla (igual las guarda) |

La semilla fija (`42`) hace que el modelo estocástico sea **reproducible**: dos corridas con
los mismos parámetros producen exactamente los mismos números, algo indispensable para que
el reporte y las gráficas sean verificables.

## 6. Salidas generadas en `dist/`

| Archivo | Contenido |
| --- | --- |
| `comparacion_modelos.png` | Los cuatro modelos frente a la serie observada |
| `crecimiento_decrecimiento.png` | Crecimiento (`r = +0.12`) vs. decrecimiento (`r = -0.12`) |
| `influencia_r.png` | Efecto de distintos valores de `r` en el modelo determinístico |
| `efecto_sigma.png` | Media de 30 corridas y banda ±1 desviación estándar por cada `σ` |
| `efecto_dt.png` | Euler vs. exponencial exacta para varios `Δt` (error del método) |
| `ajuste_r.png` | Ajuste de la tasa estimada desde los datos observados |
| `resultados.csv` | Tabla comparativa: período, observado y los cuatro modelos |

## 7. Resultados obtenidos

### 7.1 Corrida por defecto (`r = 0.08`, `σ = 40`, `Δt = 0.1`, `seed = 42`)

| Período | Observado | Determinista | Discreto | Estocástico | Euler |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1000.00 | 1000.00 | 1000.00 | 1000.00 | 1000.00 |
| 1 | 1100.00 | 1083.29 | 1080.00 | 1092.19 | 1082.94 |
| 2 | 1250.00 | 1173.51 | 1166.40 | 1137.96 | 1172.76 |
| 3 | 1400.00 | 1271.25 | 1259.71 | 1259.02 | 1270.04 |
| 4 | 1600.00 | 1377.13 | 1360.49 | 1397.36 | 1375.38 |
| 5 | 1850.00 | 1491.82 | 1469.33 | 1431.11 | 1489.45 |
| 6 | 2100.00 | 1616.07 | 1586.87 | 1493.51 | 1612.99 |

Factor de crecimiento discreto `(1 + r) = 1.0800`.

| Métrica contra la serie observada | Valor |
| --- | ---: |
| RMSE determinístico | 249.24 |
| RMSE discreto | 265.29 |
| RMSE estocástico | 296.85 |
| RMSE Euler | 250.93 |

Con `r = 0.08` los cuatro modelos **subestiman** la población observada: la serie real crece
un 13.18 % por período, no un 8 %.

### 7.2 Estimación de `r` a partir de los datos observados

| Estimador | Valor |
| --- | ---: |
| Tasa discreta (media de las razones − 1) | **0.1318** |
| Tasa continua (pendiente de `ln P` vs `t`) | **0.1254** |
| Factor de crecimiento medio | 1.1318 |

Las dos tasas **no** deben coincidir: son parámetros de modelos distintos y se relacionan
por `r_continuo = ln(1 + r_discreto)`; en efecto, `ln(1.1318) = 0.1238 ≈ 0.1254`. La tasa
discreta describe saltos multiplicativos (`(1 + r)^k`), la continua describe crecimiento
instantáneo (`e^(r·t)`).

### 7.3 Corrida ajustada (`--ajustar-r`, `r = 0.1318`)

| Período | Observado | Determinista | Discreto | Estocástico | Euler |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1000.00 | 1000.00 | 1000.00 | 1000.00 | 1000.00 |
| 1 | 1100.00 | 1140.84 | 1131.77 | 1143.96 | 1139.86 |
| 2 | 1250.00 | 1301.52 | 1280.90 | 1253.09 | 1299.29 |
| 3 | 1400.00 | 1484.83 | 1449.68 | 1448.23 | 1481.01 |
| 4 | 1600.00 | 1693.96 | 1640.70 | 1676.68 | 1688.14 |
| 5 | 1850.00 | 1932.55 | 1856.89 | 1819.57 | 1924.25 |
| 6 | 2100.00 | 2204.73 | 2101.57 | 2007.25 | 2193.38 |

| Métrica contra la serie observada | Valor |
| --- | ---: |
| RMSE determinístico | 73.81 |
| **RMSE discreto** | **29.61** |
| RMSE estocástico | 53.02 |
| RMSE Euler | 68.22 |

Al usar la tasa estimada, el **modelo discreto** es el que mejor reproduce la serie
observada (RMSE 29.61 frente a 265.29 con `r = 0.08`), lo que confirma que el mecanismo
subyacente de los datos es multiplicativo por período.

## 8. Interpretación matemática

- **Influencia de `r`.** `r` es la tasa de crecimiento y solo depende de la ecuación
  diferencial `dP/dt = r·P`; su valor decide el tipo de solución, no su escala:
  - `r > 0` ⇒ crecimiento exponencial: la población crece cada vez más rápido porque el
    incremento es proporcional a la población actual (realimentación positiva).
  - `r = 0` ⇒ equilibrio: el sistema permanece constante en `P0`.
  - `r < 0` ⇒ decrecimiento exponencial: la población tiende asintóticamente a `0` sin
    llegar a tocarlo en tiempo finito.
- **Diferencia entre discreto y continuo.** El modelo discreto produce una *sucesión*
  `P[k] = P0·(1 + r)^k`, mientras el continuo produce una *función*
  `P(t) = P0·e^(r·t)`. Euler convierte el continuo en una sucesión con factor
  `(1 + r·Δt)`, de modo que ambos coinciden cuando `Δt → 0`; para `Δt = 1` Euler es
  idéntico al modelo discreto. El error de Euler es de primer orden en `Δt`.
- **Rol de `σ`.** `σ` es la desviación estándar del ruido aditivo: mide la **variabilidad**
  del sistema, no su tendencia. Al aumentar `σ` la media se mantiene cercana a la
  trayectoria determinista, pero la banda de dispersión se ensancha y la proporción de
  trayectorias que tocan el límite inferior `0` crece.
- **Por qué graficar.** Una tabla de siete números no revela la *forma* del fenómeno
  (exponencial, lineal, saturada) ni permite distinguir a simple vista una trayectoria con
  ruido de una determinista. La gráfica expone la tendencia, la dispersión y el error del
  método numérico de forma inmediata.

## 9. Reporte técnico

| Archivo | Descripción |
| --- | --- |
| `reporte_tecnico_overleaf.tex` | Fuente LaTeX (para Overleaf) |
| `referencias.bib` | Bibliografía en formato BibTeX (estilo IEEE) |
| `reporte_tecnico_overleaf.pdf` | Reporte compilado, 11 páginas |

### Cómo compilarlo en Overleaf

1. Subir `reporte_tecnico_overleaf.tex`, `referencias.bib`, `reporte_tecnico_overleaf_logo.png`
   **y la carpeta `dist/` completa** (el `.tex` toma las seis figuras de ahí mediante
   `\graphicspath{{dist/}{./}}`).
2. Compilador: **pdfLaTeX** (el documento usa `inputenc`/`fontenc`, es su motor natural).
3. La bibliografía se resuelve sola: el documento ya incluye
   `\bibliographystyle{IEEEtran}` y `\bibliography{referencias}`.

### Qué contiene

Datos de identificación · objetivos · materiales · fundamento teórico de los cuatro modelos
· procedimiento ejecutado · resultados con las tablas y las seis figuras · interpretación
matemática · respuestas a las diez preguntas de control · conclusiones · declaración de uso
de IA · referencias.

El reporte fue compilado y verificado localmente: 11 páginas A4, sin referencias
indefinidas, sin desbordes de margen y con las seis figuras embebidas.

## 10. Preguntas de control

Las diez preguntas de control de la guía están desarrolladas con su justificación en la
sección 8 de `reporte_tecnico_overleaf.tex`.

## 11. Declaración de uso de Inteligencia Artificial

En cumplimiento de los principios de solidaridad, transparencia, responsabilidad y
honestidad del resultado de aprendizaje R1, se declara que:

1. Se utilizó asistencia de inteligencia artificial como **herramienta de apoyo acotada**,
   estimada en **no más del 20 %** del trabajo total de la práctica.
2. La IA **no reemplazó el razonamiento del estudiante**. El análisis del problema, la
   selección de los cuatro modelos, la interpretación matemática de los resultados, la
   estimación de la tasa `r` y las respuestas a las preguntas de control fueron razonados,
   revisados y validados por el estudiante.
3. El uso de la IA se limitó a tareas auxiliares: redacción y estructuración del código a
   partir del pseudocódigo provisto en la guía, formato de las gráficas y revisión de
   estilo de la documentación.
4. El estudiante **comprendió, ejecutó y verificó** cada resultado presentado: los valores
   de las tablas de la sección 7 provienen de corridas reproducibles
   (`--seed 42`) del programa incluido en esta práctica.
5. El estudiante asume la responsabilidad total por el contenido, la exactitud y la
   originalidad del trabajo entregado.

## 12. Referencias

- Guamán Q., J. O. *Guía de Actividades Práctico-Experimentales Nro. 002*. FEIRNNR —
  Carrera de Computación, 2026.
- Diapositivas de la semana 2, asignatura Simulación.
- Bibliografía ampliada en `referencias.bib` (citada en el reporte técnico).
