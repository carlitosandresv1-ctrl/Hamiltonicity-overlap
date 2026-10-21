/* Caza de pares UNIVOCAMENTE HAMILTONIANOS con un patron de tramos dado.
 *
 * Fijado el patron {k_1..k_c} (suma 5), coloca los tramos sobre H, completa F
 * con cuerdas y hace recocido simulado sobre las cuerdas (movimientos 2-opt)
 * minimizando el numero de ciclos hamiltonianos de Gamma = F u H.  Si alguna
 * vez llega a 1 con un patron distinto de {1,2,2}, la conjetura del perfil es
 * falsa y el testigo se imprime.
 *
 * uso: ./cazapat n semilla iteraciones k1 k2 ...
 */
#include <stdio.h>
#include <stdlib.h>

#define NMAX 40
#define TOPE 12                      /* corte al contar ciclos hamiltonianos */

static int n, c, k[8];
static int esH[NMAX][NMAX], enF[NMAX][NMAX], enS[NMAX][NMAX];
static int gradoF[NMAX];
static int cu[NMAX], cv[NMAX], ncu;  /* cuerdas de F */
static unsigned long long rs;

static unsigned long long rnd(void)
{ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

/* ---- numero de ciclos hamiltonianos de Gamma, con tope ---- */
static int adj[NMAX][5], gr[NMAX], vis[NMAX], cam[NMAX], prof, nham;

static void dfs(int v)
{
    if (nham >= TOPE) return;
    if (prof == n) {
        if (cam[1] < cam[n - 1])
            for (int t = 0; t < gr[v]; t++) if (adj[v][t] == 0) { nham++; break; }
        return;
    }
    for (int t = 0; t < gr[v]; t++) {
        int w = adj[v][t];
        if (vis[w]) continue;
        vis[w] = 1; cam[prof++] = w;
        dfs(w);
        prof--; vis[w] = 0;
        if (nham >= TOPE) return;
    }
}

static int cuenta(void)
{
    for (int v = 0; v < n; v++) gr[v] = 0;
    static int ya[NMAX][NMAX];
    for (int v = 0; v < n; v++) for (int w = 0; w < n; w++) ya[v][w] = 0;
    for (int v = 0; v < n; v++) for (int w = v + 1; w < n; w++)
        if (enF[v][w] || esH[v][w]) {
            if (!ya[v][w]) { ya[v][w] = ya[w][v] = 1;
                             adj[v][gr[v]++] = w; adj[w][gr[w]++] = v; }
        }
    nham = 0;
    for (int v = 0; v < n; v++) vis[v] = 0;
    vis[0] = 1; cam[0] = 0; prof = 1;
    dfs(0);
    return nham;
}

/* ---- completar F con cuerdas, al azar ---- */
static int completa(void)
{
    int v = -1;
    for (int i = 0; i < n; i++) if (gradoF[i] < 2) { v = i; break; }
    if (v < 0) return 1;
    int cand[NMAX], m = 0;
    for (int w = 0; w < n; w++)
        if (w != v && gradoF[w] < 2 && !esH[v][w] && !enF[v][w]) cand[m++] = w;
    for (int i = m - 1; i > 0; i--) { int j = rnd() % (i + 1); int t = cand[i]; cand[i] = cand[j]; cand[j] = t; }
    for (int i = 0; i < m; i++) {
        int w = cand[i];
        enF[v][w] = enF[w][v] = 1; gradoF[v]++; gradoF[w]++;
        cu[ncu] = v; cv[ncu] = w; ncu++;
        if (completa()) return 1;
        ncu--; gradoF[v]--; gradoF[w]--; enF[v][w] = enF[w][v] = 0;
    }
    return 0;
}

static int monta(void)                /* coloca los tramos al azar y completa */
{
    for (int v = 0; v < n; v++) { gradoF[v] = 0;
        for (int w = 0; w < n; w++) { enF[v][w] = 0; enS[v][w] = 0; } }
    ncu = 0;
    /* huecos aleatorios >= 1 */
    int g[8], libre = n - 5;
    for (int i = 0; i < c; i++) g[i] = 1;
    for (int r = 0; r < libre - c; r++) g[rnd() % c]++;
    int pos = rnd() % n;
    for (int j = 0; j < c; j++) {
        for (int t = 0; t < k[j]; t++) {
            int a = pos % n, b = (pos + 1) % n;
            enF[a][b] = enF[b][a] = 1; enS[a][b] = enS[b][a] = 1;
            gradoF[a]++; gradoF[b]++; pos++;
        }
        pos += g[j];
    }
    for (int v = 0; v < n; v++) if (gradoF[v] > 2) return 0;
    return completa();
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]);
    rs = strtoull(argv[2], 0, 10) | 1;
    long iters = atol(argv[3]);
    c = argc - 4;
    for (int i = 0; i < c; i++) k[i] = atoi(argv[4 + i]);

    for (int u = 0; u < n; u++) for (int v = 0; v < n; v++) esH[u][v] = 0;
    for (int i = 0; i < n; i++) { int a = i, b = (i + 1) % n; esH[a][b] = esH[b][a] = 1; }

    int global = 1 << 30;
    for (int intento = 0; intento < 40; intento++) {
        if (!monta()) continue;
        int act = cuenta();
        if (act == 0) continue;                 /* no hamiltoniano: imposible, H esta */
        for (long t = 0; t < iters; t++) {
            if (ncu < 2) break;
            int i = rnd() % ncu, j = rnd() % ncu;
            if (i == j) continue;
            int a = cu[i], b = cv[i], x = cu[j], y = cv[j];
            if (a == x || a == y || b == x || b == y) continue;
            int p1, q1, p2, q2;
            if (rnd() & 1) { p1 = a; q1 = x; p2 = b; q2 = y; }
            else           { p1 = a; q1 = y; p2 = b; q2 = x; }
            if (esH[p1][q1] || esH[p2][q2]) continue;
            if (enF[p1][q1] || enF[p2][q2]) continue;
            enF[a][b] = enF[b][a] = 0; enF[x][y] = enF[y][x] = 0;
            enF[p1][q1] = enF[q1][p1] = 1; enF[p2][q2] = enF[q2][p2] = 1;
            int nue = cuenta();
            int acepta = (nue <= act) || ((rnd() % 1000) < 3);
            if (acepta) {
                cu[i] = p1; cv[i] = q1; cu[j] = p2; cv[j] = q2;
                act = nue;
                if (act < global) {
                    global = act;
                    if (act == 1) {
                        printf("n=%d  patron {", n);
                        for (int q = 0; q < c; q++) printf("%d%s", k[q], q + 1 < c ? "," : "");
                        printf("}  UNICO!  F =");
                        for (int v = 0; v < n; v++) for (int w = v + 1; w < n; w++)
                            if (enF[v][w]) printf(" (%d,%d)", v, w);
                        printf("\n"); fflush(stdout);
                        return 0;
                    }
                }
            } else {
                enF[p1][q1] = enF[q1][p1] = 0; enF[p2][q2] = enF[q2][p2] = 0;
                enF[a][b] = enF[b][a] = 1; enF[x][y] = enF[y][x] = 1;
            }
        }
    }
    printf("n=%d  patron {", n);
    for (int q = 0; q < c; q++) printf("%d%s", k[q], q + 1 < c ? "," : "");
    printf("}  minimo de ciclos hamiltonianos alcanzado = %d\n", global);
    return 0;
}
