/* One-stretch plugs: the sides of a 2-edge cut of a {1,1} pair that separates the stretches.
 * Such a side X has a Hamilton path P = (0,1,...,m-1) between its ports x = 0 and y = m-1
 * (the part of H inside X), and a 2-factor F_X of X with F_X n P = {j(j+1)} (the stretch);
 * the chord 0-(m-1) is allowed, since 0 and m-1 are not adjacent along P.  Gamma_X = P u F_X
 * has x, y, j, j+1 of degree 3 (x or y of degree 2 when it is also a stretch end) and all
 * other vertices of degree 4.  A {1,1} pair glued from two sides X, Y along the cut is rigid
 * iff hp(X) = hp(Y) = 1, where hp is the number of Hamilton paths of Gamma_X from x to y.
 * This program computes, for each m, the histogram of hp (capped at CAP) over all F_X and all
 * stretch positions j <= (m-2)/2 (the reflection i -> m-1-i maps j to m-2-j).
 * usage: [CAP=8] plug1 m [j]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int m, j, need[32], CAP = 8;
static u32 F[32], G[32];
static long long hist[64], total;
static int cnt;
static char minF[256]; static int minhp = 1 << 30, minj;

static int Padj(int a, int b) { int d = a - b; return d == 1 || d == -1; }

static void dfs(int v, int d, u32 vis) {
    if (cnt >= CAP) return;
    if (d == m) { cnt += (v == m - 1); return; }
    u32 c = G[v] & ~vis;
    if (d < m - 1) c &= ~(1u << (m - 1));          /* y only as the last vertex */
    while (c) { int w = __builtin_ctz(c); c &= c - 1; dfs(w, d + 1, vis | 1u << w); if (cnt >= CAP) return; }
}

static void process(void) {
    total++;
    for (int i = 0; i < m; i++) {
        G[i] = F[i];
        if (i > 0) G[i] |= 1u << (i - 1);
        if (i < m - 1) G[i] |= 1u << (i + 1);
    }
    cnt = 0; dfs(0, 1, 1u);
    hist[cnt]++;
    if (cnt < minhp) {
        minhp = cnt; minj = j; int p = 0;
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if ((F[a] >> b) & 1) p += sprintf(minF + p, " %d-%d", a, b);
    }
    if (cnt == 1) {
        printf("PLUG1 m=%d j=%d F=", m, j);
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if ((F[a] >> b) & 1) printf(" %d-%d", a, b);
        printf("\n"); fflush(stdout);
    }
}

/* chords at v are added in increasing order of the other end (lo), so that each 2-factor
 * is generated exactly once */
static void gen(int v, int lo) {
    while (v < m && need[v] == 0) { v++; lo = 0; }
    if (v == m) { process(); return; }
    for (int w = (lo > v + 1 ? lo : v + 1); w < m; w++) {
        if (need[w] == 0 || Padj(v, w) || ((F[v] >> w) & 1)) continue;
        F[v] |= 1u << w; F[w] |= 1u << v; need[v]--; need[w]--;
        gen(v, w + 1);
        F[v] &= ~(1u << w); F[w] &= ~(1u << v); need[v]++; need[w]++;
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: [CAP=8] plug1 m [j]\n"); return 1; }
    m = atoi(argv[1]);
    if (getenv("CAP")) CAP = atoi(getenv("CAP"));
    if (m < 4 || m > 31 || CAP > 63) { fprintf(stderr, "4 <= m <= 31, CAP <= 63\n"); return 1; }
    int fixj = argc > 2 ? atoi(argv[2]) : -1;
    for (j = 0; j <= (m - 2) / 2; j++) {
        if (fixj >= 0 && j != fixj) continue;
        memset(F, 0, sizeof F);
        for (int i = 0; i < m; i++) need[i] = 2;
        F[j] |= 1u << (j + 1); F[j + 1] |= 1u << j; need[j]--; need[j + 1]--;
        gen(0, 0);
    }
    printf("MINHP m=%d hp=%d j=%d F=%s\n", m, minhp, minj, minF);
    printf("SUMMARY m=%d sides=%lld", m, total);
    for (int h = 0; h <= CAP; h++) if (hist[h]) printf(" hp%s%d:%lld", h == CAP ? ">=" : "=", h, hist[h]);
    printf("\n");
    return 0;
}
