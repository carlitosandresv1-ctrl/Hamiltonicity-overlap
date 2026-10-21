/* Clasifica los pares extremales: cuenta los pares con solapamiento maximo
 * igual a OBJ, cuantos son univocamente Hamiltonianos, y en cuantas clases
 * se reparten estos ultimos bajo el grupo diedral que preserva H.
 *
 * uso: ./clases n obj
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n, obj;
static int eu[16], ev[16];
static int adj[16][5], gr[16];
static int esF[16][16];
static long long tot_ext = 0, tot_uh = 0;

/* --- clases: claves canonicas de 128 bits --- */
#define MAXCL 4096
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

/* --- enumeracion de todos los ciclos Hamiltonianos de Gamma --- */
static int vis[16], prof, mejor_sol, nham;

static void dfs(int v, int sol)
{
    if (prof == n) {
        for (int t = 0; t < gr[v]; t++)
            if (adj[v][t] == 0) {
                int s2 = sol + esF[v][0];
                if (s2 > mejor_sol) mejor_sol = s2;
                nham++;
                return;
            }
        return;
    }
    for (int t = 0; t < gr[v]; t++) {
        int w = adj[v][t];
        if (vis[w]) continue;
        /* evita contar cada ciclo en los dos sentidos: exige cam[1] < cam[n-1] */
        vis[w] = 1; prof++;
        dfs(w, sol + esF[v][w]);
        prof--; vis[w] = 0;
    }
}

static void evalua(void)
{
    for (int v = 0; v < n; v++) { gr[v] = 0; for (int w = 0; w < n; w++) esF[v][w] = 0; }
    for (int i = 0; i < n; i++) esF[eu[i]][ev[i]] = esF[ev[i]][eu[i]] = 1;
    static int ya[16][16];
    for (int v = 0; v < n; v++) for (int w = 0; w < n; w++) ya[v][w] = 0;
    for (int i = 0; i < n; i++) {
        int a = eu[i], b = ev[i];
        if (!ya[a][b]) { ya[a][b] = ya[b][a] = 1; adj[a][gr[a]++] = b; adj[b][gr[b]++] = a; }
    }
    for (int i = 0; i < n; i++) {
        int a = i, b = (i + 1) % n;
        if (!ya[a][b]) { ya[a][b] = ya[b][a] = 1; adj[a][gr[a]++] = b; adj[b][gr[b]++] = a; }
    }
    mejor_sol = -1; nham = 0;
    for (int v = 0; v < n; v++) vis[v] = 0;
    vis[0] = 1; prof = 1;
    dfs(0, 0);
    nham /= 2;                       /* cada ciclo se recorre en dos sentidos */
    if (mejor_sol != obj) return;
    tot_ext++;
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

/* --- generacion de 2-factores --- */
static void gen(int mask);

static void orden(int mask, int v, int S, int *ord, int k, int pos)
{
    if (pos == k) {
        if (k > 2 && ord[1] > ord[k - 1]) return;
        int pos0 = 0;
        while (pos0 < n && eu[pos0] >= 0) pos0++;
        for (int i = 0; i < k; i++) {
            int a = ord[i], b = ord[(i + 1) % k];
            eu[pos0 + i] = a < b ? a : b;
            ev[pos0 + i] = a < b ? b : a;
        }
        gen(mask & ~S);
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
            int ord[16];
            ord[0] = v;
            orden(mask, v, Sc, ord, k, 1);
        }
        if (S == 0) break;
    }
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]);
    obj = atoi(argv[2]);
    for (int i = 0; i < 16; i++) { eu[i] = -1; ev[i] = -1; }
    gen((1 << n) - 1);
    printf("n=%d  solapamiento objetivo %d : %lld pares extremales, %lld univocamente Hamiltonianos, %d clases\n",
           n, obj, tot_ext, tot_uh, nclases);
    return 0;
}
