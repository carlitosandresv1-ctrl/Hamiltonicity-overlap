/* Gadgets with unit-stretch pattern {1,1} (M=2) or {1,1,1} (M=3) and overlap o_W = s_W.
 * W = {0,...,m-1}, P_W = 0-1-...-(m-1).  S = M pairwise non-adjacent edges (p,p+1) of P_W;
 * F_W runs over all 2-factors of W with F_W n P_W = S (the edge 0-(m-1) is a chord).
 * Prop. 8.3 / Lemma 8.2: inserting a gadget with o_W = s_W into a 4-regular uniquely
 * Hamiltonian graph gives a RIGID pair with that stretch pattern.  As in Lemma 7.5,
 * o_W = s_W iff every Hamilton path from 0 to m-1 contains all unshared edges of P_W;
 * "rigid" in the sense of Def. 8.1 (unique path) is the special case with one path.
 * usage: [M=2] gadget11 m      prints every gadget with o_W = s_W and a summary
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int m, M = 2, P[4];
static u32 F[32], G[32], Pm[32], Um[32];
static int need[32], path[32], npaths, bad;
static long long total, found, foundunique;

static inline int Padj(int a, int b) { int d = a - b; return d == 1 || d == -1; }

static void dfs(int d, u32 vis, int usedU) {
    if (bad) return;
    int v = path[d - 1];
    if (d == m) {                      /* path[m-1] is m-1 by construction */
        if (usedU < m - 1 - M) bad = 1; else npaths++;
        return;
    }
    u32 c = G[v] & ~vis;
    if (d < m - 1) c &= ~(1u << (m - 1));          /* m-1 must be last */
    while (c) {
        int w = __builtin_ctz(c); c &= c - 1;
        path[d] = w;
        dfs(d + 1, vis | (1u << w), usedU + ((Um[v] >> w) & 1));
        if (bad) return;
    }
}

static void process(void) {
    total++;
    for (int i = 0; i < m; i++) { G[i] = F[i] | Pm[i]; Um[i] = Pm[i] & ~F[i]; }
    bad = 0; npaths = 0; path[0] = 0;
    dfs(1, 1u, 0);
    if (bad) return;
    found++; if (npaths == 1) foundunique++;
    printf("GADGET m=%d p=", m); for (int i = 0; i < M; i++) printf("%d%s", P[i], i + 1 < M ? "," : "");
    printf(" paths=%d F=", npaths);
    for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if ((F[a] >> b) & 1) printf(" %d-%d", a, b);
    printf("\n"); fflush(stdout);
}

static void gen(int v) {
    while (v < m && need[v] == 0) v++;
    if (v == m) { process(); return; }
    if (need[v] == 1) {
        for (int w = v + 1; w < m; w++) if (need[w] > 0 && !Padj(v, w) && !((F[v] >> w) & 1)) {
            F[v] |= 1u << w; F[w] |= 1u << v; need[v]--; need[w]--;
            gen(v + 1);
            F[v] &= ~(1u << w); F[w] &= ~(1u << v); need[v]++; need[w]++;
        }
    } else {
        for (int a = v + 1; a < m; a++) if (need[a] > 0 && !Padj(v, a))
            for (int b = a + 1; b < m; b++) if (need[b] > 0 && !Padj(v, b)) {
                F[v] |= (1u << a) | (1u << b); F[a] |= 1u << v; F[b] |= 1u << v;
                need[v] = 0; need[a]--; need[b]--;
                gen(v + 1);
                F[v] &= ~((1u << a) | (1u << b)); F[a] &= ~(1u << v); F[b] &= ~(1u << v);
                need[v] = 2; need[a]++; need[b]++;
            }
    }
}

static void run(void) {
    memset(F, 0, sizeof F);
    for (int i = 0; i < m; i++) need[i] = 2;
    for (int i = 0; i < M; i++) { int a = P[i], b = P[i] + 1; F[a] |= 1u << b; F[b] |= 1u << a; need[a]--; need[b]--; }
    gen(0);
}

static void place(int i, int lo) {
    if (i == M) { run(); return; }
    for (int p = lo; p <= m - 2; p++) { P[i] = p; place(i + 1, p + 2); }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: [M=2] gadget11 m [p0]\n"); return 1; }
    m = atoi(argv[1]);
    if (getenv("M")) M = atoi(getenv("M"));
    for (int i = 0; i < m; i++) Pm[i] = (i > 0 ? 1u << (i - 1) : 0) | (i + 1 < m ? 1u << (i + 1) : 0);
    if (argc > 2) { P[0] = atoi(argv[2]); place(1, P[0] + 2); }   /* fix the first stretch (for parallel runs) */
    else place(0, 0);
    printf("SUMMARY m=%d M=%d gadgets=%lld oW=sW:%lld of_which_unique_path:%lld\n", m, M, total, found, foundunique);
    return 0;
}
