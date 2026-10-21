/* Quotients of the {1,1} pairs built from two K4 blocks.
 * A {1,1} pair whose two stretches lie in K4 blocks (H-path a,a+1,a+2,a+3 with chords
 * a(a+2), a(a+3), (a+1)(a+3) and stretch (a+1)(a+2)) contracts each block to one edge.
 * The quotient Q has m = n - 8 vertices, Hamilton cycle H' = (0,...,m-1), and a 2-factor F'
 * disjoint from the edges of H' except that F' may contain a second copy of the two
 * contracted edges e1 = (m-1)0 and e2 = (d-1)d (an edge parallel to e is a chord of Gamma).
 * Then #HC(Gamma) = 4 q, q = number of Hamilton cycles of Q through e1 and e2, and the pair
 * has 4q - 1 good cycles when H* is absent.  This program finds min q over all F' and d.
 * usage: quot11 m      (prints MIN m d q F' for the best d, and the overall minimum)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int m, d, need[32], best, cap;
static int Fm[32][32];          /* multiplicity of F' edges */
static int path[32], q;
static long long total;
static int bestF[32][32], bestd;

static int Hadj(int a, int b) { int x = a - b; if (x < 0) x = -x; return x == 1 || x == m - 1; }
static int isE(int a, int b) {  /* contracted edges e1 = (m-1,0), e2 = (d-1,d) */
    return (a == m - 1 && b == 0) || (a == 0 && b == m - 1) || (a == d - 1 && b == d) || (a == d && b == d - 1);
}
static int allowed(int a, int b) { return !Hadj(a, b) || isE(a, b); }

/* count Hamilton cycles through e1 and e2, as multigraph cycles; H'-edges and F'-edges are
 * distinct edges, so a pair of vertices joined by H' and F' gives two choices */
static void dfs(int v, int depth, unsigned vis, int usedE1, int usedE2) {
    if (q >= cap) return;
    if (depth == m) {
        /* close v -> 0 */
        int h = Hadj(v, 0), f = Fm[v][0];
        /* H' edge v0 is e1 only when v == m-1 */
        if (h) { int e1 = (v == m - 1), e2 = (d == 1 && v == 1) || (d == m - 1 && v == m - 1);
            if ((usedE1 || e1) && (usedE2 || e2)) q++; }
        if (f && usedE1 && usedE2) q += f;
        return;
    }
    for (int w = 0; w < m; w++) {
        if (vis >> w & 1) continue;
        if (Hadj(v, w)) {   /* the H' edge vw */
            int e1 = (v == m - 1 && w == 0) || (v == 0 && w == m - 1);
            int e2 = (v == d - 1 && w == d) || (v == d && w == d - 1);
            path[depth] = w; dfs(w, depth + 1, vis | 1u << w, usedE1 | e1, usedE2 | e2);
        }
        for (int k = 0; k < Fm[v][w]; k++) { path[depth] = w; dfs(w, depth + 1, vis | 1u << w, usedE1, usedE2); }
    }
}

static void process(void) {
    total++;
    q = 0;
    /* start at 0; each undirected cycle is found twice, so count with doubled cap */
    cap = 2 * best;
    dfs(0, 1, 1u, 0, 0);
    int qq = q / 2;
    if (q < cap && qq < best) { best = qq; memcpy(bestF, Fm, sizeof Fm); bestd = d; }
}

/* chords at v in increasing order of the other end, so each F' is generated once */
static void gen(int v, int lo) {
    while (v < m && need[v] == 0) { v++; lo = 0; }
    if (v == m) { process(); return; }
    for (int w = (lo > v + 1 ? lo : v + 1); w < m; w++) {
        if (need[w] == 0 || !allowed(v, w) || Fm[v][w]) continue;
        Fm[v][w] = Fm[w][v] = 1; need[v]--; need[w]--;
        gen(v, w + 1);
        Fm[v][w] = Fm[w][v] = 0; need[v]++; need[w]++;
    }
}

int main(int argc, char **argv) {
    m = atoi(argv[1]);
    int gbest = 1 << 30;
    for (d = 1; d <= m / 2; d++) {          /* e2 = (d-1,d); the reflection x -> m-1-x maps d to m-d */
        memset(Fm, 0, sizeof Fm); for (int i = 0; i < m; i++) need[i] = 2;
        best = 1 << 20; total = 0;
        gen(0, 0);
        printf("MIN m=%d d=%d F'=%lld q=%d F=", m, d, total, best);
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if (bestF[a][b]) printf(" %d-%d", a, b);
        printf("\n"); fflush(stdout);
        if (best < gbest) gbest = best;
    }
    printf("QMIN m=%d q=%d g=4q-1=%d (n=%d)\n", m, gbest, 4 * gbest - 1, m + 8);
    return 0;
}
