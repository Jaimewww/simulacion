package ape6;

import java.util.Arrays;

/**
 * Statistical tests for pseudo-random numbers - APE 6, Simulation.
 *
 * - Chi-square goodness-of-fit test (uniformity in k bins of [0, 1)).
 * - Kolmogorov-Smirnov test (empirical CDF vs theoretical U(0,1) CDF).
 *
 * p-values are computed from scratch, with the same algorithms as the Python
 * reference implementation (Lanczos log-gamma, series and Lentz continued
 * fraction for the regularized incomplete gamma, asymptotic Kolmogorov
 * distribution) so both implementations produce identical numbers.
 */
public final class Pruebas {

    public static final double ALPHA = 0.05;

    private Pruebas() {
    }

    // ------------------------------------------------------------------
    // Incomplete gamma (Numerical Recipes: gammln/gser/gcf)
    // ------------------------------------------------------------------

    private static double logGamma(double xx) {
        double[] cof = {
            76.18009172947146, -86.50532032941677, 24.01409824083091,
            -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5,
        };
        double x = xx;
        double y = xx;
        double tmp = x + 5.5;
        tmp -= (x + 0.5) * Math.log(tmp);
        double ser = 1.000000000190015;
        for (double c : cof) {
            y += 1.0;
            ser += c / y;
        }
        return -tmp + Math.log(2.5066282746310005 * ser / x);
    }

    private static double gser(double a, double x) {
        final int itmax = 200;
        final double eps = 3e-12;
        if (x <= 0.0) {
            return 0.0;
        }
        double ap = a;
        double sum = 1.0 / a;
        double delta = sum;
        for (int n = 0; n < itmax; n++) {
            ap += 1.0;
            delta *= x / ap;
            sum += delta;
            if (Math.abs(delta) < Math.abs(sum) * eps) {
                break;
            }
        }
        return sum * Math.exp(-x + a * Math.log(x) - logGamma(a));
    }

    private static double gcf(double a, double x) {
        final int itmax = 200;
        final double eps = 3e-12;
        final double tiny = 1e-300;
        double b = x + 1.0 - a;
        double c = 1.0 / tiny;
        double d = 1.0 / b;
        double h = d;
        for (int i = 1; i <= itmax; i++) {
            double an = -1.0 * i * (i - a);
            b += 2.0;
            d = an * d + b;
            if (Math.abs(d) < tiny) {
                d = tiny;
            }
            c = b + an / c;
            if (Math.abs(c) < tiny) {
                c = tiny;
            }
            d = 1.0 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1.0) < eps) {
                break;
            }
        }
        return Math.exp(-x + a * Math.log(x) - logGamma(a)) * h;
    }

    /** Regularized upper incomplete gamma Q(a, x) = Gamma(a, x) / Gamma(a). */
    public static double gammaQ(double a, double x) {
        if (x < 0.0 || a <= 0.0) {
            throw new IllegalArgumentException("invalid arguments");
        }
        if (x == 0.0) {
            return 1.0;
        }
        if (x < a + 1.0) {
            return 1.0 - gser(a, x);
        }
        return gcf(a, x);
    }

    /** Survival function of the chi-square distribution: P(Chi2_df > stat). */
    public static double chi2PValue(double stat, int df) {
        return gammaQ(df / 2.0, stat / 2.0);
    }

    /**
     * Asymptotic survival function of the Kolmogorov distribution:
     * Q_KS(x) = 2 * sum_{k>=1} (-1)^(k-1) exp(-2 k^2 x^2).
     * Uses the low-x series (North et al.) below 1.18, as scipy does.
     */
    public static double kolmogorovQ(double x) {
        if (x <= 0.0) {
            return 1.0;
        }
        if (x < 1.18) {
            double sum = 0.0;
            for (int j = 1; j <= 100; j++) {
                sum += Math.exp(-Math.pow(2.0 * j - 1.0, 2) * Math.pow(Math.PI, 2) / (8.0 * x * x));
            }
            return Math.sqrt(2.0 * Math.PI) / x * sum;
        }
        double sum = 0.0;
        int k = 1;
        while (k <= 1000) {
            double term = Math.exp(-2.0 * k * k * x * x);
            if (term < 1e-16 && k > 1) {
                break;
            }
            sum += (k % 2 == 1 ? 1.0 : -1.0) * term;
            k++;
        }
        return 2.0 * sum;
    }

    /** p-value for the one-sample K-S statistic D with sample size n. */
    public static double ksPValue(double d, int n) {
        return Math.min(1.0, kolmogorovQ(Math.sqrt(n) * d));
    }

    // ------------------------------------------------------------------
    // Tests
    // ------------------------------------------------------------------

    /** Chi-square uniformity test over k equal-width bins in [0, 1). */
    public static double[][] chiSquare(double[] values, int k) {
        int n = values.length;
        double e = (double) n / k;
        int[] observed = new int[k];
        for (double v : values) {
            int idx = (int) Math.min((long) (v * k), k - 1L);
            observed[idx]++;
        }
        double stat = 0.0;
        for (int o : observed) {
            stat += (o - e) * (o - e) / e;
        }
        int df = k - 1;
        double p = chi2PValue(stat, df);
        return new double[][] {
            { stat, df, p, p < ALPHA ? 1.0 : 0.0 },
            Arrays.stream(observed).asDoubleStream().toArray(),
            { e },
        };
    }

    /** Result holder for a raw statistic triple (stat, df, p, flag). */
    public static double[] ksTest(double[] values) {
        int n = values.length;
        double[] xs = values.clone();
        Arrays.sort(xs);
        double dPlus = 0.0;
        double dMinus = 0.0;
        for (int i = 0; i < n; i++) {
            double dp = (i + 1.0) / n - xs[i];
            double dm = xs[i] - (double) i / n;
            if (dp > dPlus) {
                dPlus = dp;
            }
            if (dm > dMinus) {
                dMinus = dm;
            }
        }
        double d = Math.max(dPlus, dMinus);
        double p = ksPValue(d, n);
        return new double[] { d, p, p < ALPHA ? 1.0 : 0.0 };
    }
}
