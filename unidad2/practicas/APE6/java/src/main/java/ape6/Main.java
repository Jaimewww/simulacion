package ape6;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/**
 * APE 6 - Main experiment driver (Java implementation).
 *
 * Generates 10,000 LCG values per configuration and runs Chi-square and
 * Kolmogorov-Smirnov uniformity tests. Saves JSON stats with the same schema
 * as the Python driver, plus parity CSVs, for cross-language comparison.
 *
 * Usage: java -cp out ape6.Main [outdir]
 */
public final class Main {

    private static final int N = 10_000;
    private static final int K = 10;

    /** Classic LCG parameter sets from the course material (Semana 5 slides). */
    private static Lcg[] configs() {
        return new Lcg[] {
            new Lcg("glibc", 1L << 32, 1103515245L, 12345L, 1L, "good"),
            new Lcg("java_random", 1L << 48, 25214903917L, 11L, 42L, "good"),
            new Lcg("zx81_bad", (1L << 17) + 1L, 75L, 74L, 1L, "bad"),
        };
    }

    public static void main(String[] args) throws IOException {
        Path outdir = Paths.get(args.length > 0 ? args[0] : "../results");
        Files.createDirectories(outdir);

        Map<String, Object> all = new LinkedHashMap<>();
        for (Lcg cfg : configs()) {
            double[] values = new double[N];
            long finalState = cfg.generate(values);

            double[][] chi = Pruebas.chiSquare(values, K);
            double[] ks = Pruebas.ksTest(values);
            int[] observed = new int[K];
            for (int i = 0; i < K; i++) {
                observed[i] = (int) chi[1][i];
            }

            Map<String, Object> stats = new LinkedHashMap<>();
            stats.put("n", N);
            stats.put("k", K);
            stats.put("params", params(cfg));
            stats.put("final_state", finalState);
            stats.put("chi2", Map.of("stat", chi[0][0], "df", (int) chi[0][1],
                    "p", chi[0][2], "reject", chi[0][3] > 0.0));
            stats.put("ks", Map.of("stat", ks[0], "p", ks[1], "reject", ks[2] > 0.0));
            stats.put("observed", observed);
            all.put(cfg.name, stats);

            System.out.printf(Locale.ROOT,
                    "== %s (m=%d, a=%d, c=%d, X0=%d) ==%n", cfg.name, cfg.m, cfg.a, cfg.c, cfg.seed);
            System.out.printf(Locale.ROOT, "   X_10000 final state = %d%n", finalState);
            System.out.printf(Locale.ROOT, "   first 5 values      = %s%n",
                    java.util.Arrays.toString(java.util.Arrays.stream(values).limit(5).toArray()));
            System.out.printf(Locale.ROOT, "   mean = %.6f  min = %.6f  max = %.6f%n",
                    mean(values), min(values), max(values));
            System.out.printf(Locale.ROOT, "   Chi2: stat=%.4f df=%.0f p=%.6f -> %s%n",
                    chi[0][0], chi[0][1], chi[0][2],
                    chi[0][3] > 0.0 ? "REJECT H0" : "DO NOT REJECT H0");
            System.out.printf(Locale.ROOT, "   KS:   D=%.6f p=%.6f -> %s%n",
                    ks[0], ks[1], ks[2] > 0.0 ? "REJECT H0" : "DO NOT REJECT H0");

            // observed frequencies per bin
            StringBuilder csv = new StringBuilder("bin,low,high,observed,expected\n");
            for (int i = 0; i < K; i++) {
                csv.append(String.format(Locale.ROOT, "%d,%.1f,%.1f,%d,%.1f%n",
                        i + 1, (double) i / K, (double) (i + 1) / K,
                        (int) chi[1][i], chi[2][0]));
            }
            write(outdir.resolve("observed_" + cfg.name + "_java.csv"), csv.toString());

            // first sample of states for cross-language sequence parity check
            csv = new StringBuilder("index,un_int,un_float\n");
            long x = Math.floorMod(cfg.seed, cfg.m);
            for (int i = 0; i < 200; i++) {
                x = Math.floorMod(cfg.a * x + cfg.c, cfg.m);
                csv.append(String.format(Locale.ROOT, "%d,%d,%s%n",
                        i + 1, x, doubleToFull(x / (double) cfg.m)));
            }
            write(outdir.resolve("parity_" + cfg.name + "_java.csv"), csv.toString());
        }

        write(outdir.resolve("stats_java.json"), toJson(all) + "\n");
        System.out.println("\nStats saved to " + outdir.resolve("stats_java.json"));
    }

    private static Map<String, Object> params(Lcg cfg) {
        Map<String, Object> p = new LinkedHashMap<>();
        p.put("m", cfg.m);
        p.put("a", cfg.a);
        p.put("c", cfg.c);
        p.put("seed", cfg.seed);
        p.put("quality", cfg.quality);
        return p;
    }

    private static void write(Path path, String content) {
        try {
            Files.writeString(path, content, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException("cannot write " + path, e);
        }
    }

    private static double mean(double[] v) {
        double s = 0.0;
        for (double x : v) {
            s += x;
        }
        return s / v.length;
    }

    private static double min(double[] v) {
        double m = 1.0;
        for (double x : v) {
            if (x < m) {
                m = x;
            }
        }
        return m;
    }

    private static double max(double[] v) {
        double m = 0.0;
        for (double x : v) {
            if (x > m) {
                m = x;
            }
        }
        return m;
    }

    /** Formats a double with the full round-trippable precision (repr-like). */
    private static String doubleToFull(double d) {
        return new java.math.BigDecimal(d).toString();
    }

    // ---- minimal ordered JSON serializer (numbers, strings, maps, lists, bools) --
    private static String toJson(Object o) {
        if (o instanceof Map<?, ?> map) {
            StringBuilder sb = new StringBuilder("{");
            boolean first = true;
            for (Map.Entry<?, ?> e : map.entrySet()) {
                if (!first) {
                    sb.append(',');
                }
                first = false;
                sb.append('"').append(e.getKey()).append("\":").append(toJson(e.getValue()));
            }
            return sb.append('}').toString();
        }
        if (o instanceof Boolean b) {
            return b ? "true" : "false";
        }
        if (o instanceof Number || o instanceof Long || o instanceof Integer
                || o instanceof Double) {
            Number num = (Number) o;
            return num.longValue() == num.doubleValue() && num.doubleValue() < 1e15
                    ? String.valueOf(num.longValue()) : String.valueOf(num.doubleValue());
        }
        if (o instanceof int[] arr) {
            StringBuilder sb = new StringBuilder("[");
            for (int i = 0; i < arr.length; i++) {
                if (i > 0) {
                    sb.append(',');
                }
                sb.append(arr[i]);
            }
            return sb.append(']').toString();
        }
        return '"' + String.valueOf(o) + '"';
    }

    private Main() {
    }
}
