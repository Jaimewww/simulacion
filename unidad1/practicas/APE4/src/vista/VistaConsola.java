package vista;

import java.util.List;
import modelo.SimulacionSIR;

public class VistaConsola {
    // Muestra los parámetros, la tabla resumida y el máximo de infectados.
    public void mostrar(List<int[]> resultados, double segundos) {
        System.out.println("PRÁCTICA 04 - MODELO SIR EN JAVA");
        System.out.printf("Población: %d | Infectados iniciales: %d%n",
                SimulacionSIR.POBLACION, SimulacionSIR.INFECTADOS_INICIALES);
        System.out.printf("Beta: %.2f | Gamma: %.2f | Pasos: %d | Semilla: %d%n",
                SimulacionSIR.BETA, SimulacionSIR.GAMMA,
                SimulacionSIR.TIEMPO_SIMULACION, SimulacionSIR.SEMILLA);
        System.out.println("S: susceptibles | I: infectados | R: recuperados");
        System.out.printf("%6s %6s %6s %6s%n", "Tiempo", "S", "I", "R");
        // Imprime cada diez pasos y busca el primer máximo de infectados.
        int[] pico = resultados.get(0);
        for (int[] fila : resultados) {
            if (fila[0] % 10 == 0 || fila == resultados.get(resultados.size() - 1)) {
                System.out.printf("%6d %6d %6d %6d%n", fila[0], fila[1], fila[2], fila[3]);
            }
            if (fila[2] > pico[2]) {
                pico = fila;
            }
        }
        System.out.printf("Máximo de infectados: %d en el tiempo %d.%n", pico[2], pico[0]);
        System.out.printf("Tiempo de cálculo (sin escribir archivos): %.6f s%n", segundos);
        System.out.println("CSV: resultados/resultados_java.csv");
        System.out.println("Copia para NetLogo: netlogo/resultados_java.csv");
        System.out.println("Parámetros para NetLogo: netlogo/parametros_java.csv");
    }
}
