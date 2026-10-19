# reports/

Entregables **redactados** de la APE 003.

| Archivo | Qué es |
| --- | --- |
| `ape3_mm1.tex` | Fuente LaTeX del informe (plantilla institucional llenada) |
| `ape3_mm1.pdf` | PDF compilado (9 páginas) |
| `referencias.bib` | Bibliografía (teoría de colas, simulación, SimPy, guía) |
| `assets/reporte_tecnico_overleaf_logo.png` | Logo institucional del encabezado |
| `figures/` | Figuras insertadas en el informe |

El documento parte de
[`docs/PLANTILLA_APE_LATEX/reporte_tecnico_overleaf.tex`](../docs/PLANTILLA_APE_LATEX/reporte_tecnico_overleaf.tex)
y cubre los tres criterios que califica la guía §8: estructura y presentación,
procedimiento y evidencias, y conclusiones atadas a los objetivos.

## De dónde salen los números

Ningún número del informe está escrito a mano: la corrida oficial es la que produce
`python3 main.py` con la configuración de `controlador/controlador.py`
(`TIEMPO_SIMULACION = 5000`, `REPETICIONES = 10`, `SEMILLA = 42`). Como cada réplica
deriva su semilla de la semilla base, la corrida es reproducible y las tablas se pueden
regenerar. Las tres figuras de `figures/` son las que el programa escribe en
`graficas/`, copiadas tal cual.

## Cómo compilar

Con Overleaf: subir `ape3_mm1.tex`, `referencias.bib`, `assets/` y `figures/`, y
compilar con pdfLaTeX o XeLaTeX (la bibliografía se resuelve con BibTeX).

Localmente, con Tectonic:

```bash
cd reports
tectonic ape3_mm1.tex
```

> **Nota sobre los caracteres.** El documento se probó con XeTeX (Tectonic) y con T1 +
> Helvetica. Para que los signos de apertura salgan bien en los dos motores, el fuente
> usa `\textquestiondown{}` en lugar del carácter literal `¿`. **No lo reemplaces por el
> carácter `¿` al editar.**
>
> **Nota sobre el bloque de consola.** El listado de la salida del programa usa el
> entorno `alltt` y no `verbatim`, porque la fuente monoespaciada no tiene los glifos
> griegos. Por eso dentro del bloque las letras griegas van entre `\(...\)` y no entre
> `$...$`.

## Secciones que el equipo todavía debe completar

Están marcadas en rojo con `[PENDIENTE: ...]` en el PDF:

- [ ] **Análisis de Resultados** (§8): el análisis escrito de las gráficas y de la
      comparación teoría--simulación.
- [ ] **Preguntas de Control** (§9): las respuestas a las 10 preguntas de la guía. Las
      preguntas ya están listadas; falta el texto de cada respuesta.
- [ ] **Conclusiones** (§10): una por objetivo, atadas a los resultados.
- [ ] **Demostración** (§11): el enlace al video de demostración.
