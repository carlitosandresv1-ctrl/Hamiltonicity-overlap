/* Busqueda dirigida de max cor(F) en G = F u H  (H ciclo canonico).
 * Escalada con movimientos 2-opt sobre el 2-factor F y reinicios.
 * uso: ./hunt2 n tope semilla iteraciones
 */
#include <stdio.h>
#include <stdlib.h>

static int n, tope;
static int adj[24];
static int eu[24], ev[24];
static unsigned long long rs;

static unsigned long long rnd(void)
{
    rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs;
}
static int ri(int k) { return (int)(rnd() % (unsigned)k); }

/* ---------- cor ---------- */
static int pa[24], pb[24], np;
static int usado[24], col, fin_actual, jpaths, prim;

static int rec_ens(void)
{
    if (col == jpaths) return (adj[fin_actual] >> prim) & 1;
    for (int i = 1; i < jpaths; i++) {
        if (usado[i]) continue;
        if ((adj[fin_actual] >> pa[i]) & 1) {
            usado[i] = 1;
            int sv = fin_actual; fin_actual = pb[i]; col++;
            if (rec_ens()) return 1;
            col--; fin_actual = sv; usado[i] = 0;
        }
        if (pa[i] != pb[i] && ((adj[fin_actual] >> pb[i]) & 1)) {
            usado[i] = 1;
            int sv = fin_actual; fin_actual = pa[i]; col++;
            if (rec_ens()) return 1;
            col--; fin_actual = sv; usado[i] = 0;
        }
    }
    return 0;
}

static int prueba_R(int Rmask, int j)
{
    int gr[24], ad[24][2], vis[24];
    for (int v = 0; v < n; v++) { gr[v] = 0; vis[v] = 0; }
    for (int i = 0; i < n; i++) {
        if ((Rmask >> i) & 1) continue;
        int u = eu[i], v = ev[i];
        ad[u][gr[u]++] = v;
        ad[v][gr[v]++] = u;
    }
    np = 0;
    int cub = 0;
    for (int s = 0; s < n; s++) {
        if (vis[s] || gr[s] == 2) continue;
        vis[s] = 1; cub++;
        int prev = -1, cur = s;
        while (1) {
            int sig = -1;
            for (int t = 0; t < gr[cur]; t++)
                if (ad[cur][t] != prev) { sig = ad[cur][t]; break; }
            if (sig < 0) break;
            prev = cur; cur = sig;
            vis[cur] = 1; cub++;
        }
        pa[np] = s; pb[np] = cur; np++;
    }
    if (cub != n || np != j) return 0;
    jpaths = j; prim = pa[0];
    for (int i = 0; i < j; i++) usado[i] = 0;
    col = 1; fin_actual = pb[0];
    if (j == 1) return (adj[pb[0]] >> pa[0]) & 1;
    return rec_ens();
}

static int ncic(void)
{
    int ad[24][2], gr[24], vis[24], c = 0;
    for (int v = 0; v < n; v++) { gr[v] = 0; vis[v] = 0; }
    for (int i = 0; i < n; i++) {
        ad[eu[i]][gr[eu[i]]++] = ev[i];
        ad[ev[i]][gr[ev[i]]++] = eu[i];
    }
    for (int s = 0; s < n; s++) {
        if (vis[s]) continue;
        c++;
        int prev = -1, cur = s;
        while (!vis[cur]) {
            vis[cur] = 1;
            int sig = ad[cur][0] != prev ? ad[cur][0] : ad[cur][1];
            prev = cur; cur = sig;
        }
    }
    return c;
}

static int cor_de(void)
{
    int nc = ncic();
    if (nc == 1) return 0;
    for (int v = 0; v < n; v++) adj[v] = 0;
    for (int i = 0; i < n; i++) {
        adj[eu[i]] |= 1 << ev[i];
        adj[ev[i]] |= 1 << eu[i];
    }
    for (int i = 0; i < n; i++) {
        int a = i, b = (i + 1) % n;
        adj[a] |= 1 << b; adj[b] |= 1 << a;
    }
    int combo[26];
    for (int j = nc; j <= tope; j++) {
        for (int i = 0; i < j; i++) combo[i] = i;
        while (1) {
            int R = 0;
            for (int i = 0; i < j; i++) R |= 1 << combo[i];
            if (prueba_R(R, j)) return j;
            int p = j - 1;
            while (p >= 0 && combo[p] == n - j + p) p--;
            if (p < 0) break;
            combo[p]++;
            for (int q = p + 1; q < j; q++) combo[q] = combo[q - 1] + 1;
        }
    }
    return tope + 1;
}

static int existe(int a, int b)
{
    for (int i = 0; i < n; i++)
        if ((eu[i] == a && ev[i] == b) || (eu[i] == b && ev[i] == a)) return 1;
    return 0;
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]);
    tope = atoi(argv[2]);
    rs = strtoull(argv[3], 0, 10) | 1;
    long iters = atol(argv[4]);
    int mejor = -1, bu[24], bv[24];
    for (int rest = 0; rest < 60; rest++) {
        /* arranque: 2-factor aleatorio = ciclo aleatorio (c=1) y luego cortes */
        int perm[24];
        for (int i = 0; i < n; i++) perm[i] = i;
        for (int i = n - 1; i > 0; i--) { int j = ri(i + 1), t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
        for (int i = 0; i < n; i++) {
            int a = perm[i], b = perm[(i + 1) % n];
            eu[i] = a < b ? a : b; ev[i] = a < b ? b : a;
        }
        int cur = cor_de();
        for (long t = 0; t < iters; t++) {
            int i = ri(n), j = ri(n);
            if (i == j) continue;
            int a = eu[i], b = ev[i], c = eu[j], d = ev[j];
            if (a == c || a == d || b == c || b == d) continue;
            int x1, y1, x2, y2;
            if (ri(2)) { x1 = a; y1 = c; x2 = b; y2 = d; }
            else       { x1 = a; y1 = d; x2 = b; y2 = c; }
            if (existe(x1, y1) || existe(x2, y2)) continue;
            int su = eu[i], sv = ev[i], tu = eu[j], tv = ev[j];
            eu[i] = x1 < y1 ? x1 : y1; ev[i] = x1 < y1 ? y1 : x1;
            eu[j] = x2 < y2 ? x2 : y2; ev[j] = x2 < y2 ? y2 : x2;
            int nv = cor_de();
            if (nv >= cur) {
                cur = nv;
                if (nv > mejor) {
                    mejor = nv;
                    for (int q = 0; q < n; q++) { bu[q] = eu[q]; bv[q] = ev[q]; }
                    printf("  cor=%d  (ciclos=%d)  F =", nv, ncic());
                    for (int q = 0; q < n; q++) printf(" (%d,%d)", eu[q], ev[q]);
                    printf("\n"); fflush(stdout);
                }
            } else {
                eu[i] = su; ev[i] = sv; eu[j] = tu; ev[j] = tv;
            }
        }
    }
    printf("n=%d : max cor hallado = %d   (3n/4-2 = %d, ceil(n/2) = %d)\n",
           n, mejor, 3 * n / 4 - 2, (n + 1) / 2);
    (void)bu; (void)bv;
    return 0;
}
