# Escenarios de la práctica.
# Cada escenario tiene su propio bloque: para cambiarlo solo se editan sus números.


class Escenario:
    # Guarda los datos de un escenario
    def __init__(self, nombre, llegada, servicio, condicion):
        self.nombre = nombre
        self.llegada = llegada      # λ: clientes que llegan por unidad de tiempo
        self.servicio = servicio    # μ: clientes que atiende el servidor por unidad de tiempo
        self.condicion = condicion


escenario_1 = Escenario(
    nombre="Escenario 1",
    llegada=2.0,
    servicio=3.0,
    condicion="Sistema estable",
)

escenario_2 = Escenario(
    nombre="Escenario 2",
    llegada=2.5,
    servicio=3.0,
    condicion="Mayor utilización",
)

escenario_3 = Escenario(
    nombre="Escenario 3",
    llegada=2.9,
    servicio=3.0,
    condicion="Cerca de saturación",
)

# Lista que recorre el programa. Si se agrega un escenario nuevo, se pone aquí.
ESCENARIOS = [escenario_1, escenario_2, escenario_3]
