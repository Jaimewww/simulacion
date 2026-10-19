# Valores teóricos del modelo M/M/1 (las fórmulas de la guía).


class TeoriaMM1:
    def __init__(self, llegada, servicio):
        self.llegada = llegada
        self.servicio = servicio
        self.rho = llegada / servicio   # utilización: qué tan ocupado está el servidor

        # Las fórmulas solo sirven si el sistema es estable (λ < μ)
        if self.es_estable():
            diferencia = servicio - llegada
            self.L = llegada / diferencia                          # clientes en el sistema
            self.Lq = llegada ** 2 / (servicio * diferencia)       # clientes en la cola
            self.W = 1 / diferencia                                # tiempo en el sistema
            self.Wq = llegada / (servicio * diferencia)            # tiempo de espera en la cola

    def es_estable(self):
        # Si llegan más clientes de los que se pueden atender, la cola crece sin parar
        return self.llegada < self.servicio
