/* Funcion extremal exacta  Dmax(n) = max_{G ham, F 2-factor} cor_G(F).
 *
 * Reduccion: el maximo se alcanza en G = F u H con H ciclo hamiltoniano.
 * Fijamos H = (0,1,...,n-1) y recorremos TODOS los 2-factores F de [n].
 *
 * cor(F) = min { j : existe R subset F, |R|=j, F-R bosque lineal generador,
 *                    cuyos caminos se ensamblan ciclicamente con aristas de G }
 *
 * uso:  ./exh n [tope]
 */
#include <stdio.h>
#include <stdlib.h>

static int n, tope, modo;   /* 0=todos 1=4-regular(F cap H vacio) 2=delta>=3 */
static int adj[20];
static int eu[20], ev[20];
static int nc;
static int maxcor[24];
static long long cuenta = 0;

/* ---------- ensamblaje de caminos ---------- */
static int pa[20], pb[20], np;
static int usado[20], col, fin_actual, jpaths, prim;

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
    int gr[20], ad[20][2], vis[20];
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

static int cor_de(void)
{
    if (nc == 1) return 0;
    int combo[24];
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

static void evalua(void)
{
    if (modo == 2) {
        int gH[20];
        for (int v = 0; v < n; v++) gH[v] = 0;
        for (int i = 0; i < n; i++) {
            int x = eu[i], y = ev[i];
            if (y - x == 1 || (x == 0 && y == n - 1)) { gH[x]++; gH[y]++; }
        }
        for (int v = 0; v < n; v++) if (gH[v] == 2) return;
    }
    cuenta++;
    for (int v = 0; v < n; v++) adj[v] = 0;
    for (int i = 0; i < n; i++) {
        adj[eu[i]] |= 1 << ev[i];
        adj[ev[i]] |= 1 << eu[i];
    }
    for (int i = 0; i < n; i++) {
        int a = i, b = (i + 1) % n;
        adj[a] |= 1 << b; adj[b] |= 1 << a;
    }
    int c = cor_de();
    if (c > maxcor[nc]) {
        maxcor[nc] = c;
        printf("  c=%d  cor=%d   F =", nc, c);
        for (int i = 0; i < n; i++) printf(" (%d,%d)", eu[i], ev[i]);
        printf("\n"); fflush(stdout);
    }
}

/* ---------- generacion de todos los 2-factores ---------- */
/* gen(mask): completa un 2-factor sobre el conjunto de vertices mask */

static void gen(int mask);

static void orden(int mask, int v, int S, int *ord, int k, int pos)
{
    if (pos == k) {
        if (k > 2 && ord[1] > ord[k - 1]) return;   /* mata reflexiones */
        /* colocamos las k aristas al final del array */
        int pos0 = 0;
        for (pos0 = 0; pos0 < n; pos0++) if (eu[pos0] < 0) break;
        for (int i = 0; i < k; i++) {
            int a = ord[i], b = ord[(i + 1) % k];
            int x = a < b ? a : b, y = a < b ? b : a;
            if (modo == 1 && (y - x == 1 || (x == 0 && y == n - 1))) {
                for (int q = 0; q < i; q++) { eu[pos0 + q] = -1; ev[pos0 + q] = -1; }
                return;
            }
            eu[pos0 + i] = x; ev[pos0 + i] = y;
        }
        nc++;
        gen(mask & ~S);
        nc--;
        for (int i = 0; i < k; i++) { eu[pos0 + i] = -1; ev[pos0 + i] = -1; }
        return;
    }
    int rest = S & ~(1 << v);
    for (int w = 0; w < n; w++) {
        if (!((rest >> w) & 1)) continue;
        int ya = 0;
        for (int i = 1; i < pos; i++) if (ord[i] == w) { ya = 1; break; }
        if (ya) continue;
        ord[pos] = w;
        orden(mask, v, S, ord, k, pos + 1);
    }
}

static void gen(int mask)
{
    if (mask == 0) { evalua(); return; }
    int v = -1;
    for (int i = 0; i < n; i++) if ((mask >> i) & 1) { v = i; break; }
    int resto = mask & ~(1 << v);
    /* subconjuntos S' de resto con |S'| >= 2 ; el ciclo es {v} u S' */
    for (int S = resto; ; S = (S - 1) & resto) {
        int k = __builtin_popcount(S) + 1;
        if (k >= 3) {
            int Sc = S | (1 << v);
            int ord[20];
            ord[0] = v;
            orden(mask, v, Sc, ord, k, 1);
        }
        if (S == 0) break;
    }
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]);
    tope = argc > 2 ? atoi(argv[2]) : n;
    modo = argc > 3 ? atoi(argv[3]) : 0;
    for (int i = 0; i < 24; i++) maxcor[i] = -1;
    for (int i = 0; i < 20; i++) { eu[i] = -1; ev[i] = -1; }
    nc = 0;
    gen((1 << n) - 1);
    printf("[modo %d] n=%d  2-factores recorridos = %lld\n", modo, n, cuenta);
    int glob = -1;
    for (int c = 1; c < 24; c++) if (maxcor[c] >= 0) {
        printf("  c=%2d : max cor = %d\n", c, maxcor[c]);
        if (maxcor[c] > glob) glob = maxcor[c];
    }
    printf("  Dmax(%d) = %d     (floor(n/2) = %d)\n", n, glob, n / 2);
    return 0;
}
