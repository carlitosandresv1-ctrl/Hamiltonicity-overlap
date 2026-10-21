/* Count Hamilton cycles of a graph read from stdin: "n m" then m lines "a b".
 * Also reports max |F n H'| when a second edge set F is given after: "k" then k lines.
 * DFS from vertex 0 with a degree-feasibility prune; each cycle counted once. */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
static int n; static u64 adj[64], Fadj[64];
static int path[64]; static long long cnt; static int maxov; static long long cap = 1000000;
static int feasible(u64 vis, int cur) {
    for (int v = 0; v < n; v++) if (!((vis >> v) & 1)) {
        u64 avail = adj[v] & (~vis | (1ULL << cur) | 1ULL);
        if (__builtin_popcountll(avail) < 2) return 0;
    }
    return 1;
}
static void dfs(int d, u64 vis, int ov) {
    if (cnt >= cap) return;
    int v = path[d - 1];
    if (d == n) {
        if (!(adj[v] & 1ULL) || path[1] > path[n - 1]) return;
        cnt++; int o = ov + (int)((Fadj[v]) & 1ULL); if (o > maxov) maxov = o; return;
    }
    if (!feasible(vis, v)) return;
    u64 c = adj[v] & ~vis;
    while (c) { int w = __builtin_ctzll(c); c &= c - 1; path[d] = w;
        dfs(d + 1, vis | (1ULL << w), ov + (int)((Fadj[v] >> w) & 1ULL)); }
}
int main(void) {
    int m, a, b, k;
    if (scanf("%d %d", &n, &m) != 2) return 1;
    for (int i = 0; i < m; i++) { if (scanf("%d %d", &a, &b) != 2) return 1; adj[a] |= 1ULL << b; adj[b] |= 1ULL << a; }
    if (scanf("%d", &k) == 1) for (int i = 0; i < k; i++) { if (scanf("%d %d", &a, &b) != 2) return 1; Fadj[a] |= 1ULL << b; Fadj[b] |= 1ULL << a; }
    path[0] = 0; maxov = -1; dfs(1, 1ULL, 0);
    printf("%lld %d\n", cnt, maxov);
    return 0;
}
