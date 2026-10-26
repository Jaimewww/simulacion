package modelo;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import modelo.Persona.Estado;

public class SimulacionSIR {
    // Valores de la ficha. Cada paso representa una unidad de tiempo.
    public static final int POBLACION = 100;
    public static final int INFECTADOS_INICIALES = 5;
    public static final double BETA = 0.30;
    public static final double GAMMA = 0.10;
    public static final int TIEMPO_SIMULACION = 100;
    public static final long SEMILLA = 42;

    // Crea la población y registra los resultados desde el tiempo 0 hasta el final.
    public List<int[]> ejecutar() {
        validarParametros();
        // La semilla permite repetir la misma ejecución.
        Random azar = new Random(SEMILLA);
        Persona[] personas = new Persona[POBLACION];
        for (int i = 0; i < POBLACION; i++) {
            personas[i] = new Persona(i < INFECTADOS_INICIALES
                    ? Estado.INFECTADO : Estado.SUSCEPTIBLE);
        }
        // La persona de índice 0 es el paciente cero, entre los cinco iniciales.
        List<int[]> resultados = new ArrayList<>();
        resultados.add(contar(personas, 0));

        for (int tiempo = 1; tiempo <= TIEMPO_SIMULACION; tiempo++) {
            avanzar(personas, azar);
            resultados.add(contar(personas, tiempo));
        }
        return resultados;
    }

    // Calcula los contagios y las recuperaciones de un paso.
    private void avanzar(Persona[] personas, Random azar) {
        // Conserva los cambios pendientes sin modificar todavía los estados actuales.
        Estado[] siguientes = new Estado[POBLACION];
        for (int i = 0; i < POBLACION; i++) {
            siguientes[i] = personas[i].getEstado();
        }

        for (int i = 0; i < POBLACION; i++) {
            if (personas[i].getEstado() != Estado.INFECTADO) {
                continue;
            }

            // Un contacto por infectado y paso, elegido entre las otras personas.
            if (POBLACION > 1) {
                int contacto = azar.nextInt(POBLACION - 1);
                if (contacto >= i) {
                    contacto++;
                }
                if (personas[contacto].getEstado() == Estado.SUSCEPTIBLE
                        && azar.nextDouble() < BETA) {
                    siguientes[contacto] = Estado.INFECTADO;
                }
            }
            // Cada infectado tiene una oportunidad de recuperarse en este paso.
            if (azar.nextDouble() < GAMMA) {
                siguientes[i] = Estado.RECUPERADO;
            }
        }

        // Se aplican todos los cambios juntos, usando el estado anterior.
        for (int i = 0; i < POBLACION; i++) {
            personas[i].setEstado(siguientes[i]);
        }
    }

    private void validarParametros() {
        if (POBLACION < 1) {
            throw new IllegalArgumentException("POBLACION debe ser un entero positivo.");
        }
        if (INFECTADOS_INICIALES < 0 || INFECTADOS_INICIALES > POBLACION) {
            throw new IllegalArgumentException("INFECTADOS_INICIALES debe estar entre 0 y POBLACION.");
        }
        if (!Double.isFinite(BETA) || BETA < 0 || BETA > 1) {
            throw new IllegalArgumentException("BETA debe ser un número finito entre 0 y 1.");
        }
        if (!Double.isFinite(GAMMA) || GAMMA < 0 || GAMMA > 1) {
            throw new IllegalArgumentException("GAMMA debe ser un número finito entre 0 y 1.");
        }
        if (TIEMPO_SIMULACION < 0) {
            throw new IllegalArgumentException("TIEMPO_SIMULACION debe ser un entero no negativo.");
        }
        if (SEMILLA < Integer.MIN_VALUE || SEMILLA > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("SEMILLA debe estar entre -2147483648 y 2147483647 para NetLogo.");
        }
    }

    // Cuenta las personas de cada estado y devuelve una fila para el CSV.
    private int[] contar(Persona[] personas, int tiempo) {
        int susceptibles = 0;
        int infectados = 0;
        int recuperados = 0;
        for (Persona persona : personas) {
            switch (persona.getEstado()) {
                case SUSCEPTIBLE: susceptibles++; break;
                case INFECTADO: infectados++; break;
                case RECUPERADO: recuperados++; break;
            }
        }
        // Columnas del CSV: tiempo, S, I, R.
        return new int[] {tiempo, susceptibles, infectados, recuperados};
    }
}
