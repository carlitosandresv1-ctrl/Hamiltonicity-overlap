"""Random {1,1} pairs (any, not only C3FAIL).  For a block (stretch u-w) the state of a cycle is
 S: uses uw;  O: contains u and w but not uw;  U: contains u, not w;  W: contains w, not u.
N[s] (block 1 state s, block 2 state t fixed) = number of cycles covering all other vertices.
Find all GF(2) relations sum_s c_s N[s, t] = 0 valid for every pair and every t."""
import random, itertools, sys
def E(a, b): return (min(a, b), max(a, b))
def cycles(adj, verts):
    verts = sorted(verts); s = verts[0]; out = []; path = [s]; seen = {s}; vs = set(verts); m = len(verts)
    def rec():
        v = path[-1]
        if len(path) == m:
            if s in adj[v] and path[1] < path[-1]: out.append(frozenset(E(path[i], path[(i + 1) % m]) for i in range(m)))
            return
        for w in adj[v]:
            if w in vs and w not in seen: seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)
    rec(); return out
def rand_pair(n, rng):
    H = {E(i, (i + 1) % n) for i in range(n)}
    while True:
        j = rng.randint(2, n - 2)
        S = {(0, 1), (j, j + 1)}
        # random 2-factor containing S, avoiding other H edges: random perfect structure by retries
        need = {v: 2 for v in range(n)}; F = set(S)
        for a, b in S: need[a] -= 1; need[b] -= 1
        ok = True
        order = list(range(n)); rng.shuffle(order)
        stubs = [v for v in range(n) for _ in range(need[v])]
        rng.shuffle(stubs)
        Fx = {E(stubs[i], stubs[i + 1]) for i in range(0, len(stubs), 2)}
        if any(a == b for a, b in Fx) or len(Fx) * 2 != len(stubs) or Fx & H or Fx & F: continue
        F |= Fx
        return F, H, sorted(S)
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
rows = []
for trial in range(int(sys.argv[1])):
    n = rng.choice([8, 9, 10, 11])
    F, H, S = rand_pair(n, rng)
    adj = {v: set() for v in range(n)}
    for a, b in F | H: adj[a].add(b); adj[b].add(a)
    def count(s1, s2):
        drop = set(); need = []; forb = []
        for st, (u, w) in zip((s1, s2), S):
            if st == 'U': drop.add(w)
            if st == 'W': drop.add(u)
            if st == 'S': need.append(E(u, w))
            if st == 'O': forb.append(E(u, w))
        cs = cycles(adj, set(range(n)) - drop)
        return sum(1 for c in cs if all(e in c for e in need) and not any(e in c for e in forb))
    N = {(a, b): count(a, b) for a in 'SOUW' for b in 'SOUW'}
    rows.append([N[(a, b)] % 2 for a in 'SOUW' for b in 'SOUW'])
labels = [a + b for a in 'SOUW' for b in 'SOUW']
# nullspace over GF(2) of the rows (relations c with rows . c = 0)
import copy
M = [r[:] for r in rows]; piv = []; r = 0
for col in range(16):
    p = next((i for i in range(r, len(M)) if M[i][col]), None)
    if p is None: continue
    M[r], M[p] = M[p], M[r]
    for i in range(len(M)):
        if i != r and M[i][col]: M[i] = [(x + y) % 2 for x, y in zip(M[i], M[r])]
    piv.append(col); r += 1
free = [c for c in range(16) if c not in piv]
print('pairs', len(rows), 'rank', r, 'nullity', len(free))
for f in free:
    v = [0] * 16; v[f] = 1
    for i, pc in enumerate(piv): v[pc] = M[i][f]
    print('relation: ' + ' + '.join(labels[k] for k in range(16) if v[k]) + ' = 0 (mod 2)')
