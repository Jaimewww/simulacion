# Práctica 04: Modelo SIR en Java y NetLogo

Simulación de cómo se propaga una infección en una población, con el mismo modelo en dos herramientas: **Java** calcula y exporta los datos, y **NetLogo** los dibuja y corre además su propia simulación con movimiento.

| | |
|---|---|
| Estudiante | Jaime Alejandro Landazuri Roman |
| Asignatura | Simulación, ciclo 5 (Carrera de Computación, UNL) |
| Docente | José O. Guamán Q. |
| Práctica | 04: Análisis comparativo de herramientas de simulación mediante un modelo común |

**Contenido:** [1. Descripción](#1-descripción) · [2. Tecnologías](#2-tecnologías) · [3. Instalación y ejecución](#3-instalación-y-ejecución) · [4. Uso en NetLogo](#4-uso-en-netlogo) · [5. Configuración y reglas](#5-configuración-y-reglas) · [6. Estructura](#6-estructura-del-proyecto) · [7. Información adicional](#7-información-adicional)

---

## 1. Descripción

El modelo SIR divide una población de 100 personas en tres estados: susceptible (S), infectada (I) y recuperada (R). Cada persona pasa de S a I y de I a R, sin nacimientos, muertes ni reinfecciones.

La idea de la práctica es programar el mismo modelo en dos herramientas y comparar cómo se programa cada una, cómo se visualiza y qué resultados da. El flujo es este:

1. Java ejecuta la simulación y guarda los resultados en un CSV.
2. NetLogo importa ese CSV y lo grafica.
3. NetLogo corre también su propia simulación, con las personas moviéndose en pantalla, para compararla con la de Java.

La ficha menciona tres herramientas (Python con SimPy, Java y NetLogo). En esta entrega se implementan **Java y NetLogo**; la parte de Python y la comparación entre las tres quedan fuera.

Esta carpeta publica únicamente el código y este README. El informe individual se conserva por separado y no forma parte de esta entrega en GitHub. El código corresponde al [proyecto grupal de la práctica](https://github.com/RichardChambaS/Ape4_Simulacion).

## 2. Tecnologías

| Herramienta | Versión | Para qué se usa |
|---|---|---|
| Java (JDK) | 11 o posterior | Modelo, exportación de CSV y salida por consola. Solo biblioteca estándar. |
| NetLogo | 7.0.4 | Simulación con movimiento y gráficas. Usa la extensión `csv`, que ya viene incluida. |
| MVC | | Organización del código Java en modelo, vista y controlador. |

El modelo de NetLogo está en formato `.nlogox` (el de NetLogo 7). No le cambies la extensión a `.nlogo` a mano; los cambios del formato están en la [documentación oficial](https://docs.netlogo.org/versions).

## 3. Instalación y ejecución

Necesitas tener instalados un JDK y NetLogo de escritorio. No hace falta Maven, Gradle ni descargar librerías.

Abre una terminal en la carpeta `unidad1/practicas/APE4` del repositorio `Jaimewww/simulacion` y ejecuta:

```bash
javac -encoding UTF-8 --release 11 -d build src/Main.java src/modelo/*.java src/vista/*.java src/controlador/*.java
java -cp build Main
```

El programa imprime en consola una tabla cada diez pasos, el máximo de infectados, el tiempo en que ocurre y cuánto tardó el cálculo. También guarda las 101 filas (de t = 0 a t = 100) en estos archivos:

| Archivo | Contenido |
|---|---|
| `resultados/resultados_java.csv` | Resultados generados por Java. |
| `netlogo/resultados_java.csv` | Copia idéntica, para que NetLogo la pueda leer. |
| `resultados/parametros_java.csv` | Parámetros que usó Java. |
| `netlogo/parametros_java.csv` | Copia que NetLogo usa para quedar con los mismos parámetros. |

Cada vez que ejecutas Java estos archivos se reemplazan. Si cambias el código, vuelve a compilar antes de ejecutar.

## 4. Uso en NetLogo

1. Abre `netlogo/modelo_sir_netlogo.nlogox` con NetLogo 7.
2. Si quieres cambiar parámetros, edítalos en `src/modelo/SimulacionSIR.java`, compila y ejecuta Java desde la raíz del proyecto.
3. Pulsa **ACTUALIZAR JAVA**. NetLogo reinicia el escenario, lee los parámetros y los resultados que exportó Java y muestra los valores que quedaron activos. El botón **setup** carga los mismos archivos.
4. Pulsa **go**. Es un botón continuo: avanza la simulación de NetLogo hasta el tiempo 100, y si lo vuelves a pulsar la interrumpe.
5. Observa a las personas moverse y cómo se van armando las curvas paso a paso.
6. Al terminar, compara las curvas completas de Java y de NetLogo.

**Controles**

| Control | Qué hace |
|---|---|
| **setup** | Carga los mismos archivos que exportó Java. |
| **ACTUALIZAR JAVA** | Reinicia el escenario, recarga los archivos que exportó Java y reinicia también la curva de NetLogo, para que ambas simulaciones partan con los mismos parámetros. Antes hay que volver a ejecutar Java: el botón no lo compila ni lo ejecuta. |
| **go** | Avanza la simulación de NetLogo hasta t = 100 (modo continuo). |
| **PAUSA** | Espera en segundos entre pasos. Empieza en `0.00` y llega hasta `0.50` para verlo más despacio. No cambia los parámetros ni la unidad de tiempo. Tampoco debes cambiarle el nombre. |

También puedes bajar la velocidad con la barra de velocidad de NetLogo.

**Colores:** azul = susceptible, rojo = infectado, verde = recuperado. La etiqueta **P0** marca al paciente cero, que es una de las cinco personas infectadas al inicio, y se mantiene visible aunque se recupere.

## 5. Configuración y reglas

### Parámetros

| Parámetro | Valor de la ficha |
|---|---:|
| Población | 100 |
| Susceptibles iniciales | 95 |
| Infectados iniciales | 5 |
| Recuperados iniciales | 0 |
| Beta (probabilidad de contagio por contacto) | 0.30 |
| Gamma (probabilidad de recuperación por paso) | 0.10 |
| Tiempo máximo | 100 pasos |

Java es quien define los parámetros. Al ejecutarse exporta población, infectados iniciales, beta, gamma, tiempo máximo y semilla a `parametros_java.csv`, y NetLogo los lee al pulsar **setup** o **ACTUALIZAR JAVA**. Así, si cambias `GAMMA` en Java no hay que tocar NetLogo. La semilla actual es `42`.

Antes de simular se revisan los parámetros: la población debe ser un entero positivo, los infectados iniciales deben estar entre 0 y la población, beta y gamma deben estar entre 0 y 1, el tiempo no puede ser negativo y la semilla debe ser un entero. Si algo no cumple, Java avisa y no reemplaza los CSV anteriores. NetLogo también valida los parámetros y que los conteos del CSV sean enteros.

### Qué pasa en cada paso

1. Se copia el estado actual de las personas.
2. Cada infectado elige **un contacto** al azar entre las otras 99 personas.
3. Si ese contacto era susceptible al inicio del paso, se infecta con probabilidad beta.
4. El infectado se recupera con probabilidad gamma, haya contagiado o no.
5. Los cambios se aplican todos juntos y se registran S, I y R.

Algunos detalles de esta regla:

- Un recién infectado empieza a contagiar y a poder recuperarse desde el paso siguiente.
- Varios infectados pueden elegir al mismo contacto; esa persona se cuenta una sola vez.
- Un infectado puede contagiar y recuperarse en el mismo paso.
- Aunque ya no queden infectados, se sigue registrando hasta t = 100.

La ficha permite contactos cercanos o seleccionados. Aquí se eligen al azar entre toda la población para que la regla sea igual de simple en las dos herramientas. Por eso el movimiento en NetLogo es solo ilustrativo: **que dos figuras estén cerca no influye en el contagio**. El azar del movimiento está separado del azar de las reglas con `with-local-randomness`.

### Fundamento

```text
N = S + I + R

dS/dt = -beta * S * I / N
dI/dt =  beta * S * I / N - gamma * I
dR/dt =  gamma * I
```

No se resuelven las ecuaciones: se usa la alternativa discreta por agentes que propone la ficha, con beta y gamma como probabilidades por contacto y por paso. El valor `beta / gamma = 3` es una referencia de cuántos contagios produce, en promedio, un infectado; no es un número exacto que deba cumplirse en cada corrida.

## 6. Estructura del proyecto

```text
APE4/
├── README.md
├── src/
│   ├── Main.java
│   ├── modelo/
│   │   ├── Persona.java
│   │   └── SimulacionSIR.java
│   ├── vista/
│   │   └── VistaConsola.java
│   └── controlador/
│       └── SimulacionControlador.java
└── netlogo/
    └── modelo_sir_netlogo.nlogox
```

| Archivo o carpeta | Qué hace |
|---|---|
| `Main.java` | Inicia el controlador y avisa si hubo errores al guardar archivos. |
| `modelo/Persona.java` | Representa a una persona y sus tres estados posibles. |
| `modelo/SimulacionSIR.java` | Define los parámetros, aplica los cambios de estado y cuenta S, I y R. |
| `vista/VistaConsola.java` | Muestra parámetros y resultados en la terminal. |
| `controlador/SimulacionControlador.java` | Ejecuta el modelo y exporta resultados y parámetros para NetLogo. |
| `resultados/` | Datos calculados por Java. |
| `netlogo/` | Modelo visual con sus controles, código y gráficas, más las copias de los CSV. |

El flujo es `Main → controlador → modelo → vista`, y el controlador se encarga de la exportación. Al ejecutar Java se crean `resultados/` y los CSV de `netlogo/`; no se incluyen archivos generados en esta publicación. La carpeta `build/` guarda los archivos compilados en tu computador y tampoco se publica.

## 7. Información adicional

### Resultados y gráficas

Java guarda los resultados en un CSV de cuatro columnas:

```csv
tiempo,susceptibles,infectados,recuperados
0,95,5,0
```

El archivo no incluye posiciones ni historiales individuales, y lo escribe el propio programa Java. Al importarlo, NetLogo valida el encabezado, los tiempos, que los conteos sean enteros no negativos, el estado inicial y que la población se conserve.

NetLogo muestra cinco gráficas:

| Gráfica | Qué muestra |
|---|---|
| Evolucion Java | S, I y R importados del CSV. |
| Evolucion NetLogo | S, I y R calculados por la simulación de NetLogo. |
| Comparacion S | Susceptibles de Java y de NetLogo. |
| Comparacion I | Infectados de Java y de NetLogo. |
| Comparacion R | Recuperados de Java y de NetLogo. |

En las comparaciones, Java va en negro y NetLogo en naranja. La curva de Java se carga completa desde el inicio y la de NetLogo suma un punto por paso.

Valores de referencia con la configuración base de la ficha (gamma = 0.10, semilla 42). Si cambias los parámetros, cambian las curvas y estas cifras.

| Medida | Java | NetLogo 7.0.4 |
|---|---:|---:|
| Máximo de infectados | 29 | 44 |
| Primer tiempo con ese máximo | 31 | 11 |
| Susceptibles en t = 100 | 13 | 8 |
| Infectados en t = 100 | 0 | 0 |
| Recuperados en t = 100 | 87 | 92 |

Son los resultados de una sola corrida, no promedios. Aunque las reglas y los parámetros sean los mismos, la trayectoria no tiene por qué coincidir: Java y NetLogo usan generadores de números aleatorios distintos. La semilla permite repetir una ejecución dentro de cada herramienta, pero no hace que las dos generen los mismos números.

Para el análisis, las gráficas permiten ver cómo baja S, cómo sube y luego baja I, cómo crece R, cuándo ocurre el máximo de infectados y en qué se diferencian las dos herramientas, explicando el efecto del azar.

### Tiempo de ejecución

Java mide lo que tarda en calcular el modelo y contar los resultados, sin imprimir ni escribir archivos. El monitor de NetLogo suma solo el tiempo de actualizar los estados, sin movimiento, conteos para las gráficas, CSV ni pausas. Son medidas orientativas, no una comparación de rendimiento entre lenguajes.

### Verificación

- El código Java compila con `--release 11` y genera los CSV: 101 registros, con conteos enteros no negativos y población de 100.
- En las gráficas, S no aumenta, R no disminuye, cada una tiene los puntos esperados, recargar no los duplica y **setup** repite la ejecución con la misma semilla.
- La simulación de NetLogo tiene movimiento y **go** está en modo continuo; se detiene al llegar a t = 100.
- La sincronización visual hay que probarla abriendo el modelo en NetLogo 7.0.4 y pulsando **ACTUALIZAR JAVA**.

### Nota sobre la ficha

La rúbrica de la ficha menciona un modelo M/M/1, pero es un error de la guía: esta práctica usa el modelo SIR.

### Entrega

Se publican los fuentes Java, el modelo NetLogo y el README. Se excluyen el informe (LaTeX y PDF), la guía, las figuras, los CSV y los archivos compilados. Para obtener los CSV, ejecuta Java antes de abrir la comparación en NetLogo.
