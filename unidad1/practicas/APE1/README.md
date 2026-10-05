# APE 001 — Construcción y simulación computacional de un modelo matemático

Modelo del índice atmosférico para estimar la probabilidad de lluvia en una ventana
de 24 horas:

```
I = a·H + b·N + c·Tf
```

- `H` = humedad normalizada (`humedad % / 100`)
- `N` = nubosidad normalizada (`nubosidad % / 100`)
- `Tf` = factor de temperatura (tabla de la guía)

Reglas de decisión:

| Índice `I` | Estado |
| --- | --- |
| `I < 0.40` | Sin lluvia |
| `0.40 ≤ I < 0.60` | Baja posibilidad |
| `0.60 ≤ I < 0.75` | Lluvia probable |
| `I ≥ 0.75` | Lluvia |

Modelos comparados:

- **Original:** `I = 0.50H + 0.30N + 0.20Tf`
- **Ajustado:** `I = 0.40H + 0.35N + 0.25Tf` (coeficientes elegidos al azar, suman 1.0)

## Estructura

```
APE1/
├── models/datasets.py         # tabla Tf, coeficientes y datos horarios
├── controller/
│   ├── utils.py               # factor Tf, índice I y clasificación
│   └── tabla.py               # construcción e impresión de la tabla
├── views/
│   ├── graficas.py            # gráficas con matplotlib
│   └── main.py                # entrada de consola (Python)
├── java/
│   └── SimulacionAtmosferica.java   # misma práctica en Java (sin dependencias)
└── dist/                      # salidas: PNG y CSV
```

## Ejecutar Python

```bash
cd unidad1/practicas/APE1
python -m views.main                # tablas + gráficas
python -m views.main --interactivo  # además consulta una hora por consola
```

Requiere `numpy` y `matplotlib`:

```bash
python -m venv venv
./venv/bin/pip install numpy matplotlib pandas
```

## Ejecutar Java

Requiere un **JDK** (no alcanza con el JRE). Compila sin dependencias externas y dibuja
la gráfica con Java2D:

```bash
cd unidad1/practicas/APE1
javac -d build/java java/SimulacionAtmosferica.java
java -cp build/java SimulacionAtmosferica
```

## Salidas

| Archivo | Descripción |
| --- | --- |
| `dist/indice_original.png` | Índice por hora, modelo original (Python) |
| `dist/indice_ajustado.png` | Índice por hora, modelo ajustado (Python) |
| `dist/indice_comparacion.png` | Original vs. ajustado (Python) |
| `dist/variables_hora.png` | H, N y Tf por hora (Python) |
| `dist/barras_original.png` | Barras del índice, modelo original (Python) |
| `dist/barras_ajustado.png` | Barras del índice, modelo ajustado (Python) |
| `dist/indice_original_java.png` | Índice por hora, modelo original (Java) |
| `dist/indice_ajustado_java.png` | Índice por hora, modelo ajustado (Java) |
| `dist/datos_java.csv` | Tabla completa de ambos modelos (Java) |
