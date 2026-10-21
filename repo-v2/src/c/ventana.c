/* Verificacion exhaustiva de la ventana:  existe algun par (F,H) con
 * |F cap H| <= SOBJ y solapamiento maximo <= 4 ?
 *
 * Test rapido: en vez de calcular cor(F) entero, enumeramos ciclos
 * Hamiltonianos de Gamma = F u H y paramos en cuanto uno solapa >= 5.
 * Si ninguno llega a 5, el par se reporta como candidato.
 *
 * uso: ./ventana n smax
 */
#include <stdio.h>
#include <stdlib.h>

static int n, smax;
static int eu[24], ev[24];
static int adj[24][5], gr[24];
static int esF[24][24];
static long long cuenta = 0, cand = 0;
static int mejor_sol;           /* mejor solapamiento hallado en el par actual */

/* ---- enumeracion de ciclos Hamiltonianos con salida temprana ---- */
static int vis[24], cam[24], prof;

static int dfs(int v, int sol)
{
    if (prof == n) {
        /* cerrar con la arista v-0 */
        int cierra = 0;
        for (int t = 0; t < gr[v]; t++) if (adj[v][t] == 0) cierra = 1;
        if (!cierra) return 0;
        int s2 = sol + esF[v][0];
        if (s2 > mejor_sol) mejor_sol = s2;
        return s2 >= 5;
    }
    for (int t = 0; t < gr[v]; t++) {
        int w = adj[v][t];
        if (vis[w]) continue;
        vis[w] = 1; cam[prof++] = w;
        if (dfs(w, sol + esF[v][w])) { vis[w] = 0; prof--; return 1; }
        vis[w] = 0; prof--;
    }
    return 0;
}

static void evalua(void)
{
    int sh = 0;
    for (int i = 0; i < n; i++) {
        int x = eu[i], y = ev[i];
        if (y - x == 1 || (x == 0 && y == n - 1)) sh++;
    }
    if (sh > smax) return;
    cuenta++;

    for (int v = 0; v < n; v++) { gr[v] = 0; for (int w = 0; w < n; w++) esF[v][w] = 0; }
    for (int i = 0; i < n; i++) { esF[eu[i]][ev[i]] = esF[ev[i]][eu[i]] = 1; }
    /* adyacencia de Gamma = F u H */
    static int ya[24][24];
    for (int v = 0; v < n; v++) for (int w = 0; w < n; w++) ya[v][w] = 0;
    for (int i = 0; i < n; i++) {
        int a = eu[i], b = ev[i];
        if (!ya[a][b]) { ya[a][b] = ya[b][a] = 1; adj[a][gr[a]++] = b; adj[b][gr[b]++] = a; }
    }
    for (int i = 0; i < n; i++) {
        int a = i, b = (i + 1) % n;
        if (!ya[a][b]) { ya[a][b] = ya[b][a] = 1; adj[a][gr[a]++] = b; adj[b][gr[b]++] = a; }
    }

    mejor_sol = -1;
    for (int v = 0; v < n; v++) vis[v] = 0;
    vis[0] = 1; cam[0] = 0; prof = 1;
    int hay = dfs(0, 0);
    if (!hay) {
        /* ningun ciclo Hamiltoniano solapa >= 5 */
        cand++;
        printf("  CANDIDATO s=%d solapamiento_max=%d  F =", sh, mejor_sol);
        for (int i = 0; i < n; i++) printf(" (%d,%d)", eu[i], ev[i]);
        printf("\n"); fflush(stdout);
    }
}

/* ---- generacion de todos los 2-factores de [n] con poda en s ---- */
static void gen(int mask);

static void orden(int mask, int v, int S, int *ord, int k, int pos)
{
    if (pos == k) {
        if (k > 2 && ord[1] > ord[k - 1]) return;
        int pos0 = 0;
        while (pos0 < n && eu[pos0] >= 0) pos0++;
        int comp = 0;
        for (int i = 0; i < pos0; i++) {
            int x = eu[i], y = ev[i];
            if (y - x == 1 || (x == 0 && y == n - 1)) comp++;
        }
        for (int i = 0; i < k; i++) {
            int a = ord[i], b = ord[(i + 1) % k];
            int x = a < b ? a : b, y = a < b ? b : a;
            if (y - x == 1 || (x == 0 && y == n - 1)) comp++;
            eu[pos0 + i] = x; ev[pos0 + i] = y;
        }
        if (comp <= smax) gen(mask & ~S);
        for (int i = 0; i < k; i++) { eu[pos0 + i] = -1; ev[pos0 + i] = -1; }
        return;
    }
    int rest = S & ~(1 << v);
    for (int w = 0; w < n; w++) {
        if (!((rest >> w) & 1)) continue;
        int ya2 = 0;
        for (int i = 1; i < pos; i++) if (ord[i] == w) { ya2 = 1; break; }
        if (ya2) continue;
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
    for (int S = resto; ; S = (S - 1) & resto) {
        int k = __builtin_popcount(S) + 1;
        if (k >= 3) {
            int Sc = S | (1 << v);
            int ord[24];
            ord[0] = v;
            orden(mask, v, Sc, ord, k, 1);
        }
        if (S == 0) break;
    }
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]);
    smax = atoi(argv[2]);
    for (int i = 0; i < 24; i++) { eu[i] = -1; ev[i] = -1; }
    gen((1 << n) - 1);
    printf("n=%d  smax=%d : %lld pares examinados, %lld candidatos con solapamiento <= 4\n",
           n, smax, cuenta, cand);
    return 0;
}
