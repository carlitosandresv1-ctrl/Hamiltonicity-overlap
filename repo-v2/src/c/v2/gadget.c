/* Gadget search.  A gadget on W = [m] is a 2-factor F of [m] together with the
 * path P = 0-1-...-(m-1).  Inserted in place of an H-edge xy (x-0, (m-1)-y),
 * every Hamilton cycle of the new graph must traverse W as one Hamilton path of
 * F u P from 0 to m-1.  We want gadgets where that path is UNIQUE (it is P).
 * Report, for each m, how many such gadgets exist by s = |F n P| and stretch pattern. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int m; static u32 F[16], A[16]; static int deg[16];
static long long hp;
static void dfs(int v, u32 vis, int d) {
    if (hp > 1) return;
    if (d == m) { if (v == m - 1) hp++; return; }
    u32 c = A[v] & ~vis;
    while (c) { int w = __builtin_ctz(c); c &= c - 1;
        if (w == m - 1 && d != m - 1) continue;
        dfs(w, vis | (1u << w), d + 1); }
}
static long long tot[16]; static long long cnt[16][64]; static char pname[16][64][32]; static int npat[16];
static void process(void) {
    int s = 0;
    for (int i = 0; i + 1 < m; i++) if ((F[i] >> (i + 1)) & 1) s++;
    for (int i = 0; i < m; i++) { A[i] = F[i]; if (i) A[i] |= 1u << (i - 1); if (i + 1 < m) A[i] |= 1u << (i + 1); }
    hp = 0; dfs(0, 1u, 1);
    if (hp != 1) return;
    /* stretch pattern along P */
    int sz[16], c = 0, len = 0;
    for (int i = 0; i + 1 < m; i++) { if ((F[i] >> (i + 1)) & 1) len++; else { if (len) sz[c++] = len; len = 0; } }
    if (len) sz[c++] = len;
    for (int i = 0; i < c; i++) for (int j = i + 1; j < c; j++) if (sz[j] < sz[i]) { int t = sz[i]; sz[i] = sz[j]; sz[j] = t; }
    char key[32] = "{"; for (int i = 0; i < c; i++) { char b[8]; sprintf(b, i ? ",%d" : "%d", sz[i]); strcat(key, b); } strcat(key, "}");
    tot[s]++;
    int k; for (k = 0; k < npat[s]; k++) if (!strcmp(pname[s][k], key)) break;
    if (k == npat[s]) { strcpy(pname[s][k], key); npat[s]++; cnt[s][k] = 0;
        printf("  first example m=%d s=%d pattern %s : F =", m, s, key);
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) if ((F[a] >> b) & 1) printf(" %d%d", a, b);
        printf("\n"); }
    cnt[s][k]++;
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
    for (m = 3; m <= M; m++) {
        memset(tot, 0, sizeof tot); memset(npat, 0, sizeof npat);
        printf("m=%d\n", m);
        gen(0);
        for (int s = 0; s <= m; s++) if (tot[s]) {
            printf("  s=%d : %lld gadgets;", s, tot[s]);
            for (int k = 0; k < npat[s]; k++) printf(" %s:%lld", pname[s][k], cnt[s][k]);
            printf("\n"); }
        fflush(stdout);
    }
}
