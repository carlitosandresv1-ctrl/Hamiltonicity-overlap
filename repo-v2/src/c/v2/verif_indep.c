/* Independent verifier, written from scratch (does not reuse repo code).
 * Enumerates every labelled 2-regular simple graph F on [n] by assigning
 * neighbours vertex by vertex, fixes H = (0,1,...,n-1), and for Gamma = F u H
 * enumerates ALL Hamilton cycles by DFS, recording max |F n H'| and the count.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 16
typedef unsigned int u32;
static int n;
static u32 Fadj[MAXN], Gadj[MAXN];
static int degF[MAXN];
static long long total = 0;

/* statistics */
static int minov = 99;
static int minov_s[MAXN + 1];
static long long cnt_s[MAXN + 1];
static long long ext_cnt = 0, ext_uh = 0;
static long long opt_cnt = 0, opt_viol = 0; static int opt_maxhc = 0;
/* s=5 patterns: key = sorted stretch sizes encoded */
static long long pat_cnt[7], pat_uh[7];
static const char *pat_name[7] = {"{5}", "{1,4}", "{2,3}", "{1,1,3}", "{1,2,2}", "{1,1,1,2}", "{1,1,1,1,1}"};
/* UH extremal canonical forms */
#define MAXC 4096
static unsigned long long canon[MAXC][2]; static int ncanon = 0;
static int ext_s_hist[MAXN + 1];

static inline int inH(int a, int b) { int d = a - b; if (d < 0) d = -d; return d == 1 || d == n - 1; }

/* DFS over Hamilton cycles */
static int path[MAXN];
static int hc_count, hc_maxov, cur_s;
static int lemma_violation; /* some H' gives up an H-edge not in F */
static void dfs(int depth, u32 vis, int ovF) {
    int v = path[depth - 1];
    if (depth == n) {
        if (!((Gadj[v] >> 0) & 1)) return;
        if (path[1] > path[n - 1]) return;
        int o = ovF + ((Fadj[v] & 1) ? 1 : 0);
        hc_count++;
        if (o > hc_maxov) hc_maxov = o;
        /* H \ H' : H-edges (i,i+1) not used by H'. check whether all such lie in F */
        {
            static int pos[MAXN];
            for (int i = 0; i < n; i++) pos[path[i]] = i;
            for (int i = 0; i < n; i++) {
                int a = i, b = (i + 1) % n;
                int pa = pos[a], pb = pos[b];
                int d = pa - pb; if (d < 0) d = -d;
                int used = (d == 1 || d == n - 1);
                if (!used && !((Fadj[a] >> b) & 1)) { lemma_violation = 1; }
            }
        }
        return;
    }
    u32 c = Gadj[v] & ~vis;
    while (c) {
        int w = __builtin_ctz(c); c &= c - 1;
        path[depth] = w;
        dfs(depth + 1, vis | (1u << w), ovF + ((Fadj[v] >> w) & 1));
    }
}

static void canon_form(unsigned long long out[2]) {
    unsigned long long best[2] = {~0ULL, ~0ULL};
    for (int refl = 0; refl < 2; refl++)
        for (int r = 0; r < n; r++) {
            unsigned long long m[2] = {0, 0};
            for (int a = 0; a < n; a++)
                for (int b = a + 1; b < n; b++)
                    if ((Fadj[a] >> b) & 1) {
                        int x = refl ? (n - a + r) % n : (a + r) % n;
                        int y = refl ? (n - b + r) % n : (b + r) % n;
                        if (x > y) { int t = x; x = y; y = t; }
                        int idx = x * (2 * n - x - 1) / 2 + (y - x - 1); /* < 120 for n<=16 */
                        if (idx < 64) m[0] |= 1ULL << idx; else m[1] |= 1ULL << (idx - 64);
                    }
            if (m[1] < best[1] || (m[1] == best[1] && m[0] < best[0])) { best[0] = m[0]; best[1] = m[1]; }
        }
    out[0] = best[0]; out[1] = best[1];
}

static int pattern_index(void) {
    /* stretches of S along H */
    int sz[MAXN], c = 0;
    int start = -1;
    for (int i = 0; i < n; i++) { int b = (i + 1) % n; if (!((Fadj[i] >> b) & 1)) { start = b; break; } }
    if (start < 0) return -1;
    int len = 0;
    for (int k = 0; k < n; k++) {
        int i = (start + k) % n, b = (i + 1) % n;
        if ((Fadj[i] >> b) & 1) len++;
        else { if (len) sz[c++] = len; len = 0; }
    }
    if (len) sz[c++] = len;
    /* sort */
    for (int i = 0; i < c; i++) for (int j = i + 1; j < c; j++) if (sz[j] < sz[i]) { int t = sz[i]; sz[i] = sz[j]; sz[j] = t; }
    if (c == 1) return 0;
    if (c == 2) return sz[0] == 1 ? 1 : 2;
    if (c == 3) return sz[2] == 3 ? 3 : 4;
    if (c == 4) return 5;
    return 6;
}

static void process(void) {
    total++;
    int s = 0;
    for (int i = 0; i < n; i++) if ((Fadj[i] >> ((i + 1) % n)) & 1) s++;
    for (int i = 0; i < n; i++) Gadj[i] = Fadj[i] | (1u << ((i + 1) % n)) | (1u << ((i + n - 1) % n));
    hc_count = 0; hc_maxov = -1; lemma_violation = 0; cur_s = s;
    path[0] = 0;
    dfs(1, 1u, 0);
    int ov = hc_maxov;
    cnt_s[s]++;
    if (ov < minov_s[s]) minov_s[s] = ov;
    if (ov == s) { opt_cnt++; if (lemma_violation) opt_viol++; if (hc_count > opt_maxhc) opt_maxhc = hc_count; }
    if (s == 5) { int p = pattern_index(); pat_cnt[p]++; if (hc_count == 1) pat_uh[p]++; }
    if (ov < minov) { minov = ov; ext_cnt = 0; ext_uh = 0; ncanon = 0; memset(ext_s_hist, 0, sizeof ext_s_hist); }
    if (ov == minov) {
        ext_cnt++; ext_s_hist[s]++;
        if (hc_count == 1) {
            ext_uh++;
            unsigned long long cf[2]; canon_form(cf);
            int found = 0;
            for (int i = 0; i < ncanon; i++) if (canon[i][0] == cf[0] && canon[i][1] == cf[1]) { found = 1; break; }
            if (!found && ncanon < MAXC) { canon[ncanon][0] = cf[0]; canon[ncanon][1] = cf[1]; ncanon++; }
        }
    }
}

/* enumerate 2-regular simple graphs: vertex v gets neighbours among higher vertices */
static void gen(int v) {
    while (v < n && degF[v] == 2) v++;
    if (v == n) { process(); return; }
    int need = 2 - degF[v];
    if (need == 1) {
        for (int w = v + 1; w < n; w++) if (degF[w] < 2 && !((Fadj[v] >> w) & 1)) {
            Fadj[v] |= 1u << w; Fadj[w] |= 1u << v; degF[v]++; degF[w]++;
            gen(v + 1);
            Fadj[v] &= ~(1u << w); Fadj[w] &= ~(1u << v); degF[v]--; degF[w]--;
        }
    } else {
        for (int w1 = v + 1; w1 < n; w1++) if (degF[w1] < 2)
            for (int w2 = w1 + 1; w2 < n; w2++) if (degF[w2] < 2) {
                Fadj[v] |= (1u << w1) | (1u << w2); Fadj[w1] |= 1u << v; Fadj[w2] |= 1u << v;
                degF[v] = 2; degF[w1]++; degF[w2]++;
                gen(v + 1);
                Fadj[v] = 0; Fadj[w1] &= ~(1u << v); Fadj[w2] &= ~(1u << v);
                degF[v] = 0; degF[w1]--; degF[w2]--;
            }
    }
}
/* note: a vertex with need==2 has no lower neighbours, so Fadj[v]==0 before; edges to lower
   vertices are never added here, so the graph is simple; components are cycles (2-regular). */

int main(int argc, char **argv) {
    n = atoi(argv[1]);
    for (int i = 0; i <= MAXN; i++) minov_s[i] = 99;
    gen(0);
    printf("n=%d  2-factors=%lld  ov(n)=%d\n", n, total, minov);
    printf("  extremal pairs=%lld  UH extremal=%lld  UH dihedral classes=%d  s-dist of extremal:", ext_cnt, ext_uh, ncanon);
    for (int s = 0; s <= n; s++) if (ext_s_hist[s]) printf(" s=%d:%d", s, ext_s_hist[s]);
    printf("\n  min overlap by s:");
    for (int s = 0; s <= n; s++) if (cnt_s[s]) printf(" s%d=%d(%lld)", s, minov_s[s], cnt_s[s]);
    printf("\n  pairs with H optimal=%lld  Lemma7.5 violations=%lld  max #HC among them=%d\n", opt_cnt, opt_viol, opt_maxhc);
    printf("  s=5 patterns:");
    for (int p = 0; p < 7; p++) printf(" %s=%lld[UH %lld]", pat_name[p], pat_cnt[p], pat_uh[p]);
    printf("\n");
    return 0;
}
