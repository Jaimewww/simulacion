"""Console entry point for the atmospheric-rainfall simulation (APE1).

Runs the whole practice: builds and prints the hourly table for the original
and the adjusted model, generates the charts, and then offers the original
single-shot interactive query.
"""

import argparse

import controller.tabla as tabla
import controller.utils as utils
import models.datasets as datasets
import views.graficas as graficas


def consulta_interactiva():
    """Original base behaviour: query one hour and classify it."""
    H = float(input("Ingrese el porcentaje de humedad (0-100): ")) * 0.01
    N = float(input("Ingrese el porcentaje de nubes (0-100): ")) * 0.01
    Tf = utils.tf_dict(float(input("Ingrese la temperatura en °C: ")), datasets.tabla_tf)
    valor = utils.indice(H, N, Tf)
    print(f"El indice atmosferico es: {valor:.3f} ({utils.clasificar(valor)})")


def main():
    parser = argparse.ArgumentParser(description="Simulacion atmosferica - APE1")
    parser.add_argument(
        "--interactivo",
        action="store_true",
        help="Al terminar, pedir humedad, nubosidad y temperatura por consola.",
    )
    args = parser.parse_args()

    original = tabla.construir_tabla(datasets.COEFICIENTES_ORIGINAL)
    ajustado = tabla.construir_tabla(datasets.COEFICIENTES_AJUSTADO)

    tabla.imprimir_tabla(
        original, "Modelo original: I = 0.50H + 0.30N + 0.20Tf"
    )
    tabla.imprimir_tabla(
        ajustado, "Modelo ajustado: I = 0.40H + 0.35N + 0.25Tf"
    )

    archivos = graficas.generar(original, ajustado)
    print(f"\nGraficas generadas en dist/: {', '.join(archivos)}")

    if args.interactivo:
        consulta_interactiva()


if __name__ == "__main__":
    main()
