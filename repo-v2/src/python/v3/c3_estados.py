"""For C3FAIL pairs: N[s1][s2], s_i in {S, U, W}: number of cycles of Gamma that
 S: contain the stretch edge u_i w_i;  U: contain u_i but not w_i;  W: contain w_i but not u_i,
and cover every other vertex.  Sum over states = Hamilton cycles of Gamma/S ignoring ports.
Prints one line per pair: n j good N(SS) N(SU) ... (9 numbers) and F-structure features."""
import sys, re
def E(a, b): return (min(a, b), max(a, b))
def cycles(n, adj, verts):
    verts = sorted(verts); s = verts[0]; out = []; path = [s]; seen = {s}; vs = set(verts); m = len(verts)
    def rec():
        v = path[-1]
        if len(path) == m:
            if s in adj[v] and path[1] < path[-1]: out.append(frozenset(E(path[i], path[(i + 1) % m]) for i in range(m)))
            return
        for w in adj[v]:
            if w in vs and w not in seen: seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)
    rec(); return out
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 99
for line in open(sys.argv[1]):
    if not line.startswith('C3FAIL'): continue
    n = int(re.search(r'n=(\d+)', line).group(1))
    if n > NMAX: continue
    F = {E(*map(int, t.split('-'))) for t in line.split('F=')[1].split()}
    H = {E(i, (i + 1) % n) for i in range(n)}; S = sorted(F & H); U = H - set(S)
    adj = {v: set() for v in range(n)}
    for a, b in F | H: adj[a].add(b); adj[b].add(a)
    j = S[1][0]
    N = {}
    for s1 in 'SUW':
        for s2 in 'SUW':
            drop = set()
            for st, (u, w) in zip((s1, s2), S):
                if st == 'U': drop.add(w)
                if st == 'W': drop.add(u)
            cs = cycles(n, adj, set(range(n)) - drop)
            for st, e in zip((s1, s2), S):
                if st == 'S': cs = [c for c in cs if e in c]
            N[s1 + s2] = len(cs)
    good = N['SS'] - 1
    print(n, j, good, ' '.join('%s=%d' % (k, N[k]) for k in sorted(N)))
