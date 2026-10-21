/* Busqueda dirigida por PATRON de tramos.
 *
 * Un par (F,H) univocamente Hamiltoniano con s = |F cap H| = 5 tiene
 * S = F cap H descompuesto en c caminos ("tramos") de tamanos k_1..k_c con
 * suma 5, y entonces  n_2 = 5 - c,  n_3 = 2c.  Los siete patrones posibles son
 *
 *    {5}  {1,4} {2,3}  {1,1,3} {1,2,2}  {1,1,1,2}  {1,1,1,1,1}
 *
 * y la conjetura es que solo {1,2,2} admite pares univocamente Hamiltonianos.
 * Este programa fija el patron, coloca los tramos sobre H de todas las formas
 * posibles (modulo rotacion), completa F con cuerdas de todas las maneras, y
 * comprueba unicidad hamiltoniana.  Es muchisimo mas barato que recorrer todos
 * los 2-factores porque S queda fijado de antemano.
 *
 * uso: ./patronp n idx k1 k2 ...   (idx = -1 todos, -2 solo contar colocaciones)
 *      ./patron n k1 k2 ...  -> un patron concreto
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NMAX 24

static int n;
static int gradoF[NMAX];
static int Fu[NMAX], Fv[NMAX], nF;      /* aristas de F */
static int esH[NMAX][NMAX];             /* arista del ciclo canonico */
static int enF[NMAX][NMAX];
static long long completos = 0, uh = 0;
static int nclases = 0;
#define MAXCL 20000
static unsigned __int128 clave[MAXCL];

static int idx(int u, int v)
{
    int a = u < v ? u : v, b = u < v ? v : u;
    return a * n - a * (a + 1) / 2 + (b - a - 1);
}

static unsigned __int128 canon(void)
{
    unsigned __int128 mejor = 0; int primero = 1;
    for (int sh = 0; sh < n; sh++)
        for (int d = -1; d <= 1; d += 2) {
            unsigned __int128 m = 0;
            for (int i = 0; i < nF; i++) {
                int a = ((Fu[i] * d + sh) % n + n) % n;
                int b = ((Fv[i] * d + sh) % n + n) % n;
                m |= ((unsigned __int128)1) << idx(a, b);
            }
            if (primero || m < mejor) { mejor = m; primero = 0; }
        }
    return mejor;
}

/* ---- unicidad hamiltoniana de Gamma = F u H ---- */
static int adj[NMAX][5], gr[NMAX], vis[NMAX], cam[NMAX], prof, nham;

static int dfs(int v)
{
    if (prof == n) {
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
    completos++;
    for (int v = 0; v < n; v++) gr[v] = 0;
    static int ya[NMAX][NMAX];
    for (int v = 0; v < n; v++) for (int w = 0; w < n; w++) ya[v][w] = 0;
    for (int i = 0; i < nF; i++) {
        int a = Fu[i], b = Fv[i];
        ya[a][b] = ya[b][a] = 1; adj[a][gr[a]++] = b; adj[b][gr[b]++] = a;
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
    uh++;
    unsigned __int128 k = canon();
    for (int i = 0; i < nclases; i++) if (clave[i] == k) return;
    if (nclases < MAXCL) {
        clave[nclases++] = k;
        printf("    UH! F =");
        for (int i = 0; i < nF; i++) printf(" (%d,%d)", Fu[i], Fv[i]);
        printf("\n"); fflush(stdout);
    }
}

/* ---- completar F con cuerdas ---- */
static void completa(int desde)
{
    int v = -1;
    for (int i = 0; i < n; i++) if (gradoF[i] < 2) { v = i; break; }
    if (v < 0) { evalua(); return; }
    for (int w = desde; w < n; w++) {
        if (w == v) continue;
        if (gradoF[w] >= 2) continue;
        if (esH[v][w]) continue;            /* solo cuerdas */
        if (enF[v][w]) continue;
        enF[v][w] = enF[w][v] = 1;
        gradoF[v]++; gradoF[w]++;
        Fu[nF] = v < w ? v : w; Fv[nF] = v < w ? w : v; nF++;
        /* si v sigue deficiente seguimos con v y w creciente; si no, reinicio */
        completa(gradoF[v] < 2 ? w + 1 : 0);
        nF--;
        gradoF[v]--; gradoF[w]--;
        enF[v][w] = enF[w][v] = 0;
    }
}

/* ---- colocacion de los tramos sobre H ---- */
static int k[8], c;
static long placas = 0, objetivo = -1;   /* troceado: ejecutar solo una colocacion */

static void coloca(void)
{
    /* huecos g_1..g_c >= 1 con sum k + sum g = n ; primer tramo empieza en 0 */
    int libre = n - 5;
    if (libre < c) return;
    int g[8];
    /* composiciones de 'libre' en c partes >= 1 */
    int tope = libre - c;
    int idxs[8];
    for (int i = 0; i < c; i++) idxs[i] = 0;
    /* enumeracion simple por recursion manual sobre c <= 5 */
    int pila[8], nivel = 0;
    (void)tope; (void)idxs; (void)pila; (void)nivel;
    /* recursion explicita */
    void rec(int i, int resto) {
        if (i == c - 1) {
            g[i] = resto;
            if (g[i] < 1) return;
            long mia = placas++;
            if (objetivo >= 0 && mia != objetivo) return;
            if (objetivo == -2) return;
            /* construir S */
            memset(gradoF, 0, sizeof gradoF);
            memset(enF, 0, sizeof enF);
            nF = 0;
            int pos = 0;
            for (int j = 0; j < c; j++) {
                for (int t = 0; t < k[j]; t++) {
                    int a = pos % n, b = (pos + 1) % n;
                    int x = a < b ? a : b, y = a < b ? b : a;
                    Fu[nF] = x; Fv[nF] = y; nF++;
                    enF[a][b] = enF[b][a] = 1;
                    gradoF[a]++; gradoF[b]++;
                    pos++;
                }
                pos += g[j];
            }
            int ok = 1;
            for (int v = 0; v < n; v++) if (gradoF[v] > 2) ok = 0;
            if (ok) completa(0);
            return;
        }
        for (int x = 1; x <= resto - (c - 1 - i); x++) { g[i] = x; rec(i + 1, resto - x); }
    }
    rec(0, libre);
}

static void permuta(int *a, int m, int prof2)
{
    if (prof2 == m) { coloca(); return; }
    for (int i = prof2; i < m; i++) {
        int t = a[prof2]; a[prof2] = a[i]; a[i] = t;
        int rep = 0;
        for (int j = prof2; j < i; j++) if (a[j] == a[prof2]) rep = 1;
        if (!rep) permuta(a, m, prof2 + 1);
        t = a[prof2]; a[prof2] = a[i]; a[i] = t;
    }
}

static void prueba(int *ks, int cc)
{
    c = cc;
    for (int i = 0; i < cc; i++) k[i] = ks[i];
    completos = 0; uh = 0; nclases = 0;
    printf("  patron {");
    for (int i = 0; i < cc; i++) printf("%d%s", ks[i], i + 1 < cc ? "," : "");
    printf("} :  n_2=%d n_3=%d  ... ", 5 - cc, 2 * cc); fflush(stdout);
    int tmp[8];
    for (int i = 0; i < cc; i++) tmp[i] = ks[i];
    permuta(tmp, cc, 0);
    printf("placa %ld : %lld 2-factores, %lld UH, %d clases\n", objetivo, completos, uh, nclases);
    fflush(stdout);
}

int main(int argc, char **argv)
{
    n = atoi(argv[1]);
    objetivo = atol(argv[2]);
    for (int u = 0; u < n; u++) for (int v = 0; v < n; v++) esH[u][v] = 0;
    for (int i = 0; i < n; i++) { int a = i, b = (i + 1) % n; esH[a][b] = esH[b][a] = 1; }

    {
        int ks[8], cc = argc - 3;
        for (int i = 0; i < cc; i++) ks[i] = atoi(argv[3 + i]);
        placas = 0;
        if (objetivo == -2) {
            c = cc; for (int i = 0; i < cc; i++) k[i] = ks[i];
            int tmp[8]; for (int i = 0; i < cc; i++) tmp[i] = ks[i];
            permuta(tmp, cc, 0);
            printf("colocaciones = %ld\n", placas);
            return 0;
        }
        prueba(ks, cc);
        return 0;
    }
    int pats[7][6] = {
        {1, 5, 0, 0, 0, 0},
        {2, 1, 4, 0, 0, 0},
        {2, 2, 3, 0, 0, 0},
        {3, 1, 1, 3, 0, 0},
        {3, 1, 2, 2, 0, 0},
        {4, 1, 1, 1, 2, 0},
        {5, 1, 1, 1, 1, 1}
    };
    printf("n=%d\n", n);
    for (int p = 0; p < 7; p++) prueba(pats[p] + 1, pats[p][0]);
    return 0;
}
