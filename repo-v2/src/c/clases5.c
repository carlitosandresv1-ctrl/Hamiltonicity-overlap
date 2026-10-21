/* Clasifica los pares EXTREMALES UNIVOCAMENTE HAMILTONIANOS con solapamiento 5.
 *
 * Observacion que hace esto exhaustivo y rapido: si Gamma = F u H es
 * univocamente Hamiltoniano, su unico ciclo Hamiltoniano es H, de modo que el
 * solapamiento maximo vale exactamente s = |F cap H|.  Un par extremal UH con
 * solapamiento 5 cumple por tanto s = 5, y basta generar los 2-factores con
 * exactamente 5 aristas compartidas (podando durante la generacion) y contar
 * los ciclos Hamiltonianos de Gamma con salida temprana en 2.
 *
 * uso: ./clases5 n
 */
#include <stdio.h>
#include <stdlib.h>

static int n;
static int eu[24], ev[24];
static int adj[24][5], gr[24];
static long long tot = 0, tot_uh = 0;

#define MAXCL 65536
static unsigned __int128 clave[MAXCL];
static int nclases = 0;

static int idx(int u, int v)
{
    int a = u < v ? u : v, b = u < v ? v : u;
    return a * n - a * (a + 1) / 2 + (b - a - 1);
}

static unsigned __int128 canon(void)
{
    unsigned __int128 mejor = 0;
    int primero = 1;
    for (int sh = 0; sh < n; sh++) {
        for (int d = -1; d <= 1; d += 2) {
            unsigned __int128 m = 0;
            for (int i = 0; i < n; i++) {
                int a = ((eu[i] * d + sh) % n + n) % n;
                int b = ((ev[i] * d + sh) % n + n) % n;
                m |= ((unsigned __int128)1) << idx(a, b);
            }
            if (primero || m < mejor) { mejor = m; primero = 0; }
        }
    }
    return mejor;
}

static int vis[24], cam[24], prof, nham;

static int dfs(int v)                   /* devuelve 1 si ya hay 2 ciclos */
{
    if (prof == n) {
        /* cada ciclo se recorreria en dos sentidos: exigimos cam[1] < cam[n-1] */
        if (cam[1] >= cam[n - 1]) return 0;
        for (int t = 0; t < gr[v]; t++)
            if (adj[v][t] == 0) { nham++; break; }
        return nham >= 2;
    }
    for (int t = 0; t < gr[v]; t++) {
        int w = adj[v][t];
        if (vis[w]) continue;
        vis[w] = 1; cam[prof++] = w;
        int r = dfs(w);
        prof--; vis[w] = 0;
        if (r) return 1;
    }
    return 0;
}

static void evalua(void)
{
    tot++;
    for (int v = 0; v < n; v++) gr[v] = 0;
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
    nham = 0;
    for (int v = 0; v < n; v++) vis[v] = 0;
    vis[0] = 1; cam[0] = 0; prof = 1;
    dfs(0);
    if (nham != 1) return;
    tot_uh++;
    unsigned __int128 k = canon();
    for (int i = 0; i < nclases; i++) if (clave[i] == k) return;
    if (nclases < MAXCL) {
        clave[nclases++] = k;
        printf("  clase %d: F =", nclases);
        for (int i = 0; i < n; i++) printf(" (%d,%d)", eu[i], ev[i]);
        printf("   S =");
        for (int i = 0; i < n; i++) {
            int x = eu[i], y = ev[i];
            if (y - x == 1 || (x == 0 && y == n - 1)) printf(" (%d,%d)", x, y);
        }
        printf("\n"); fflush(stdout);
    }
}

static void gen(int mask, int comp);

static void orden(int mask, int v, int S, int *ord, int k, int pos, int comp)
{
    if (pos == k) {
        if (k > 2 && ord[1] > ord[k - 1]) return;
        int pos0 = 0;
        while (pos0 < n && eu[pos0] >= 0) pos0++;
        int c2 = comp;
        for (int i = 0; i < k; i++) {
            int a = ord[i], b = ord[(i + 1) % k];
            int x = a < b ? a : b, y = a < b ? b : a;
            if (y - x == 1 || (x == 0 && y == n - 1)) c2++;
            eu[pos0 + i] = x; ev[pos0 + i] = y;
        }
        if (c2 <= 5) gen(mask & ~S, c2);
        for (int i = 0; i < k; i++) { eu[pos0 + i] = -1; ev[pos0 + i] = -1; }
        return;
    }
    int rest = S & ~(1 << v);
    for (int w = 0; w < n; w++) {
        if (!((rest >> w) & 1)) continue;
        int rep = 0;
        for (int i = 1; i < pos; i++) if (ord[i] == w) { rep = 1; break; }
        if (rep) continue;
        ord[pos] = w;
        orden(mask, v, S, ord, k, pos + 1, comp);
    }
}

static void gen(int mask, int comp)
{
    if (mask == 0) { if (comp == 5) evalua(); return; }
    int v = -1;
    for (int i = 0; i < n; i++) if ((mask >> i) & 1) { v = i; break; }
    int resto = mask & ~(1 << v);
    for (int S = resto; ; S = (S - 1) & resto) {
        int k = __builtin_popcount(S) + 1;
        if (k >= 3) {
            int Sc = S | (1 << v);
            int ord[24];
            ord[0] = v;
            orden(mask, v, Sc, ord, k, 1, comp);
        }
        if (S == 0) break;
    }
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]);
    for (int i = 0; i < 24; i++) { eu[i] = -1; ev[i] = -1; }
    gen((1 << n) - 1, 0);
    printf("n=%d : %lld 2-factores con s=5, %lld univocamente Hamiltonianos, %d clases\n",
           n, tot, tot_uh, nclases);
    return 0;
}
