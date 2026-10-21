/* Pattern {1,1,1} search (and, with M=2, pattern {1,1} again as a cross-check of near11).
 * H = (0,1,...,n-1).  S = M unit stretches (p_i, p_i+1) with p_0 = 0, p_{i+1} >= p_i + 2,
 * p_{M-1} <= n-2, so that no two stretches share a vertex; all other F-edges are chords.
 * For each 2-factor F with F n H = S, count the Hamilton cycles of Gamma = F u H that give
 * up some UNSHARED H-edge ("good" cycles; by Cor. 7.9 the pair is rigid iff there are none).
 *
 * usage: [M=3] [CAP=40] [HIST=1] [DETAIL=T] [LOC=1 [LOCSHOW=t]] near111 n [p1 [p2]]
 *   CAP      early-exit threshold on the number of good cycles (default 3).
 *   HIST=1   exact histogram of good cycles for g < CAP.
 *   DETAIL=T for every pair with at most T good cycles print a DET line and one CYC line per
 *            good cycle: keep=<bits of S kept> lost= A<i>:<a>/<len> ... cyc= ...
 *            Arc A<i> runs from w_i = p_i + 1 to u_{i+1} = p_{i+1} (indices mod M) and has len
 *            edges; A<i>:<a> is its a-th edge counted from w_i.
 *   LOC=1    also compute, per pair, the least number t of chords (edges of F not in H) used
 *            by a good cycle, i.e. t = |H' \ H| minimised over good H'.  Prints LOCHIST t count
 *            and, for pairs with t >= LOCSHOW (default 99), a LOC line with F and one optimal H'.
 *   NOCUT=1  for the pairs with good < CAP (CAP <= 64), split the histogram by whether Gamma has
 *            a 2-edge cut (CUTHIST / NOCUTHIST); a NOCUT line for every cut-free pair.
 *   p1 [p2]  fix the stretch positions instead of running over all of them.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned int u32;
static int n, M = 3, P[4];
static u32 F[32], G[32], Hm[32], Um[32];          /* Um = unshared H-edges */
static int need[32];
static long long total, hist[4], ghist[64], lochist[33];
static int path[32], good, CAP = 3, DETAIL = -1, HIST = 0, LOC = 0, LOCSHOW = 99, recording = 0;
static long long mingood = 1LL << 60; static char minF[512];
static int bestt, bestpath[32];

static inline int Hadj(int a, int b) { int d = a - b; if (d < 0) d = -d; return d == 1 || d == n - 1; }

static void printF(void) {
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if ((F[a] >> b) & 1) printf(" %d-%d", a, b);
}

static void lostpos(const int *pth) {
    u32 used[32]; memset(used, 0, sizeof used);
    for (int i = 0; i < n; i++) { int a = pth[i], b = pth[(i + 1) % n]; used[a] |= 1u << b; used[b] |= 1u << a; }
    printf("keep=");
    for (int i = 0; i < M; i++) printf("%d", (used[P[i]] >> (P[i] + 1)) & 1);
    printf(" lost=");
    for (int i = 0; i < M; i++) {
        int w = P[i] + 1, u = (i + 1 < M) ? P[i + 1] : n, len = u - w;   /* arc w..u, u = n means vertex 0 */
        for (int a = 0; a < len; a++) { int x = w + a, y = (x + 1) % n;
            if (!((used[x] >> y) & 1)) printf(" A%d:%d/%d", i, a, len); }
    }
    printf(" cyc=");
    for (int i = 0; i < n; i++) printf(" %d", pth[i]);
    printf("\n");
}

/* count good cycles; usedU = unshared H-edges used so far */
static void dfs(int d, u32 vis, int usedU) {
    if (!recording && good >= CAP) return;
    int v = path[d - 1];
    if (d == n) {
        if (!(G[v] & 1u) || path[1] > path[n - 1]) return;
        int u = usedU + (Um[v] & 1u);
        if (u < n - M) { good++; if (recording) { printf("CYC %d ", good); lostpos(path); } }
        return;
    }
    u32 c = G[v] & ~vis;
    while (c) {
        int w = __builtin_ctz(c); c &= c - 1;
        path[d] = w;
        dfs(d + 1, vis | (1u << w), usedU + ((Um[v] >> w) & 1));
    }
}

/* CLAIMS=1: per pair, does some good cycle (C1) keep every shared edge, (C2) give up an
 * unshared edge adjacent to a stretch?  Prints CLAIMFAIL lines and a CLAIMS summary.
 * Also (C3) does some good cycle give up a shared edge?  kmask has bit K set when some
 * good cycle keeps exactly the subset K of S (bit i of K = stretch i); KMASK lines give
 * the histogram of kmask over all pairs. */
static int CLAIMS = 0, c1, c2; static u32 adjU[32]; static int NA; static long long fail1, fail2, fail12;
static u32 sbit[32], kmask; static long long fail3, kmhist[256];
static void dfsclaim(int d, u32 vis, int usedU, u32 keptS, int usedAdj) {
    int v = path[d - 1];
    if (d == n) {
        if (!(G[v] & 1u) || path[1] > path[n - 1]) return;
        int u = usedU + (Um[v] & 1u), a = usedAdj + (adjU[v] & 1u);
        u32 k = keptS | ((Hm[v] & F[v] & 1u) ? sbit[v] : 0);
        if (u < n - M) { if (k == (1u << M) - 1) c1 = 1; if (a < NA) c2 = 1; kmask |= 1u << k; }
        return;
    }
    u32 c = G[v] & ~vis;
    while (c) {
        int w = __builtin_ctz(c); c &= c - 1;
        path[d] = w;
        dfsclaim(d + 1, vis | (1u << w), usedU + ((Um[v] >> w) & 1), keptS | ((((Hm[v] & F[v]) >> w) & 1) ? sbit[v] : 0), usedAdj + ((adjU[v] >> w) & 1));
    }
}

/* least number of chords in a good cycle (branch and bound on chords used) */
static void dfsloc(int d, u32 vis, int usedU, int ch) {
    if (ch >= bestt) return;
    int v = path[d - 1];
    if (d == n) {
        if (!(G[v] & 1u)) return;
        int u = usedU + (Um[v] & 1u), c2 = ch + !((Hm[v] & 1u));
        if (u < n - M && c2 < bestt) { bestt = c2; memcpy(bestpath, path, sizeof path); }
        return;
    }
    u32 c = G[v] & ~vis;
    u32 hfirst = c & Hm[v], rest = c & ~Hm[v];         /* try H-edges first */
    while (hfirst) { int w = __builtin_ctz(hfirst); hfirst &= hfirst - 1;
        path[d] = w; dfsloc(d + 1, vis | (1u << w), usedU + ((Um[v] >> w) & 1), ch); }
    while (rest) { int w = __builtin_ctz(rest); rest &= rest - 1;
        path[d] = w; dfsloc(d + 1, vis | (1u << w), usedU, ch + 1); }
}

/* NOCUT=1: for every pair with good < CAP, does Gamma have a 2-edge cut?  Histograms of
 * good for pairs with and without one (NOCUTHIST / CUTHIST) and a NOCUT line per cut-free
 * pair.  The test removes every pair of edges and checks connectivity (bitmask BFS). */
static int NOCUT = 0; static long long cuthist[64], nocuthist[64];
static int connected(void) {
    u32 seen = 1u, frontier = 1u, all = (n == 32) ? ~0u : ((1u << n) - 1);
    while (frontier) {
        u32 nxt = 0;
        for (u32 f = frontier; f; f &= f - 1) nxt |= G[__builtin_ctz(f)];
        frontier = nxt & ~seen; seen |= nxt;
    }
    return seen == all;
}
static int hascut(void) {
    int ea[64], eb[64], ne = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if ((G[a] >> b) & 1) { ea[ne] = a; eb[ne] = b; ne++; }
    for (int i = 0; i < ne; i++) {
        G[ea[i]] &= ~(1u << eb[i]); G[eb[i]] &= ~(1u << ea[i]);
        for (int j = i + 1; j < ne; j++) {
            G[ea[j]] &= ~(1u << eb[j]); G[eb[j]] &= ~(1u << ea[j]);
            int c = connected();
            G[ea[j]] |= 1u << eb[j]; G[eb[j]] |= 1u << ea[j];
            if (!c) { G[ea[i]] |= 1u << eb[i]; G[eb[i]] |= 1u << ea[i]; return 1; }
        }
        G[ea[i]] |= 1u << eb[i]; G[eb[i]] |= 1u << ea[i];
    }
    return 0;
}

static void process(void) {
    total++;
    for (int i = 0; i < n; i++) { G[i] = F[i] | Hm[i]; Um[i] = Hm[i] & ~F[i]; }
    good = 0; path[0] = 0;
    dfs(1, 1u, 0);
    int g = good > 3 ? 3 : good;
    hist[g]++;
    if (good < CAP && good < 64) ghist[good]++;
    if (good < mingood) { mingood = good; int p = 0;
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if ((F[a] >> b) & 1) p += sprintf(minF + p, " %d-%d", a, b); }
    if (good <= 2) { printf("NEAR n=%d p=", n); for (int i = 0; i < M; i++) printf("%d%s", P[i], i + 1 < M ? "," : "");
        printf(" good=%d F=", good); printF(); printf("\n"); fflush(stdout); }
    if (NOCUT && good < CAP && good < 64) {
        if (hascut()) cuthist[good]++;
        else { nocuthist[good]++;
            printf("NOCUT n=%d p=%d good=%d F=", n, P[1], good); printF(); printf("\n"); }
    }
    if (good <= DETAIL) {
        printf("DET n=%d p=", n); for (int i = 0; i < M; i++) printf("%d%s", P[i], i + 1 < M ? "," : "");
        printf(" good=%d F=", good); printF(); printf("\n");
        int g0 = good; good = 0; recording = 1; dfs(1, 1u, 0); recording = 0;
        if (good != g0) { fprintf(stderr, "recount mismatch %d vs %d\n", good, g0); exit(1); }
    }
    if (CLAIMS) {
        memset(adjU, 0, sizeof adjU);               /* the 2M unshared H-edges next to a stretch */
        for (int i = 0; i < M; i++) { int a = P[i], b = P[i] + 1, x = (a + n - 1) % n, y = (b + 1) % n;
            adjU[x] |= 1u << a; adjU[a] |= 1u << x; adjU[b] |= 1u << y; adjU[y] |= 1u << b; }
        NA = 0; for (int i = 0; i < n; i++) NA += __builtin_popcount(adjU[i]); NA /= 2;
        memset(sbit, 0, sizeof sbit);
        for (int i = 0; i < M; i++) sbit[P[i]] = sbit[P[i] + 1] = 1u << i;
        c1 = c2 = 0; kmask = 0; path[0] = 0; dfsclaim(1, 1u, 0, 0, 0);
        int c3 = (kmask & ~(1u << ((1u << M) - 1))) != 0;
        kmhist[kmask & 255]++;
        if (!c1) fail1++;
        if (!c2) fail2++;
        if (!c3) fail3++;
        if (!c1 && !c2) fail12++;
        if (!c1 || !c2) { printf("CLAIMFAIL C1=%d C2=%d n=%d good=%d F=", c1, c2, n, good); printF(); printf("\n"); }
        if (!c3) { printf("C3FAIL n=%d good=%d kmask=%u F=", n, good, kmask); printF(); printf("\n"); }
    }
    if (LOC && good > 0) {
        bestt = 33; path[0] = 0; dfsloc(1, 1u, 0, 0);
        if (bestt > 32) { fprintf(stderr, "LOC found no good cycle although good=%d\n", good); exit(1); }
        lochist[bestt]++;
        if (bestt >= LOCSHOW) { printf("LOC n=%d t=%d good=%d F=", n, bestt, good); printF(); printf(" | "); lostpos(bestpath); }
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

static void run(void) {
    memset(F, 0, sizeof F);
    for (int i = 0; i < n; i++) need[i] = 2;
    for (int i = 0; i < M; i++) { int a = P[i], b = P[i] + 1;
        F[a] |= 1u << b; F[b] |= 1u << a; need[a]--; need[b]--; }
    gen(0);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: [M=3] near111 n [p1 [p2]]\n"); return 1; }
    n = atoi(argv[1]);
    if (getenv("M")) M = atoi(getenv("M"));
    if (M < 2 || M > 3 || n > 31) { fprintf(stderr, "M must be 2 or 3, n <= 31\n"); return 1; }
    if (getenv("CAP")) CAP = atoi(getenv("CAP"));
    if (getenv("HIST")) HIST = atoi(getenv("HIST"));
    if (getenv("LOC")) LOC = atoi(getenv("LOC"));
    if (getenv("LOCSHOW")) LOCSHOW = atoi(getenv("LOCSHOW"));
    if (getenv("CLAIMS")) CLAIMS = atoi(getenv("CLAIMS"));
    if (getenv("NOCUT")) NOCUT = atoi(getenv("NOCUT"));
    if (NOCUT && CAP > 64) CAP = 64;
    if (getenv("DETAIL")) { DETAIL = atoi(getenv("DETAIL")); if (CAP <= DETAIL) CAP = DETAIL + 1; }
    for (int i = 0; i < n; i++) Hm[i] = (1u << ((i + 1) % n)) | (1u << ((i + n - 1) % n));
    P[0] = 0;
    int fix1 = argc > 2 ? atoi(argv[2]) : -1, fix2 = argc > 3 ? atoi(argv[3]) : -1;
    for (P[1] = 2; P[1] <= n - 2; P[1]++) {
        if (fix1 >= 0 && P[1] != fix1) continue;
        if (M == 2) { run(); continue; }
        for (P[2] = P[1] + 2; P[2] <= n - 2; P[2]++) {
            if (fix2 >= 0 && P[2] != fix2) continue;
            run();
        }
    }
    printf("MINGOOD %lld F=%s\n", mingood, minF);
    printf("SUMMARY n=%d M=%d pairs=%lld good0(rigid)=%lld good1=%lld good2=%lld good>=3=%lld\n",
           n, M, total, hist[0], hist[1], hist[2], hist[3]);
    if (HIST) for (int g = 0; g < CAP && g < 64; g++) if (ghist[g]) printf("HIST %d %lld\n", g, ghist[g]);
    if (NOCUT) for (int g = 0; g < CAP && g < 64; g++) {
        if (cuthist[g]) printf("CUTHIST %d %lld\n", g, cuthist[g]);
        if (nocuthist[g]) printf("NOCUTHIST %d %lld\n", g, nocuthist[g]); }
    if (LOC) for (int t = 0; t <= 32; t++) if (lochist[t]) printf("LOCHIST %d %lld\n", t, lochist[t]);
    if (CLAIMS) printf("CLAIMS n=%d M=%d pairs=%lld fail_C1(keep all S)=%lld fail_C2(lose edge next to stretch)=%lld fail_both=%lld\n",
                       n, M, total, fail1, fail2, fail12);
    if (CLAIMS) { printf("C3 n=%d M=%d pairs=%lld fail_C3(give up a shared edge)=%lld\n", n, M, total, fail3);
        for (int k = 0; k < 256; k++) if (kmhist[k]) printf("KMASK %d %lld\n", k, kmhist[k]); }
    return 0;
}
