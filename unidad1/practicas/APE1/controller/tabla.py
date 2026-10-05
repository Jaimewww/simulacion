"""Build and print the hourly simulation table."""

import controller.utils as utils
import models.datasets as datasets


def construir_tabla(coeficientes=None):
    """Return one row per hour with H, N, Tf, index and rain state."""
    filas = []
    for hora, humedad, nubosidad, temp in datasets.DATOS_HORARIOS:
        H = humedad / 100.0
        N = nubosidad / 100.0
        Tf = utils.tf_dict(temp, datasets.tabla_tf)
        valor = utils.indice(H, N, Tf, coeficientes)
        filas.append(
            {
                "hora": hora,
                "humedad": humedad,
                "nubosidad": nubosidad,
                "temp": temp,
                "H": H,
                "N": N,
                "Tf": Tf,
                "indice": valor,
                "estado": utils.clasificar(valor),
            }
        )
    return filas


def imprimir_tabla(filas, titulo):
    """Print a formatted table to standard output."""
    print(f"\n{titulo}")
    encabezado = (
        f"{'Hora':<6} {'Humedad':>8} {'Nubosidad':>10} {'Temp.':>6} "
        f"{'H':>6} {'N':>6} {'Tf':>6} {'Indice':>8}  Estado"
    )
    print(encabezado)
    print("-" * len(encabezado))
    for f in filas:
        print(
            f"{f['hora']:<6} {f['humedad']:>8} {f['nubosidad']:>10} {f['temp']:>6} "
            f"{f['H']:>6.2f} {f['N']:>6.2f} {f['Tf']:>6.2f} {f['indice']:>8.3f}"
            f"  {f['estado']}"
        )
