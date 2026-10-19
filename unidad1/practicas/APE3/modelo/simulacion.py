# Simulación del sistema M/M/1 con SimPy.
import random
import simpy


class SistemaMM1:
    # Una fila con un solo servidor: los clientes llegan, esperan su turno
    # y el servidor los atiende uno por uno.

    def __init__(self, llegada, servicio, tiempo_total, semilla):
        self.llegada = llegada              # λ: clientes que llegan por unidad de tiempo
        self.servicio = servicio            # μ: clientes que atiende el servidor por unidad de tiempo
        self.tiempo_total = tiempo_total    # cuánto dura la simulación
        self.azar = random.Random(semilla)  # números aleatorios (la semilla permite repetirlos)

        self.esperas = []                   # lo que esperó cada cliente antes de ser atendido
        self.historial_cola = [(0, 0)]      # (instante, clientes en la cola) cada vez que cambia
        self.entorno = None
        self.servidor = None

    def ejecutar(self):
        self.entorno = simpy.Environment()                          # el reloj de la simulación
        self.servidor = simpy.Resource(self.entorno, capacity=1)    # un solo servidor
        self.entorno.process(self.generar_clientes())
        self.entorno.run(until=self.tiempo_total)
        self.anotar_cola()                                          # último dato al terminar

    def generar_clientes(self):
        # Cada vuelta del while es un cliente nuevo.
        # El yield hace que el reloj avance hasta que el cliente llega.
        while True:
            tiempo_entre_llegadas = self.azar.expovariate(self.llegada)
            yield self.entorno.timeout(tiempo_entre_llegadas)
            self.entorno.process(self.atender_cliente())

    def atender_cliente(self):
        hora_llegada = self.entorno.now
        with self.servidor.request() as turno:      # el cliente pide el servidor
            self.anotar_cola()
            yield turno                             # espera aquí hasta que el servidor esté libre
            self.esperas.append(self.entorno.now - hora_llegada)
            self.anotar_cola()                      # ya salió de la cola
            tiempo_servicio = self.azar.expovariate(self.servicio)
            yield self.entorno.timeout(tiempo_servicio)     # lo atienden
        # Al salir del with el servidor queda libre para el siguiente cliente

    def anotar_cola(self):
        # Guarda cuántos clientes están esperando en este momento
        self.historial_cola.append((self.entorno.now, len(self.servidor.queue)))

    def espera_promedio(self):
        if len(self.esperas) == 0:
            return 0
        return sum(self.esperas) / len(self.esperas)

    def cola_promedio(self):
        # El tamaño de la cola cambia con el tiempo, así que cada tamaño
        # se multiplica por el tiempo que duró y al final se divide entre el total.
        suma = 0
        for i in range(len(self.historial_cola) - 1):
            instante, tamano = self.historial_cola[i]
            siguiente_instante = self.historial_cola[i + 1][0]
            suma += tamano * (siguiente_instante - instante)
        return suma / self.tiempo_total
