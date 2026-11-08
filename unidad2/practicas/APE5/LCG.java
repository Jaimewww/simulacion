import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

/**
 * LCG (Linear Congruential Generator) - Practica 05, Simulacion U2.
 *
 * Implementa el mismo algoritmo que lcg.py para comparar secuencias:
 *     X(n+1) = (a * X(n) + c) mod m
 *     U(n)   = X(n) / m
 *
 * Parametros: a = 1664525, c = 1013904223, m = 2^32, semilla = 12345.
 *
 * Detalle critico: a * state puede desbordar el rango de int e incluso
 * acercarse al limite de long. Se usa arithmetic modular manual con la
 * mascara & 0xFFFFFFFFL y multiplicacion en "pedazos" para evitar overflow:
 * como todos los valores son < 2^32, se descompone a * x mod 2^32 en
 * (a_lo * x_lo + ((a_lo * x_hi + a_hi * x_lo) & 0xFFFFFFFF) << 16) mod 2^32.
 *
 * Uso: java LCG.java            (semilla 12345)
 *      java LCG.java 54321      (otra semilla)
 */
public class LCG {

    static final long A = 1664525L;
    static final long C = 1013904223L;
    static final long M = 4294967296L; // 2^32
    static final int N = 10_000;

    private final long a, c, m;
    private long state;

    public LCG(long a, long c, long m, long seed) {
        this.a = a;
        this.c = c;
        this.m = m;
        this.state = seed % m;
    }

    // Multiplica dos valores < 2^32 y devuelve el modulo 2^32 del producto
    // sin overflow de long (el producto real puede llegar a ~2^64).
    static long mulMod32(long x, long y) {
        long xHi = x >>> 16;          // 16 bits altos
        long xLo = x & 0xFFFFL;       // 16 bits bajos
        long yHi = y >>> 16;
        long yLo = y & 0xFFFFL;
        // Todos los productos parciales <= (2^16)^2 = 2^32 -> no desbordan long.
        long ll = xLo * yLo;
        long lh = xLo * yHi;
        long hl = xHi * yLo;
        long mid = (lh + hl) & 0xFFFFFFFFL; // solo importan los bits < 32
        long result = ll + (mid << 16);
        return result & 0xFFFFFFFFL;
    }

    /** Siguiente X entero crudo en [0, m). */
    public long nextX() {
        state = (mulMod32(a, state) + c) % m;
        return state;
    }

    /** Siguiente valor normalizado U = X / m en [0, 1). */
    public double nextU() {
        return (double) nextX() / (double) m;
    }

    /** Genera n valores crudos X (los U se derivan). */
    public long[] generateX(int n) {
        long[] xs = new long[n];
        for (int i = 0; i < n; i++) {
            xs[i] = nextX();
        }
        return xs;
    }

    /** Guarda las primeras `rows` observaciones (formato igual al CSV de Python). */
    static void saveCsv(long[] xs, String path, int rows) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(Path.of(path))) {
            w.write("n,X(n),U(n)\n");
            for (int i = 0; i < rows; i++) {
                w.write((i + 1) + "," + xs[i] + ","
                        + String.format(Locale.ROOT, "%.10f", (double) xs[i] / (double) M) + "\n");
            }
        }
    }

    static void saveFullCsv(long[] xs, String path) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(Path.of(path))) {
            w.write("index,X,U\n");
            for (int i = 0; i < xs.length; i++) {
                w.write(i + "," + xs[i] + ","
                        + String.format(Locale.ROOT, "%.10f", (double) xs[i] / (double) M) + "\n");
            }
        }
    }

    public static void main(String[] args) throws IOException {
        long seed = args.length > 0 ? Long.parseLong(args[0]) : 12345L;
        String tag = String.valueOf(seed);

        LCG g = new LCG(A, C, M, seed);
        long[] xs = g.generateX(N);

        Path dir = Path.of("resultados");
        Files.createDirectories(dir);
        saveCsv(xs, dir.resolve("java_primeras20_" + tag + ".csv").toString(), 20);
        saveFullCsv(xs, dir.resolve("java_10000_" + tag + ".csv").toString());

        System.out.println("Parametros: a=" + A + "  c=" + C + "  m=" + M
                + " (2^32)   semilla=" + seed);
        System.out.println("Generados " + N + " valores.");
        System.out.println();
        System.out.println("Primeras 10 observaciones:");
        for (int i = 0; i < 10; i++) {
            System.out.printf("  X[%d] = %10d   U[%d] = %.10f%n",
                    i, xs[i], i, (double) xs[i] / (double) M);
        }
    }
}
