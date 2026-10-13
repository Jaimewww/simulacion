# APE 001 — Construcción y simulación computacional de un modelo matemático

Práctica Nro. 001 de **Simulación** (5.º ciclo, FEIRNNR — Carrera de Computación). El
sistema de estudio es el **índice atmosférico**, un modelo matemático que estima la
probabilidad de lluvia en una ventana de 24 horas a partir de la humedad, la nubosidad y
la temperatura observadas. El trabajo implementa el modelo propuesto por la guía y una
versión ajustada del mismo, completa la tabla horaria para las 9 observaciones y genera
las gráficas correspondientes.

- Guía: `../ape_guia simulacion semana 1-firmado-signed.pdf`
- Declaración de uso de IA: al final de este README

## 1. Modelo implementado

El índice atmosférico es una combinación lineal de tres variables normalizadas:

```text
I = a·H + b·N + c·Tf
```

- `H` = humedad normalizada (humedad % / 100)
- `N` = nubosidad normalizada (nubosidad % / 100)
- `Tf` = factor de temperatura, tomado de la tabla de la guía

Se implementan dos versiones del modelo:

| Modelo | Coeficientes | Expresión |
| --- | --- | --- |
| **Original** | a = 0.50, b = 0.30, c = 0.20 | `I = 0.50H + 0.30N + 0.20Tf` |
| **Ajustado** | a = 0.40, b = 0.35, c = 0.25 | `I = 0.40H + 0.35N + 0.25Tf` |

Ambos conjuntos de coeficientes suman 1.0; el ajustado se eligió al azar sobre esa
restricción («Ajuste el modelo y llene de nuevo la misma tabla», según la guía).

### Factor de temperatura (`Tf`)

| Temperatura | `Tf` |
| --- | ---: |
| ≤ 10 °C | 1.00 |
| 12 °C | 0.90 |
| 14 °C | 0.80 |
| 16 °C | 0.70 |
| 18 °C | 0.60 |
| 20 °C | 0.50 |
| 22 °C | 0.40 |
| 24 °C | 0.30 |
| 26 °C | 0.20 |
| ≥ 28 °C | 0.10 |

La función `controller.utils.tf_dict` redondea la temperatura al múltiplo de 2 °C más
cercano (`round(temp / 2) * 2`) antes de consultar la tabla y **limita** el resultado al
rango de la tabla: por debajo de 10 °C usa `Tf = 1.00` y por encima de 28 °C usa
`Tf = 0.10`. Por ejemplo, 17 °C se redondea a 16 °C, de modo que `Tf = 0.70`.

### Reglas de decisión (lluvia)

| Índice `I` | Estado |
| --- | --- |
| `I < 0.40` | Sin lluvia |
| `0.40 ≤ I < 0.60` | Baja posibilidad |
| `0.60 ≤ I < 0.75` | Lluvia probable |
| `I ≥ 0.75` | Lluvia |

### Ejemplo de la guía

Con humedad = 90 %, nubosidad = 80 % y temperatura = 18 °C:

```text
H  = 0.90
N  = 0.80
Tf = 0.60
I  = 0.50(0.90) + 0.30(0.80) + 0.20(0.60) = 0.81
```

Con `I = 0.81 ≥ 0.75` el modelo clasifica el estado como **lluvia**.

## 2. Datos de entrada

Las 9 observaciones horarias que indica la guía, tal como están declaradas en
`models/datasets.py`:

| Hora | Humedad (%) | Nubosidad (%) | Temperatura (°C) |
| --- | ---: | ---: | ---: |
| 06:00 | 65 | 40 | 14 |
| 08:00 | 70 | 50 | 16 |
| 10:00 | 68 | 45 | 18 |
| 12:00 | 60 | 30 | 22 |
| 14:00 | 75 | 70 | 20 |
| 16:00 | 85 | 85 | 18 |
| 18:00 | 92 | 95 | 16 |
| 20:00 | 88 | 90 | 17 |
| 22:00 | 80 | 75 | 15 |

## 3. Estructura del proyecto

```text
APE1/
├── models/
│   ├── __init__.py
│   └── datasets.py        # tabla Tf, coeficientes y datos horarios
├── controller/
│   ├── __init__.py
│   ├── utils.py           # factor Tf, índice I y clasificación
│   └── tabla.py           # construcción e impresión de la tabla horaria
├── views/
│   ├── __init__.py
│   ├── graficas.py        # las cuatro gráficas (matplotlib)
│   └── main.py            # punto de entrada por consola
├── dist/                  # salidas generadas: PNG
├── requirements.txt
└── README.md
```

La carpeta `dist/` se resuelve de forma relativa al paquete
(`views/graficas.py`), así que las imágenes se guardan siempre en la misma ubicación
independientemente del directorio de trabajo.

## 4. Requisitos e instalación

Solo se necesita Python 3.10 o superior.

```bash
cd unidad1/practicas/APE1

python -m venv venv                    # crear el entorno virtual
source venv/bin/activate               # activarlo (Linux / macOS)

pip install -r requirements.txt        # instalar dependencias
```

Dependencias declaradas en `requirements.txt`:

| Paquete | Uso |
| --- | --- |
| `matplotlib` | generación de las gráficas |

> **Nota:** la guía lista `NumPy` y `Matplotlib` entre sus materiales, pero el código de
> esta práctica es Python puro: el cálculo de `H`, `N`, `Tf` e `I` usa únicamente
> aritmética básica y `round()`, y la única dependencia de terceros realmente importada
> es `matplotlib`. Cualquier otra librería instalada en el entorno se considera
> opcional y **no** se declara: declarar dependencias sin uso sería ruido.

## 5. Ejecución

```bash
# Corrida estándar: tablas de ambos modelos + gráficas
python -m views.main

# Además solicita una consulta interactiva (humedad, nubosidad y temperatura)
python -m views.main --interactivo
```

Banderas disponibles:

| Bandera | Por defecto | Descripción |
| --- | --- | --- |
| `--interactivo` | desactivado | Tras generar las gráficas, pide humedad, nubosidad y temperatura por consola |

Las gráficas se guardan en `dist/` **y** se abren en pantalla mediante `plt.show()`; por
eso la corrida queda a la espera de que se cierre la ventana de la última figura.
Ejecutar `python -m views.main` desde el directorio `APE1/`.

## 6. Salidas generadas en `dist/`

| Archivo | Contenido |
| --- | --- |
| `indice_original.png` | Índice `I` por hora del modelo original con los umbrales de lluvia |
| `indice_ajustado.png` | Índice `I` por hora del modelo ajustado con los umbrales de lluvia |
| `indice_comparacion.png` | Modelo original vs. modelo ajustado (umbral `I ≥ 0.75`) |
| `variables_hora.png` | Evolución de `H`, `N` y `Tf` por hora |

## 7. Alcance y limitaciones

- La guía indica «Se debe programar en java y Python». Esta entrega incluye únicamente la
  implementación **en Python**; no se adjunta una versión en Java.
- Los apartados «Resultados esperados» y «Preguntas de Control» de la guía mencionan
  `P₀`, `r` y el modelo exponencial (gráficas de crecimiento/decrecimiento, influencia de
  `r`). Esos conceptos pertenecen a la plantilla de **crecimiento poblacional** y **no
  corresponden** al modelo de índice atmosférico de esta práctica, por lo que no se
  desarrollan aquí.
- Las observaciones cubren 9 horas (de 06:00 a 22:00) y no las 24 horas completas de la
  ventana que describe la guía; el comportamiento en las horas no muestreadas es una
  extrapolación del modelo sin datos de respaldo.
- El modelo es **determinístico**: con las mismas observaciones produce siempre el mismo
  índice; no incorpora componentes estocásticos ni etapa de validación estadística.

## 8. Declaración de uso de Inteligencia Artificial

En cumplimiento de los principios de solidaridad, transparencia, responsabilidad y
honestidad del resultado de aprendizaje R1, se declara que:

1. Se utilizó asistencia de inteligencia artificial como **herramienta de apoyo acotada**,
   estimada en **no más del 20 %** del trabajo total de la práctica.
2. La IA **no reemplazó el razonamiento del estudiante**. El análisis del problema
   atmosférico, la interpretación del modelo `I = 0.50H + 0.30N + 0.20Tf`, la elección de
   los coeficientes del modelo ajustado y la clasificación según las reglas de la guía
   fueron razonados, revisados y validados por el estudiante.
3. El uso de la IA se limitó a tareas auxiliares: redacción y estructuración del código
   en Python a partir de las ecuaciones y la tabla de la guía, formato de las gráficas y
   revisión de estilo de la documentación.
4. El estudiante **comprendió, ejecutó y verificó** cada resultado presentado: las tablas
   y las gráficas de la sección 6 provienen de corridas del programa incluido en esta
   práctica.
5. El estudiante asume la responsabilidad total por el contenido, la exactitud y la
   originalidad del trabajo entregado.

## 9. Referencias

- Guamán Q., J. O. *Guía de Actividades Práctico-Experimentales Nro. 001*. FEIRNNR —
  Carrera de Computación, 2026.
- Diapositivas de la semana 1, asignatura Simulación.