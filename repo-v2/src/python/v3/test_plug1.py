"""Checks for plug1.c and for the gluing of two one-stretch sides.

(1) Independent enumeration of the one-stretch sides X of size m (Hamilton path P = 0..m-1,
    2-factor F_X with F_X n P = {j(j+1)}, j <= (m-2)/2) and of hp(X) = number of Hamilton
    paths 0 -> m-1 of P u F_X; prints the histogram to compare with `plug1 m`.
(2) Gluing: for random sides X (stretch j) and Y (stretch k), Gamma = X u Y + the H-edges
    (m_X-1, m_X) and (m_X+m_Y-1, 0) is a {1,1} pair whose 2-edge cut separates the stretches;
    check that F is a 2-factor with F n H = S of two unit stretches, and that
    #HC(Gamma) = hp(X) * hp(Y).
usage: python3 test_plug1.py
"""
import random
from collections import Counter


def sides(m):
    out = []
    for j in range((m - 2) // 2 + 1):
        need = [2] * m
        F = {(j, j + 1)}
        need[j] -= 1; need[j + 1] -= 1

        def gen(v, lo):
            while v < m and need[v] == 0:
                v += 1; lo = 0
            if v == m:
                out.append((j, frozenset(F))); return
            for w in range(max(v + 1, lo), m):
                if need[w] and abs(v - w) != 1 and (v, w) not in F:
                    F.add((v, w)); need[v] -= 1; need[w] -= 1
                    gen(v, w + 1)
                    F.discard((v, w)); need[v] += 1; need[w] += 1
        gen(0, 0)
        assert len(set(out)) == len(out)
    return out


def adjacency(n, edges):
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    return adj


def hp(n, edges, s, t):
    adj = adjacency(n, edges); cnt = 0; seen = {s}

    def rec(v, d):
        nonlocal cnt
        if d == n:
            cnt += v == t; return
        for w in adj[v]:
            if w not in seen and (w != t or d == n - 1):
                seen.add(w); rec(w, d + 1); seen.discard(w)
    rec(s, 1)
    return cnt


def hc(n, edges):
    adj = adjacency(n, edges); cnt = 0; seen = {0}

    def rec(v, d):
        nonlocal cnt
        if d == n:
            cnt += 0 in adj[v]; return
        for w in adj[v]:
            if w not in seen:
                seen.add(w); rec(w, d + 1); seen.discard(w)
    rec(0, 1)
    return cnt // 2


def side_edges(m, F):
    return set(F) | {(i, i + 1) for i in range(m - 1)}


def sides_brute(m):
    """the same sides by brute force over all sets of m-1 chords (no recursive generator)"""
    from itertools import combinations
    chords = [(a, b) for a in range(m) for b in range(a + 2, m)]
    out = set()
    for C in combinations(chords, m - 1):
        deg = Counter(v for e in C for v in e)
        for j in range((m - 2) // 2 + 1):
            d = deg.copy(); d[j] += 1; d[j + 1] += 1
            if all(d[v] == 2 for v in range(m)):
                out.add((j, frozenset(C) | {(j, j + 1)}))
    return out


# (1) histograms
for m in (6, 7, 8):
    S1 = sides(m)
    assert set(S1) == sides_brute(m), m
    h = Counter(min(hp(m, side_edges(m, F), 0, m - 1), 8) for j, F in S1)
    print('m=%d sides=%d (= brute force)' % (m, sum(h.values())),' '.join('hp%s%d:%d' % ('>=' if k == 8 else '=', k, c) for k, c in sorted(h.items())))

# (2) gluing
rng = random.Random(5)
pool = {m: sides(m) for m in (4, 5, 6, 7)}
bad = 0; tests = 0
for t in range(300):
    mx, my = rng.choice([4, 5, 6, 7]), rng.choice([4, 5, 6, 7])
    jx, FX = rng.choice(pool[mx]); jy, FY = rng.choice(pool[my])
    if rng.random() < 0.5:     # use the reflected side too
        FX = frozenset((mx - 1 - b, mx - 1 - a) for a, b in FX); jx = mx - 2 - jx
    n = mx + my
    F = set(FX) | {(a + mx, b + mx) for a, b in FY}
    H = {(i, i + 1) for i in range(n - 1)} | {(0, n - 1)}
    deg = Counter(v for e in F for v in e)
    S = F & H
    ok_pair = all(deg[v] == 2 for v in range(n)) and S == {(jx, jx + 1), (jy + mx, jy + mx + 1)}
    g = hc(n, F | H)
    expect = hp(mx, side_edges(mx, FX), 0, mx - 1) * hp(my, side_edges(my, FY), 0, my - 1)
    tests += 1
    if not (ok_pair and g == expect):
        bad += 1; print('MISMATCH', mx, my, ok_pair, g, expect)
print('gluing: %d pairs tested, %s' % (tests, 'all checks passed' if bad == 0 else '%d FAILURES' % bad))
