import controlador.SimulacionControlador;
import java.io.IOException;

public class Main {
    // Inicia el programa y comunica parámetros inválidos o errores de escritura.
    public static void main(String[] args) {
        try {
            new SimulacionControlador().ejecutar();
        } catch (IllegalArgumentException e) {
            System.err.println("Parámetros inválidos: " + e.getMessage());
            System.exit(1);
        } catch (IOException e) {
            System.err.println("No se pudo guardar el CSV: " + e.getMessage());
            System.exit(1);
        }
    }
}
