"""Console entry point for the population simulation (APE2).

Runs the four models over the observed period grid, prints the comparison
table and the metrics, and generates the charts and the CSV in ``dist/``.

Usage:
    python -m views.main
    python -m views.main --no-show --r 0.15 --seed 7
"""

import argparse

import controller.modelos as modelos
import models.parametros as parametros
import views.graficas as graficas


def imprimir_tabla(resultados):
    """Print the period table with the observed data and the four models."""
    cabecera = (
        f"{'Periodo':>8} {'Observado':>10} {'Determinista':>13} "
        f"{'Discreto':>10} {'Estocastico':>12} {'Euler':>10}"
    )
    print("\nTabla de resultados")
    print(cabecera)
    print("-" * len(cabecera))
    for i, periodo in enumerate(resultados["periodos"]):
        print(
            f"{periodo:>8d} "
            f"{resultados['observado'][i]:>10.2f} "
            f"{resultados['deterministico'][i]:>13.2f} "
            f"{resultados['discreto'][i]:>10.2f} "
            f"{resultados['estocastico'][i]:>12.2f} "
            f"{resultados['euler'][i]:>10.2f}"
        )
    print("-" * len(cabecera))


def imprimir_metricas(resumen):
    """Print the final population, growth factor and RMSE per model."""
    print("\nValores finales y factor de crecimiento discreto")
    print(f"  Factor de crecimiento discreto (1 + r): {resumen['factor_crecimiento']:.4f}")
    for nombre, datos in resumen["modelos"].items():
        print(f"  {nombre.capitalize():<15} valor final = {datos['final']:.2f}")

    print("\nError cuadratico medio (RMSE) contra la serie observada")
    for nombre, datos in resumen["modelos"].items():
        print(f"  {nombre.capitalize():<15} RMSE = {datos['rmse']:.2f}")


def imprimir_estimacion(estimado, p0, observado, periodos):
    """Print the estimated rates and the RMSE of the two fitted models."""
    print("\nEstimación de la tasa r a partir de los datos observados")
    print(f"  Tasa discreta (media de las razones - 1): {estimado['discreto']:.4f}")
    print(f"  Tasa continua (pendiente de ln P vs t):   {estimado['continuo']:.4f}")
    print(f"  Factor de crecimiento medio:              {estimado['factor_medio']:.4f}")

    observado = list(observado)[: periodos + 1]
    discreto_ajustado = modelos.discreto(p0, estimado["discreto"], periodos)
    determinista_ajustado = modelos.determinista_periodos(p0, estimado["continuo"], periodos)
    print("\nError cuadratico medio (RMSE) de los modelos ajustados contra la serie observada")
    print(
        "  Discreto ajustado       RMSE = "
        f"{modelos.error_cuadratico_medio(discreto_ajustado, observado):.2f}"
    )
    print(
        "  Deterministico ajustado RMSE = "
        f"{modelos.error_cuadratico_medio(determinista_ajustado, observado):.2f}"
    )


def main():
    parser = argparse.ArgumentParser(description="Simulacion de poblacion - APE2")
    parser.add_argument("--p0", type=float, default=parametros.P0, help="Poblacion inicial")
    parser.add_argument("--r", type=float, default=parametros.R, help="Tasa de crecimiento")
    parser.add_argument("--sigma", type=float, default=parametros.SIGMA, help="Ruido del modelo estocastico")
    parser.add_argument("--dt", type=float, default=parametros.DT, help="Paso de integracion de Euler")
    parser.add_argument("--periodos", type=int, default=parametros.PERIODOS, help="Numero de periodos")
    parser.add_argument("--seed", type=int, default=parametros.SEED, help="Semilla del generador aleatorio")
    parser.add_argument(
        "--ajustar-r",
        action="store_true",
        help="Estimar r desde los datos observados y usarla en toda la corrida",
    )
    parser.add_argument("--no-show", action="store_true", help="No mostrar las figuras en pantalla")
    args = parser.parse_args()

    mostrar = not args.no_show

    estimado = modelos.estimar_r(parametros.datos)
    imprimir_estimacion(estimado, p0=args.p0, observado=parametros.datos, periodos=args.periodos)

    r = args.r
    if args.ajustar_r:
        r = estimado["discreto"]
        print("\nTasa r usada en la corrida (--ajustar-r)")
        print(f"  r estimada (discreta) = {r:.4f} en lugar de r = {args.r:.4f}")

    resultados = modelos.comparar(
        p0=args.p0,
        r=r,
        sigma=args.sigma,
        dt=args.dt,
        periodos=args.periodos,
        observado=parametros.datos,
        seed=args.seed,
    )
    resumen = modelos.metricas(resultados, r)

    imprimir_tabla(resultados)
    imprimir_metricas(resumen)

    archivos = graficas.generar(
        resultados,
        p0=args.p0,
        r=r,
        sigma=args.sigma,
        dt=args.dt,
        periodos=args.periodos,
        seed=args.seed,
        mostrar=mostrar,
    )
    print("\nArchivos generados en dist/:")
    for archivo in archivos:
        print(f"  - {archivo}")


if __name__ == "__main__":
    main()
