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
│   └── main.py                # entrada de consola
└── dist/                      # salidas: PNG
```

## Ejecutar

```bash
cd unidad1/practicas/APE1
python -m views.main                # tablas + gráficas
python -m views.main --interactivo  # además consulta una hora por consola
```

Requiere `matplotlib` (y `numpy`/`pandas` para el entorno):

```bash
python -m venv venv
./venv/bin/pip install matplotlib numpy pandas
```

Las gráficas se guardan en `dist/` y además se abren en pantalla con `plt.show()`.

## Salidas

| Archivo | Descripción |
| --- | --- |
| `dist/indice_original.png` | Índice por hora, modelo original |
| `dist/indice_ajustado.png` | Índice por hora, modelo ajustado |
| `dist/indice_comparacion.png` | Original vs. ajustado |
| `dist/variables_hora.png` | H, N y Tf por hora |
