package ape6;

/**
 * Linear Congruential Generator (LCG) - APE 6, Simulation.
 *
 * X_{n+1} = (a * X_n + c) mod m
 * U_n     = X_{n+1} / m  in [0, 1)
 *
 * State arithmetic uses 64-bit wrapping: for power-of-two moduli m <= 2^64,
 * (wrapped product) mod m equals the exact mathematical product mod m, which
 * keeps the sequence identical to the Python reference implementation.
 */
public final class Lcg {

    public final String name;
    public final long m;      // modulus
    public final long a;      // multiplier
    public final long c;      // increment
    public final long seed;   // X_0
    public final String quality;

    public Lcg(String name, long m, long a, long c, long seed, String quality) {
        if (m <= 0) {
            throw new IllegalArgumentException("modulus must be positive");
        }
        this.name = name;
        this.m = m;
        this.a = a;
        this.c = c;
        this.seed = seed;
        this.quality = quality;
    }

    /** Generates out.length uniforms in [0, 1) and returns the final state. */
    public long generate(double[] out) {
        long x = Math.floorMod(seed, m);
        for (int i = 0; i < out.length; i++) {
            x = Math.floorMod(a * x + c, m);
            out[i] = (double) x / (double) m;
        }
        return x;
    }
}
