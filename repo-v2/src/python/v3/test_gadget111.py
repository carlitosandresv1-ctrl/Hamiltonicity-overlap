"""Check of the {1,1,1} gadgets with two Hamilton paths found by src/c/v3/gadget11.c.

(a) For each gadget, enumerate from scratch all Hamilton paths 0 -> m-1 of F_W u P_W and
    check that there are exactly two and both have overlap |F_W n Q| = 3 = s_W, with
    F_W n P_W three pairwise disjoint single edges.
(b) Lemma 8.2 end to end, as in src/python/v2/test_gadget.py: insert the gadget into the
    H-edge xy = (0,1) of random 4-regular Hamiltonian graphs G = F0 u H and check, with the
    independent counter hc, that
        #HC(G') = 2 * #HC(G through xy)   and   ov_{G'}(F') = 3 + max_{C through xy} |F0 n C|,
    and that F' n H' has pattern {1,1,1}.  If G were uniquely Hamiltonian the right-hand
    side would be 3 = |F' n H'|, i.e. (F', H') would be a rigid pair with pattern {1,1,1}.

usage: python3 test_gadget111.py path/to/hc
"""
import random
import subprocess
import sys

HC = sys.argv[1]
GADGETS = [  # (m, F_W) from results/v3/gadgets111.txt: the two of size m = 7 (the smallest) and three of size 9
    (7, "0-1 0-6 1-6 2-3 2-4 3-5 4-5"),
    (7, "0-5 0-6 1-2 1-3 2-4 3-4 5-6"),
    (9, "0-5 0-7 1-2 1-3 2-4 3-4 5-8 6-7 6-8"),
    (9, "0-6 0-8 1-2 1-3 2-4 3-4 5-7 5-8 6-7"),
    (9, "0-2 0-3 1-2 1-8 3-8 4-5 4-6 5-7 6-7"),
]


def E(a, b):
    return (min(a, b), max(a, b))


def parse(fs):
    return {E(*map(int, t.split("-"))) for t in fs.split()}


def ham_paths(m, edges):
    adj = {v: set() for v in range(m)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    out, path, seen = [], [0], {0}

    def rec():
        v = path[-1]
        if len(path) == m:
            if v == m - 1:
                out.append({E(path[i], path[i + 1]) for i in range(m - 1)})
            return
        for w in adj[v]:
            if w not in seen and (w != m - 1 or len(path) == m - 1):
                seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)

    rec()
    return out


def stretches(S):
    """sizes of the components (paths) formed by the edge set S"""
    adj = {}
    for a, b in S:
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    seen, sizes = set(), []
    for v in adj:
        if v in seen:
            continue
        comp, stack = set(), [v]
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x); stack.extend(adj[x] - comp)
        seen |= comp
        sizes.append(len(comp) - 1)
    return sorted(sizes)


def count(n, edges, F=()):
    inp = f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges) + f"{len(F)}\n" + "".join(f"{a} {b}\n" for a, b in F)
    c, ov = subprocess.run([HC], input=inp, capture_output=True, text=True).stdout.split()
    return int(c), int(ov)


def random_F0(n, rng):  # same generator as src/python/v2/test_gadget.py
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


bad = 0
for m, fs in GADGETS:
    FW = parse(fs)
    P = {E(i, i + 1) for i in range(m - 1)}
    deg = [0] * m
    for a, b in FW:
        deg[a] += 1; deg[b] += 1
    paths = ham_paths(m, FW | P)
    ovs = sorted(len(FW & Q) for Q in paths)
    pat = stretches(FW & P)
    ok = all(d == 2 for d in deg) and len(paths) == 2 and ovs == [3, 3] and pat == [1, 1, 1]
    print(f"(a) m={m} F_W={fs}: 2-factor={all(d == 2 for d in deg)} paths={len(paths)} overlaps={ovs} pattern={pat} {'OK' if ok else 'FAIL'}")
    bad += not ok

rng = random.Random(1)
tests = 0
for trial in range(60):
    n = rng.choice([9, 10, 11, 12])
    F0, H = random_F0(n, rng)
    G = F0 | H
    x, y = 0, 1
    sub = (G - {E(x, y)}) | {E(x, n), E(y, n)}          # HCs through xy = HCs of the subdivision
    through, ov_through = count(n + 1, sorted(sub), sorted(F0))
    for m, fs in GADGETS:
        W = {i: n + i for i in range(m)}
        FW = {E(W[a], W[b]) for a, b in parse(fs)}
        P = {E(W[i], W[i + 1]) for i in range(m - 1)}
        Hn = (H - {E(x, y)}) | P | {E(x, W[0]), E(W[m - 1], y)}
        Fn = F0 | FW
        N = n + m
        hc_count, ov = count(N, sorted(Fn | Hn), sorted(Fn))
        tests += 1
        ok = hc_count == 2 * through and ov == 3 + ov_through and stretches(Fn & Hn) == [1, 1, 1]
        if not ok:
            bad += 1
            print("MISMATCH", n, fs, hc_count, through, ov, ov_through, stretches(Fn & Hn))
print(f"(b) {tests} insertions tested")
print("all checks passed" if bad == 0 else f"FAILURES: {bad}")
