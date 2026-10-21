/* s = 1 gadget search (Proposition 8.3, case k = 1).  For every 2-factor F of [m] sharing
 * exactly one edge with the path P = 0-1-...-(m-1), enumerate all Hamilton paths of F u P
 * from 0 to m-1 and record the largest overlap with F.  A rigid s = 1 gadget would have a
 * single path (overlap 1); the K4 gadget (m = 4) has two paths and overlap 3.
 * usage: gadget1 M   (all m = 3..M)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int m; static u32 F[16], A[16]; static int deg[16];
static long long hp; static int maxo;
static void dfs(int v, u32 vis, int d, int o) {
    if (d == m) { if (v == m - 1) { hp++; if (o > maxo) maxo = o; } return; }
    u32 c = A[v] & ~vis;
    while (c) { int w = __builtin_ctz(c); c &= c - 1;
        if (w == m - 1 && d != m - 1) continue;
        dfs(w, vis | (1u << w), d + 1, o + ((F[v] >> w) & 1)); }
}
static long long hist[16][16]; static int best=99;
static void process(void) {
    int s = 0;
    for (int i = 0; i + 1 < m; i++) if ((F[i] >> (i + 1)) & 1) s++;
    if (s != 1) return;
    for (int i = 0; i < m; i++) { A[i] = F[i]; if (i) A[i] |= 1u << (i - 1); if (i + 1 < m) A[i] |= 1u << (i + 1); }
    hp = 0; maxo = -1; dfs(0, 1u, 1, 0);
    hist[m][maxo]++;
    if (maxo < best || (maxo<=4 && hist[m][maxo]==1)) { if (maxo<best) best = maxo;
        printf("  m=%d max-overlap=%d #paths=%lld F =", m, maxo, hp);
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if ((F[a] >> b) & 1) printf(" %d%d", a, b);
        printf("\n"); }
}
static void gen(int v) {
    while (v < m && deg[v] == 2) v++;
    if (v == m) { process(); return; }
    if (deg[v] == 1) {
        for (int w = v + 1; w < m; w++) if (deg[w] < 2 && !((F[v] >> w) & 1)) {
            F[v] |= 1u << w; F[w] |= 1u << v; deg[v]++; deg[w]++; gen(v + 1);
            F[v] &= ~(1u << w); F[w] &= ~(1u << v); deg[v]--; deg[w]--; }
    } else {
        for (int a = v + 1; a < m; a++) if (deg[a] < 2) for (int b = a + 1; b < m; b++) if (deg[b] < 2) {
            F[v] = (1u << a) | (1u << b); F[a] |= 1u << v; F[b] |= 1u << v; deg[v] = 2; deg[a]++; deg[b]++; gen(v + 1);
            F[v] = 0; F[a] &= ~(1u << v); F[b] &= ~(1u << v); deg[v] = 0; deg[a]--; deg[b]--; }
    }
}
int main(int argc, char **argv) {
    int M = atoi(argv[1]);
    for (m = 3; m <= M; m++) { gen(0);
        printf("m=%d  s=1 gadgets by max overlap:", m);
        for (int o = 0; o <= m; o++) if (hist[m][o]) printf(" %d:%lld", o, hist[m][o]);
        printf("\n"); fflush(stdout); }
}
