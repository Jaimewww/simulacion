package modelo;

public class Persona {
    // Estados posibles de una persona durante la simulación.
    public enum Estado { SUSCEPTIBLE, INFECTADO, RECUPERADO }

    private Estado estado;

    // Crea una persona con su estado inicial.
    public Persona(Estado estado) {
        this.estado = estado;
    }

    // Consulta el estado actual.
    public Estado getEstado() {
        return estado;
    }

    // Actualiza el estado después de un paso.
    public void setEstado(Estado estado) {
        this.estado = estado;
    }
}
