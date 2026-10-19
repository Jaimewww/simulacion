# Tablas que se muestran en la consola.

# Qué significa cada variable. Se imprime entre paréntesis encima de cada tabla
# para que la salida se entienda sin tener que buscar la notación en el informe.
SIGNIFICADOS = {
    "llegada": "λ (tasa de llegada de clientes)",
    "servicio": "μ (tasa de servicio del servidor)",
    "rho": "ρ (utilización del servidor)",
    "L": "L (clientes en el sistema)",
    "Lq": "Lq (clientes en la cola)",
    "W": "W (tiempo en el sistema)",
    "Wq": "Wq (tiempo de espera en la cola)",
    "diferencia": "Dif % (diferencia frente al valor teórico)",
}

ANCHO_LEYENDA = 80   # a partir de este ancho la leyenda sigue en otra línea


def mostrar_leyenda(partes):
    # Escribe los significados separados por dos espacios, partiendo la línea
    # cuando se pasa del ancho para que no quede una sola línea larguísima.
    linea = []
    largo = 0
    for parte in partes:
        agregado = len(parte) + (2 if linea else 0)
        if linea and largo + agregado > ANCHO_LEYENDA:
            print("  ".join(linea))
            linea = [parte]
            largo = len(parte)
        else:
            linea.append(parte)
            largo += agregado
    if linea:
        print("  ".join(linea))


def mostrar_no_estable(escenario):
    print(f"\n{escenario.nombre}: {SIGNIFICADOS['llegada']} = {escenario.llegada} no es menor "
          f"que {SIGNIFICADOS['servicio']} = {escenario.servicio}. El sistema no es estable.")


def mostrar_teoria(resultados):
    print("\n=== Valores teóricos ===")
    mostrar_leyenda([SIGNIFICADOS["llegada"], SIGNIFICADOS["servicio"], SIGNIFICADOS["rho"],
                     SIGNIFICADOS["L"], SIGNIFICADOS["Lq"], SIGNIFICADOS["W"], SIGNIFICADOS["Wq"]])
    print()
    print(f"{'Escenario':<14}{'λ':>6}{'μ':>6}{'ρ':>9}{'L':>9}{'Lq':>9}{'W':>9}{'Wq':>9}")
    for r in resultados:
        e = r["escenario"]
        t = r["teoria"]
        print(f"{e.nombre:<14}{e.llegada:>6}{e.servicio:>6}{t.rho:>9.3f}"
              f"{t.L:>9.3f}{t.Lq:>9.3f}{t.W:>9.3f}{t.Wq:>9.3f}")


def mostrar_comparacion(resultados):
    print("\n=== Teoría vs simulación ===")
    mostrar_leyenda([SIGNIFICADOS["Wq"], SIGNIFICADOS["Lq"], SIGNIFICADOS["diferencia"]])
    print()
    print(f"{'Escenario':<14}{'Wq teórico':>12}{'Wq simulado':>13}{'Dif %':>8}"
          f"{'Lq teórico':>13}{'Lq simulado':>13}{'Dif %':>8}")
    for r in resultados:
        e = r["escenario"]
        t = r["teoria"]
        dif_espera = (r["espera_simulada"] - t.Wq) / t.Wq * 100
        dif_cola = (r["cola_simulada"] - t.Lq) / t.Lq * 100
        print(f"{e.nombre:<14}{t.Wq:>12.3f}{r['espera_simulada']:>13.3f}{dif_espera:>8.1f}"
              f"{t.Lq:>13.3f}{r['cola_simulada']:>13.3f}{dif_cola:>8.1f}")
