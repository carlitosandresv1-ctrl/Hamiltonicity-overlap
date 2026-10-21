/* Pattern {1,1} search.  H = (0,1,...,n-1).  S = {e1 = (0,1), e2 = (j,j+1)}, 2 <= j <= n-2,
 * all other F-edges are chords.  For each such 2-factor F, count the Hamilton cycles of
 * Gamma = F u H that give up some UNSHARED H-edge ("good" cycles; by Cor. 7.9 the pair is
 * rigid iff there are none).  Early exit at 3.  Pairs with <= 2 good cycles are printed.
 * usage: [CAP=40] near11 n   (all j)   or   [CAP=40] near11 n j   (one j)
 * CAP = early-exit threshold on the number of good cycles (default 3); MINGOOD is exact when < CAP.
 * v3 additions (default output unchanged):
 *   HIST=1    print HIST g count, the exact histogram of good cycles for g < CAP.
 *   DETAIL=T  for every pair with at most T good cycles (CAP is raised to T+1 if needed),
 *             re-enumerate all its Hamilton cycles and print one CYC line per good cycle:
 *               CYC k keep=<e1><e2> lost= A<a>/<la> ... B<b>/<lb> ... cyc= v0 v1 ...
 *             H = u1 w1 A u2 w2 B with u1=0, w1=1, u2=j, w2=j+1.  A has la=j-1 edges,
 *             A<a> is the edge (1+a,2+a), a counted from w1; B has lb=n-j-1 edges,
 *             B<b> is the edge (j+1+b, j+2+b mod n), b counted from w2.  keep=11 means
 *             the cycle keeps both shared edges, 10 only e1, 01 only e2, 00 neither.
 *             Each pair is announced by a DET line with its F, before its CYC lines.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int n, J;
static u32 F[32], G[32], Hm[32];
static int need[32];
static long long total, hist[4];
static int path[32], good; static int CAP = 3; static long long mingood = 1LL<<60; static char minF[512];
static int DETAIL = -1, HIST = 0, recording = 0; static long long ghist[64];

static inline int Hadj(int a, int b) { int d = a - b; if (d < 0) d = -d; return d == 1 || d == n - 1; }

/* one CYC line: which unshared H-edges the cycle in path[] gives up, by position */
static void record(void) {
    u32 used[32]; memset(used, 0, sizeof used);
    for (int i = 0; i < n; i++) { int a = path[i], b = path[(i + 1) % n]; used[a] |= 1u << b; used[b] |= 1u << a; }
    printf("CYC %d keep=%d%d lost=", good, (used[0] >> 1) & 1, (used[J] >> (J + 1)) & 1);
    for (int i = 1; i < J; i++) if (!((used[i] >> (i + 1)) & 1)) printf(" A%d/%d", i - 1, J - 1);
    for (int b = 0; b < n - J - 1; b++) { int x = J + 1 + b, y = (x + 1) % n;
        if (!((used[x] >> y) & 1)) printf(" B%d/%d", b, n - J - 1); }
    printf(" cyc=");
    for (int i = 0; i < n; i++) printf(" %d", path[i]);
    printf("\n");
}

static void dfs(int d, u32 vis, int usedU) {
    if (!recording && good >= CAP) return;
    int v = path[d - 1];
    if (d == n) {
        if (!(G[v] & 1u) || path[1] > path[n - 1]) return;
        int u = usedU + (((Hm[v] & ~F[v]) & 1u) ? 1 : 0);
        if (u < n - 2) { good++; if (recording) record(); }
        return;
    }
    u32 c = G[v] & ~vis;
    while (c) {
        int w = __builtin_ctz(c); c &= c - 1;
        path[d] = w;
        dfs(d + 1, vis | (1u << w), usedU + (((Hm[v] & ~F[v]) >> w) & 1));
    }
}

static void process(void) {
    total++;
    for (int i = 0; i < n; i++) G[i] = F[i] | Hm[i];
    good = 0; path[0] = 0;
    dfs(1, 1u, 0);
    int g = good > 3 ? 3 : good;
    hist[g]++;
    if (good < CAP && good < 64) ghist[good]++;
    if (good <= DETAIL) {
        printf("DET n=%d j=%d good=%d F=", n, J, good);
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if ((F[a] >> b) & 1) printf(" %d-%d", a, b);
        printf("\n");
        int g0 = good; good = 0; recording = 1; dfs(1, 1u, 0); recording = 0;
        if (good != g0) { fprintf(stderr, "recount mismatch %d vs %d\n", good, g0); exit(1); }
    }
    if (good < mingood) { mingood = good; int p = 0;
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if ((F[a] >> b) & 1) p += sprintf(minF + p, " %d-%d", a, b);
        printf("NEWMIN n=%d j=%d good=%d F=%s\n", n, J, good, minF); fflush(stdout); }
    if (good <= 2) {
        printf("NEAR n=%d j=%d good=%d F=", n, J, good);
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if ((F[a] >> b) & 1) printf(" %d-%d", a, b);
        printf("\n"); fflush(stdout);
    }
}

static void gen(int v) {
    while (v < n && need[v] == 0) v++;
    if (v == n) { process(); return; }
    if (need[v] == 1) {
        for (int w = v + 1; w < n; w++) if (need[w] > 0 && !Hadj(v, w) && !((F[v] >> w) & 1)) {
            F[v] |= 1u << w; F[w] |= 1u << v; need[v]--; need[w]--;
            gen(v + 1);
            F[v] &= ~(1u << w); F[w] &= ~(1u << v); need[v]++; need[w]++;
        }
    } else {
        for (int a = v + 1; a < n; a++) if (need[a] > 0 && !Hadj(v, a))
            for (int b = a + 1; b < n; b++) if (need[b] > 0 && !Hadj(v, b)) {
                F[v] |= (1u << a) | (1u << b); F[a] |= 1u << v; F[b] |= 1u << v;
                need[v] = 0; need[a]--; need[b]--;
                gen(v + 1);
                F[v] &= ~((1u << a) | (1u << b)); F[a] &= ~(1u << v); F[b] &= ~(1u << v);
                need[v] = 2; need[a]++; need[b]++;
            }
    }
}

int main(int argc, char **argv) {
    n = atoi(argv[1]);
    int jlo = 2, jhi = n - 2; if (getenv("CAP")) CAP = atoi(getenv("CAP"));
    if (getenv("HIST")) HIST = atoi(getenv("HIST"));
    if (getenv("DETAIL")) { DETAIL = atoi(getenv("DETAIL")); if (CAP <= DETAIL) CAP = DETAIL + 1; }
    if (argc > 2) jlo = jhi = atoi(argv[2]);
    for (int i = 0; i < n; i++) Hm[i] = (1u << ((i + 1) % n)) | (1u << ((i + n - 1) % n));
    for (J = jlo; J <= jhi; J++) {
        memset(F, 0, sizeof F);
        for (int i = 0; i < n; i++) need[i] = 2;
        F[0] |= 2u; F[1] |= 1u; need[0]--; need[1]--;
        F[J] |= 1u << (J + 1); F[J + 1] |= 1u << J; need[J]--; need[J + 1]--;
        gen(0);
    }
    printf("MINGOOD %lld F=%s\n", mingood, minF); printf("SUMMARY n=%d j=%d..%d pairs=%lld good0(rigid)=%lld good1=%lld good2=%lld good>=3=%lld\n",
           n, jlo, jhi, total, hist[0], hist[1], hist[2], hist[3]);
    if (HIST) for (int g = 0; g < CAP && g < 64; g++) if (ghist[g]) printf("HIST %d %lld\n", g, ghist[g]);
    return 0;
}
