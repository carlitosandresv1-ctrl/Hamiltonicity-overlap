"""Two-edge-cut decomposition of the {1,1} pairs with few good cycles.

Every Hamilton cycle of Gamma = F u H crosses a 2-edge cut {e, f} through both edges, so it
traverses the side B of the cut by a Hamilton path of B between its two port vertices.
Replacing each inclusion-minimal side B_i by a single edge between its outside neighbours
gives a quotient multigraph Q, and

    #HC(Gamma) = prod_i hp(B_i) * #HC(Q through every new edge).

For each DET line of `M=2 DETAIL=T near111` this script computes the minimal sides, their
sizes, hp(B_i), whether B_i contains a stretch, the quotient count, and checks the identity
against a direct count of #HC(Gamma).  It also checks #HC(Gamma) = good + 1 (H* absent).
usage: python3 bloques11.py det_files...
"""
import re
import sys
from collections import Counter
from itertools import combinations


def E(a, b):
    return (min(a, b), max(a, b))


def connected_without(n, edges, drop):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        if i not in drop:
            adj[a].append(b); adj[b].append(a)
    seen, st = {0}, [0]
    while st:
        for w in adj[st.pop()]:
            if w not in seen:
                seen.add(w); st.append(w)
    return seen


def hc_count(nv, edges, required=()):
    """Hamilton cycles of a multigraph given as an edge list (vertices 0..nv-1), counted as
    edge-index sets, that contain every edge index in `required`."""
    if nv == 1:
        return 0
    if nv == 2:   # a 2-cycle made of two parallel edges
        idx = [i for i, (a, b) in enumerate(edges) if a != b]
        return sum(1 for c in combinations(idx, 2) if set(required) <= set(c))
    inc = [[] for _ in range(nv)]
    for i, (a, b) in enumerate(edges):
        if a != b:
            inc[a].append((b, i)); inc[b].append((a, i))
    req = set(required)
    cnt = 0
    used = []
    seen = [False] * nv
    seen[0] = True

    def rec(v, d):
        nonlocal cnt
        if d == nv:
            for w, i in inc[v]:
                if w == 0 and i != used[0]:
                    cyc = set(used) | {i}
                    if req <= cyc:
                        cnt += 1
            return
        for w, i in inc[v]:
            if not seen[w]:
                seen[w] = True; used.append(i); rec(w, d + 1); used.pop(); seen[w] = False

    rec(0, 1)
    return cnt // 2      # each cycle is found in both directions


def hp_count(vs, edges, x, y):
    vs = sorted(vs); idx = {v: k for k, v in enumerate(vs)}
    adj = {k: [] for k in range(len(vs))}
    for a, b in edges:
        if a in idx and b in idx:
            adj[idx[a]].append(idx[b]); adj[idx[b]].append(idx[a])
    m, s, t = len(vs), idx[x], idx[y]
    if m == 1:
        return 1
    cnt = 0; seen = {s}

    def rec(v, d):
        nonlocal cnt
        if d == m:
            cnt += v == t; return
        for w in adj[v]:
            if w not in seen and (w != t or d == m - 1):
                seen.add(w); rec(w, d + 1); seen.discard(w)

    rec(s, 1)
    return cnt


def analyse(n, F, good):
    H = {E(i, (i + 1) % n) for i in range(n)}
    S = F & H
    edges = sorted(F | H)          # simple graph Gamma
    sides = []
    for i, j in combinations(range(len(edges)), 2):
        comp = connected_without(n, edges, {i, j})
        if len(comp) < n:
            side = frozenset(range(n)) - comp if len(comp) > n / 2 else frozenset(comp)
            sides.append((side, i, j))
    minimal = [s for s in sides if not any(t[0] < s[0] for t in sides)]
    # contract each minimal side to one edge
    blocks = []
    for side, i, j in minimal:
        (a1, b1), (a2, b2) = edges[i], edges[j]
        x = a1 if a1 in side else b1; xo = b1 if a1 in side else a1
        y = a2 if a2 in side else b2; yo = b2 if a2 in side else a2
        hp = hp_count(side, edges, x, y)
        blocks.append((side, xo, yo, hp, len(side & {v for e in S for v in e}) // 2))
    inside = set().union(*[b[0] for b in blocks]) if blocks else set()
    if any(len(a[0] & b[0]) for a, b in combinations(blocks, 2)):
        return None
    outside = [v for v in range(n) if v not in inside]
    relab = {v: k for k, v in enumerate(outside)}
    qedges = [(relab[a], relab[b]) for a, b in edges if a in relab and b in relab]
    req = []
    for side, xo, yo, hp, ns in blocks:
        req.append(len(qedges)); qedges.append((relab[xo], relab[yo]))
    q = hc_count(len(outside), qedges, req) if outside else 1
    prod = 1
    for b in blocks:
        prod *= b[3]
    total = hc_count(n, edges)
    return dict(total=total, prod=prod, q=q, qn=len(outside),
                blocks=sorted((len(b[0]), b[3], b[4]) for b in blocks))


stat = Counter(); bad = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith('DET'):
            continue
        n = int(re.search(r'n=(\d+)', line).group(1))
        g = int(re.search(r'good=(\d+)', line).group(1))
        F = {E(*map(int, t.split('-'))) for t in line.split('F=')[1].split()}
        r = analyse(n, F, g)
        if r is None:
            print('OVERLAP', n, g); bad += 1; continue
        ok = r['total'] == r['prod'] * r['q'] and r['total'] == g + 1
        bad += not ok
        desc = ' '.join('%d:hp%d%s' % (m, h, 'S' * s) for m, h, s in r['blocks'])
        stat[(n, g, desc, r['qn'], r['q'])] += 1
        if not ok:
            print('MISMATCH', n, g, r, line.split('F=')[1].strip())
for (n, g, desc, qn, q), c in sorted(stat.items()):
    print('n=%d g=%d pairs=%d blocks[size:hp,S=stretch inside]= %s | quotient %d vertices, %d cycles'
          % (n, g, c, desc or '-', qn, q))
print('identity #HC = prod hp * quotient = good + 1:', 'all OK' if bad == 0 else '%d FAIL' % bad)
