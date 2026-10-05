/**
 * Atmospheric-rainfall model simulation (APE1).
 *
 * Mirrors the Python implementation: builds the hourly table for the original
 * and the adjusted model, prints it, exports a CSV and draws the index chart.
 *
 * Compile: javac -d build/java java/SimulacionAtmosferica.java
 * Run:     java -cp build/java SimulacionAtmosferica
 */
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.PrintWriter;
import java.util.LinkedHashMap;
import java.util.Locale;
import javax.imageio.ImageIO;

public class SimulacionAtmosferica {

    /** Temperature factor (Tf) by temperature in Celsius, from the guide. */
    static final LinkedHashMap<Integer, Double> TABLA_TF = new LinkedHashMap<>();
    static {
        TABLA_TF.put(10, 1.00);
        TABLA_TF.put(12, 0.90);
        TABLA_TF.put(14, 0.80);
        TABLA_TF.put(16, 0.70);
        TABLA_TF.put(18, 0.60);
        TABLA_TF.put(20, 0.50);
        TABLA_TF.put(22, 0.40);
        TABLA_TF.put(24, 0.30);
        TABLA_TF.put(26, 0.20);
        TABLA_TF.put(28, 0.10);
    }

    /** Hourly observations: {hora, humedad %, nubosidad %, temperatura °C}. */
    static final Object[][] DATOS = {
        {"06:00", 65, 40, 14},
        {"08:00", 70, 50, 16},
        {"10:00", 68, 45, 18},
        {"12:00", 60, 30, 22},
        {"14:00", 75, 70, 20},
        {"16:00", 85, 85, 18},
        {"18:00", 92, 95, 16},
        {"20:00", 88, 90, 17},
        {"22:00", 80, 75, 15},
    };

    // Coefficients: original from the guide, adjusted randomly, both sum to 1.
    static final double[] COEF_ORIGINAL = {0.50, 0.30, 0.20};
    static final double[] COEF_AJUSTADO = {0.40, 0.35, 0.25};

    /** One computed row of the table. */
    record Fila(String hora, int humedad, int nubosidad, int temp,
                double h, double n, double tf, double indice, String estado) {}

    /** Temperature factor for a temperature in Celsius (2 °C steps). */
    static double tfDic(int temp) {
        if (temp <= 10) return TABLA_TF.get(10);
        if (temp >= 28) return TABLA_TF.get(28);
        // rint = round half to even, matching Python's built-in round().
        int par = (int) Math.rint(temp / 2.0) * 2;
        return TABLA_TF.get(par);
    }

    /** Atmospheric index I = aH + bN + cTf. */
    static double indice(double h, double n, double tf, double[] c) {
        return c[0] * h + c[1] * n + c[2] * tf;
    }

    /** Rain state for an index value, following the guide rules. */
    static String clasificar(double valor) {
        if (valor < 0.40) return "Sin lluvia";
        if (valor < 0.60) return "Baja posibilidad";
        if (valor < 0.75) return "Lluvia probable";
        return "Lluvia";
    }

    static Fila[] construirTabla(double[] coeficientes) {
        Fila[] filas = new Fila[DATOS.length];
        for (int i = 0; i < DATOS.length; i++) {
            String hora = (String) DATOS[i][0];
            int humedad = (int) DATOS[i][1];
            int nubosidad = (int) DATOS[i][2];
            int temp = (int) DATOS[i][3];
            double h = humedad / 100.0;
            double n = nubosidad / 100.0;
            double tf = tfDic(temp);
            double valor = indice(h, n, tf, coeficientes);
            filas[i] = new Fila(hora, humedad, nubosidad, temp, h, n, tf, valor, clasificar(valor));
        }
        return filas;
    }

    static void imprimir(Fila[] filas, String titulo) {
        System.out.println();
        System.out.println(titulo);
        System.out.printf("%-6s %8s %10s %6s %6s %6s %6s %8s  %s%n",
                "Hora", "Humedad", "Nubosidad", "Temp.", "H", "N", "Tf", "Indice", "Estado");
        System.out.println("-".repeat(80));
        for (Fila f : filas) {
            System.out.printf("%-6s %8d %10d %6d %6.2f %6.2f %6.2f %8.3f  %s%n",
                    f.hora(), f.humedad(), f.nubosidad(), f.temp(),
                    f.h(), f.n(), f.tf(), f.indice(), f.estado());
        }
    }

    static void escribirCsv(PrintWriter out, String modelo, Fila[] filas) {
        for (Fila f : filas) {
            out.printf("%s,%s,%d,%d,%d,%.2f,%.2f,%.2f,%.3f,%s%n",
                    modelo, f.hora(), f.humedad(), f.nubosidad(), f.temp(),
                    f.h(), f.n(), f.tf(), f.indice(), f.estado());
        }
    }

    static void exportarCsv(Fila[] original, Fila[] ajustado, File destino) throws Exception {
        try (PrintWriter out = new PrintWriter(destino, "UTF-8")) {
            out.println("modelo,hora,humedad,nubosidad,temp,H,N,Tf,indice,estado");
            escribirCsv(out, "original", original);
            escribirCsv(out, "ajustado", ajustado);
        }
    }

    static void dibujarUmbral(Graphics2D g, double valor, Color color,
                              int left, int right, int top, int bottom) {
        int y = bottom - (int) Math.round((bottom - top) * valor);
        g.setColor(color);
        g.setStroke(new BasicStroke(1f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER,
                10f, new float[]{6f, 6f}, 0f));
        g.drawLine(left, y, right, y);
        g.drawString(String.format("%.2f", valor), left - 55, y + 4);
    }

    /** Draw a simple line chart with Java2D; no external libraries needed. */
    static void graficar(Fila[] filas, String titulo, File destino) throws Exception {
        int w = 900;
        int h = 500;
        BufferedImage img = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, w, h);

        int left = 70;
        int right = w - 30;
        int top = 50;
        int bottom = h - 60;

        g.setColor(Color.DARK_GRAY);
        g.drawLine(left, top, left, bottom);
        g.drawLine(left, bottom, right, bottom);

        dibujarUmbral(g, 0.40, Color.GRAY, left, right, top, bottom);
        dibujarUmbral(g, 0.60, Color.ORANGE, left, right, top, bottom);
        dibujarUmbral(g, 0.75, Color.RED, left, right, top, bottom);

        int n = filas.length;
        int[] xs = new int[n];
        int[] ys = new int[n];
        for (int i = 0; i < n; i++) {
            xs[i] = left + (int) Math.round((right - left) * i / (double) (n - 1));
            ys[i] = bottom - (int) Math.round((bottom - top) * filas[i].indice());
        }

        g.setColor(new Color(59, 130, 246));
        g.setStroke(new BasicStroke(2.5f));
        for (int i = 0; i < n - 1; i++) {
            g.drawLine(xs[i], ys[i], xs[i + 1], ys[i + 1]);
        }
        for (int i = 0; i < n; i++) {
            g.fillOval(xs[i] - 4, ys[i] - 4, 8, 8);
            g.setColor(Color.BLACK);
            g.drawString(filas[i].hora(), xs[i] - 14, bottom + 18);
            g.setColor(new Color(59, 130, 246));
        }

        g.setColor(Color.BLACK);
        g.setFont(new Font("SansSerif", Font.BOLD, 16));
        g.drawString(titulo, left, 30);

        g.dispose();
        ImageIO.write(img, "png", destino);
    }

    public static void main(String[] args) throws Exception {
        // Keep console/CSV decimals with a dot, matching the Python output.
        Locale.setDefault(Locale.US);
        System.setProperty("java.awt.headless", "true");

        Fila[] original = construirTabla(COEF_ORIGINAL);
        Fila[] ajustado = construirTabla(COEF_AJUSTADO);

        imprimir(original, "Modelo original: I = 0.50H + 0.30N + 0.20Tf");
        imprimir(ajustado, "Modelo ajustado: I = 0.40H + 0.35N + 0.25Tf");

        File dir = new File("dist");
        dir.mkdirs();
        exportarCsv(original, ajustado, new File(dir, "datos_java.csv"));
        graficar(original, "Indice atmosferico - modelo original",
                new File(dir, "indice_original_java.png"));
        graficar(ajustado, "Indice atmosferico - modelo ajustado",
                new File(dir, "indice_ajustado_java.png"));

        System.out.println();
        System.out.println("Archivos generados en dist/: "
                + "datos_java.csv, indice_original_java.png, indice_ajustado_java.png");
    }
}
