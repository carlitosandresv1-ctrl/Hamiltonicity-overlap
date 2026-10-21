/* Simulated annealing for the pattern {1,1}: H = (0,1,...,n-1), S = {01, j(j+1)} fixed, the
 * n-2 chords of F (edges of F outside H) are changed by 2-switches ab,cd -> ac,bd / ad,bc that
 * keep F a 2-factor with F n H = S.  Energy = number of good Hamilton cycles of Gamma = F u H
 * (cycles that give up an unshared H-edge), counted up to CAP; a pair is rigid iff it is 0.
 * For the best pair of each restart it also reports kmask (bit K set when some good cycle keeps
 * exactly the subset K of S, as in near111 CLAIMS) and whether the pair is in the C3-failing
 * class (every good cycle keeps S, kmask = 8).
 * usage: [CAP=400] [T0=1] [SEED="a-b ..."] anneal11 n restarts moves seed [j]
 *        (j = 2..n-2 fixed, else random per restart; SEED = a {1,1} pair on n-1 vertices,
 *        grown by one vertex at a random place in each restart, see seedinit)
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int n, CAP = 400, j;
static u32 Hm[32], F[32], G[32], Um[32], sbit[32];
static int good, path[32]; static u32 kmask; static int fullkm;

static void dfs(int d, u32 vis, int usedU, u32 keptS) {
    if (good >= CAP && !fullkm) return;
    int v = path[d - 1];
    if (d == n) {
        if (!(G[v] & 1u) || path[1] > path[n - 1]) return;
        int u = usedU + (Um[v] & 1u);
        u32 k = keptS | ((Hm[v] & F[v] & 1u) ? sbit[v] : 0);
        if (u < n - 2) { good++; kmask |= 1u << k; }
        return;
    }
    u32 c = G[v] & ~vis;
    while (c) {
        int w = __builtin_ctz(c); c &= c - 1;
        path[d] = w;
        dfs(d + 1, vis | (1u << w), usedU + ((Um[v] >> w) & 1), keptS | ((((Hm[v] & F[v]) >> w) & 1) ? sbit[v] : 0));
        if (good >= CAP && !fullkm) return;
    }
}

static int energy(int full) {
    for (int i = 0; i < n; i++) { G[i] = F[i] | Hm[i]; Um[i] = Hm[i] & ~F[i]; }
    good = 0; kmask = 0; fullkm = full; path[0] = 0;
    dfs(1, 1u, 0, 0);
    return good;
}

static int ca[32], cb[32], nc;          /* chord list */
static void rebuild(void) {
    for (int i = 0; i < n; i++) F[i] = 0;
    F[0] |= 2u; F[1] |= 1u; F[j] |= 1u << (j + 1); F[j + 1] |= 1u << j;
    for (int k = 0; k < nc; k++) { F[ca[k]] |= 1u << cb[k]; F[cb[k]] |= 1u << ca[k]; }
}
static int okchord(int a, int b) { return a != b && !((Hm[a] >> b) & 1) && !((F[a] >> b) & 1); }

static double urand(void) { return rand() / (RAND_MAX + 1.0); }

static void randinit(void) {
    for (;;) {
        int stubs[64], m = 0;
        for (int v = 0; v < n; v++) { int need = (v == 0 || v == 1 || v == j || v == j + 1) ? 1 : 2;
            for (int t = 0; t < need; t++) stubs[m++] = v; }
        for (int i = m - 1; i > 0; i--) { int r = rand() % (i + 1), t = stubs[i]; stubs[i] = stubs[r]; stubs[r] = t; }
        nc = 0; for (int i = 0; i < n; i++) F[i] = 0;
        F[0] |= 2u; F[1] |= 1u; F[j] |= 1u << (j + 1); F[j + 1] |= 1u << j;
        int ok = 1;
        for (int i = 0; i < m; i += 2) {
            int a = stubs[i], b = stubs[i + 1];
            if (!okchord(a, b)) { ok = 0; break; }
            ca[nc] = a; cb[nc] = b; nc++; F[a] |= 1u << b; F[b] |= 1u << a;
        }
        if (ok) return;
    }
}

/* SEED: a {1,1} pair on n-1 vertices (F as "a-b a-b ...", e.g. copied from a BEST line).
 * Each restart inserts a new vertex p between p-1 and p on H (not inside a stretch), relabels,
 * and reroutes a random chord ab through p (ab -> ap, pb).  Returns the new j. */
static int sa0[64], sb0[64], ns0, jseed;
static void parseseed(const char *s) {
    ns0 = 0; jseed = -1;
    while (*s) {
        while (*s == ' ') s++;
        if (!*s) break;
        int a, b, k; if (sscanf(s, "%d-%d%n", &a, &b, &k) != 2) break;
        s += k; sa0[ns0] = a; sb0[ns0] = b; ns0++;
        if (b == a + 1 && a != 0) jseed = a;
    }
    if (ns0 != n - 1 || jseed < 2) { fprintf(stderr, "SEED must be a {1,1} pair on n-1 = %d vertices\n", n - 1); exit(1); }
}
static int seedinit(void) {
    for (;;) {
        int p = 2 + rand() % (n - 2);                 /* new vertex p, 2 <= p <= n-1 */
        if (p == jseed + 1) continue;                    /* would split the stretch jseed (jseed+1) */
        int jn = p <= jseed ? jseed + 1 : jseed;
        j = jn;
        for (int i = 0; i < n; i++) F[i] = 0;
        F[0] |= 2u; F[1] |= 1u; F[j] |= 1u << (j + 1); F[j + 1] |= 1u << j;
        nc = 0;
        for (int k = 0; k < ns0; k++) {
            int a = sa0[k] >= p ? sa0[k] + 1 : sa0[k], b = sb0[k] >= p ? sb0[k] + 1 : sb0[k];
            if ((a == 0 && b == 1) || (a == j && b == j + 1)) continue;   /* stretch edges */
            ca[nc] = a; cb[nc] = b; nc++;
        }
        int q = rand() % nc, a = ca[q], b = cb[q];
        ca[q] = ca[nc - 1]; cb[q] = cb[nc - 1]; nc--;
        for (int k = 0; k < nc; k++) { F[ca[k]] |= 1u << cb[k]; F[cb[k]] |= 1u << ca[k]; }
        /* the old H-edge (p-1)(p+1) is no longer in H: a chord there is fine, so only
         * the new H-neighbours of p have to be avoided */
        if (!okchord(a, p) || !okchord(p, b)) continue;
        int bad = 0;                                  /* old chords must not become H-edges */
        for (int k = 0; k < nc && !bad; k++) if ((Hm[ca[k]] >> cb[k]) & 1) bad = 1;
        if ((Hm[a] >> p) & 1 || (Hm[p] >> b) & 1) bad = 1;
        if (bad) continue;
        F[a] |= 1u << p; F[p] |= 1u << a; F[p] |= 1u << b; F[b] |= 1u << p;
        ca[nc] = a; cb[nc] = p; nc++; ca[nc] = p; cb[nc] = b; nc++;
        return jn;
    }
}

static void printF(void) {
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if ((F[a] >> b) & 1) printf(" %d-%d", a, b);
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: [CAP=400] anneal11 n restarts moves seed [j]\n"); return 1; }
    n = atoi(argv[1]); int R = atoi(argv[2]), MV = atoi(argv[3]); srand(atoi(argv[4]));
    int fixj = argc > 5 ? atoi(argv[5]) : -1;
    if (getenv("CAP")) CAP = atoi(getenv("CAP"));
    if (n < 7 || n > 31) { fprintf(stderr, "7 <= n <= 31\n"); return 1; }
    for (int i = 0; i < n; i++) Hm[i] = (1u << ((i + 1) % n)) | (1u << ((i + n - 1) % n));
    double T0 = getenv("T0") ? atof(getenv("T0")) : 1.0, T1 = 0.02;
    const char *seed = getenv("SEED");
    if (seed) parseseed(seed);
    int gbest = 1 << 30;
    for (int r = 0; r < R; r++) {
        if (seed) seedinit();
        else j = fixj >= 2 ? fixj : 2 + rand() % (n - 3);
        memset(sbit, 0, sizeof sbit); sbit[0] = sbit[1] = 1; sbit[j] = sbit[j + 1] = 2;
        if (!seed) randinit();
        int e = energy(0), best = e; int bca[32], bcb[32]; memcpy(bca, ca, sizeof ca); memcpy(bcb, cb, sizeof cb);
        for (int mv = 0; mv < MV && best > 0; mv++) {
            double T = T0 * pow(T1 / T0, (double)mv / MV);
            int p = rand() % nc, q = rand() % nc; if (p == q) continue;
            int a = ca[p], b = cb[p], c = ca[q], d = cb[q];
            if (rand() & 1) { int t = c; c = d; d = t; }          /* ab,cd -> ac,bd */
            if (a == c || a == d || b == c || b == d) continue;
            F[a] &= ~(1u << b); F[b] &= ~(1u << a); F[c] &= ~(1u << d); F[d] &= ~(1u << c);
            if (!okchord(a, c) || !okchord(b, d) || (a == b) ) { rebuild(); continue; }
            F[a] |= 1u << c; F[c] |= 1u << a;
            if (!okchord(b, d)) { rebuild(); continue; }
            F[b] |= 1u << d; F[d] |= 1u << b;
            int oa = ca[p], ob = cb[p], oc = ca[q], od = cb[q];
            ca[p] = a; cb[p] = c; ca[q] = b; cb[q] = d;
            int e2 = energy(0);
            double dE = log(1.0 + e2) - log(1.0 + e);
            if (dE <= 0 || urand() < exp(-dE / T)) {
                e = e2;
                if (e < best) { best = e; memcpy(bca, ca, sizeof ca); memcpy(bcb, cb, sizeof cb); }
            } else { ca[p] = oa; cb[p] = ob; ca[q] = oc; cb[q] = od; rebuild(); }
        }
        memcpy(ca, bca, sizeof ca); memcpy(cb, bcb, sizeof cb); rebuild();
        int g = energy(1);                                    /* full count and kmask */
        if (g != best && best < CAP) { fprintf(stderr, "recount mismatch %d %d\n", g, best); return 1; }
        printf("BEST n=%d j=%d good=%d%s kmask=%u class=%s F=", n, j, g, g >= CAP ? "+" : "", kmask,
               kmask == 8u ? "C3FAIL" : (g == 0 ? "RIGID" : "other"));
        printF(); printf("\n"); fflush(stdout);
        if (g < gbest) gbest = g;
    }
    printf("SUMMARY n=%d restarts=%d moves=%d min_good=%d\n", n, R, MV, gbest);
    return 0;
}
