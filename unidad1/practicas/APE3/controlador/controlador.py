# Controlador: recorre los escenarios, los simula y le pasa los resultados a la vista.
from modelo.escenarios import ESCENARIOS
from modelo.teoria import TeoriaMM1
from modelo.simulacion import SistemaMM1
from vista import tabla, graficas

TIEMPO_SIMULACION = 5000    # cuánto tiempo se simula cada vez
REPETICIONES = 10           # veces que se repite cada escenario (con distinta semilla)
SEMILLA = 42                # número base para que los resultados se puedan repetir


class Controlador:
    def ejecutar(self):
        resultados = []
        for escenario in ESCENARIOS:
            teoria = TeoriaMM1(escenario.llegada, escenario.servicio)

            # Si λ >= μ no se puede simular, se avisa y se sigue con el siguiente
            if not teoria.es_estable():
                tabla.mostrar_no_estable(escenario)
                continue

            print(f"Simulando {escenario.nombre}...")
            resultados.append(self.simular_escenario(escenario, teoria))

        if len(resultados) == 0:
            return

        tabla.mostrar_teoria(resultados)
        tabla.mostrar_comparacion(resultados)

        # Las gráficas se muestran una por una (cerrar la ventana para ver la siguiente)
        graficas.grafica_cola(resultados)
        graficas.grafica_esperas(resultados)
        graficas.grafica_comparacion(resultados)

    def simular_escenario(self, escenario, teoria):
        # Se simula varias veces porque una sola corrida cambia mucho por el azar
        sistemas = []
        for i in range(REPETICIONES):
            sistema = SistemaMM1(escenario.llegada, escenario.servicio,
                                 TIEMPO_SIMULACION, SEMILLA + i)
            sistema.ejecutar()
            sistemas.append(sistema)

        esperas = [s.espera_promedio() for s in sistemas]
        colas = [s.cola_promedio() for s in sistemas]

        return {
            "escenario": escenario,
            "teoria": teoria,
            "espera_simulada": sum(esperas) / len(esperas),
            "cola_simulada": sum(colas) / len(colas),
            "ejemplo": sistemas[0],     # una de las corridas, para las gráficas
        }
