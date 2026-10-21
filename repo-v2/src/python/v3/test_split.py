"""Vertex splitting: claim C1 for pattern {1,1} is at least as hard as Sheehan's conjecture.

Let G = F0 u H0 be 4-regular with F0 n H0 = empty.  Split two vertices z1, z2: z gets
replaced by an edge u-w, u inherits one H0-edge and one F0-edge of z, w the other two.
Then (F, H) is a pair with pattern {1,1} (S = {u1w1, u2w2}), and the Hamilton cycles of
Gamma = F u H that contain S are in bijection with the Hamilton cycles of G that are
compatible at z1 and z2 (they leave z through one edge of u and one edge of w).
So if G were uniquely Hamiltonian, H would be the only Hamilton cycle of Gamma through S,
and claim C1 ("some good cycle keeps both shared edges") would fail.

This script checks the bijection on random 4-regular Hamiltonian graphs by brute force.
usage: python3 test_split.py
"""
import random


def E(a, b):
    return (min(a, b), max(a, b))


def ham_cycles(n, edges):
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    res, path, seen = [], [0], {0}

    def rec():
        v = path[-1]
        if len(path) == n:
            if 0 in adj[v] and path[1] < path[-1]:
                res.append(frozenset(E(path[i], path[(i + 1) % n]) for i in range(n)))
            return
        for w in adj[v]:
            if w not in seen:
                seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)

    rec()
    return res


def random_F0(n, rng):
    H = {E(i, (i + 1) % n) for i in range(n)}
    while True:
        p = list(range(n)); rng.shuffle(p)
        cuts, i = [], 0
        while i < n:
            L = rng.randint(3, max(3, n - i)) if n - i >= 6 else n - i
            cuts.append(p[i:i + L]); i += L
        if any(len(c) < 3 for c in cuts):
            continue
        F = {E(c[j], c[(j + 1) % len(c)]) for c in cuts for j in range(len(c))}
        if len(F) == n and not (F & H):
            return F, H


rng = random.Random(7)
bad = tests = 0
for trial in range(150):
    n = rng.choice([7, 8, 9, 10])
    F0, H0 = random_F0(n, rng)
    z1, z2 = rng.sample(range(n), 2)
    # split z -> (u, w): u keeps the H0-edge to z-1 and one F0-edge, w gets z+1 and the other
    F, H = set(F0), set(H0)
    new = n
    trans = {}
    for z in (z1, z2):
        u, w = z, new; new += 1
        fz = sorted(b if a == z else a for a, b in F0 if z in (a, b))
        hz = [(z - 1) % n, (z + 1) % n]
        f_u, f_w = rng.sample(fz, 2)
        h_u, h_w = hz
        for X in (F, H):
            for e in list(X):
                if z in e:
                    X.discard(e)
        H |= {E(u, h_u), E(w, h_w), E(u, w)}
        F |= {E(u, f_u), E(w, f_w), E(u, w)}
        trans[z] = ({h_u, f_u}, {h_w, f_w})
    # u keeps the label z, so an edge z1-z2 of G would be attached to the wrong side when
    # z2 is split after z1: skip adjacent z1, z2 (non-adjacent pairs are plentiful).
    if E(z1, z2) in F0 | H0:
        continue
    N = n + 2
    deg = [0] * N
    for a, b in F:
        deg[a] += 1; deg[b] += 1
    assert all(d == 2 for d in deg) and len(F & H) == 2 and len(H) == N
    S = F & H
    through_S = [C for C in ham_cycles(N, F | H) if S <= C]
    compat = 0
    for C in ham_cycles(n, F0 | H0):
        ok = True
        for z in (z1, z2):
            nb = {a if b == z else b for a, b in C if z in (a, b)}
            su, sw = trans[z]
            ok &= len(nb & su) == 1 and len(nb & sw) == 1
        compat += ok
    tests += 1
    if len(through_S) != compat:
        bad += 1
        print("MISMATCH", n, z1, z2, len(through_S), compat)
print(f"{tests} splittings tested, mismatches: {bad}")
