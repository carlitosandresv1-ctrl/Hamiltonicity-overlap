"""Two-edge cuts: a port block (Def. 7.x) yields a plug (Def. 8.4), hence via doubling
(Lemma 8.5) a simple 4-regular uniquely Hamiltonian graph.

Let B have exactly two vertices x, y of degree 2, all others of degree 4.
  (i)  xy not in E(B):  Q = B + xy has x, y of degree 3, and the Hamilton paths x -> y of Q
       are those of B (a Hamilton path from x to y cannot use the edge xy when m >= 3).
  (ii) xy in E(B): let a, b be the other neighbours of x, y.  Every Hamilton path x -> y of B
       is x a ... b y, so Q = B - {x, y} has a, b of degree 3 and hp(Q; a, b) = hp(B; x, y).
In both cases #HC(D(Q)) = hp(B; x, y)^2 by Lemma 8.5, so a port block (hp = 1) gives a
counterexample to Sheehan's conjecture.  Also: Q minus its Hamilton path is a 2-factor
disjoint from it, so a plug is the same thing as a rigid gadget with s_W = 0.

This script checks the identities on random graphs B with that degree sequence (no port
blocks exist for m <= 13, so hp >= 2 here), counting Hamilton cycles of D(Q) with the
independent counter hc.
usage: python3 test_cut2.py path/to/hc
"""
import random
import subprocess
import sys

HC = sys.argv[1]


def E(a, b):
    return (min(a, b), max(a, b))


def random_B(m, rng):
    """simple connected graph, degrees 2, 2, 4, ..., 4 (x = 0, y = 1), configuration model"""
    while True:
        stubs = [0, 0, 1, 1] + [v for v in range(2, m) for _ in range(4)]
        rng.shuffle(stubs)
        edges = {E(stubs[i], stubs[i + 1]) for i in range(0, len(stubs), 2)}
        if len(edges) * 2 != len(stubs) or any(a == b for a, b in edges):
            continue
        adj = adjacency(m, edges)
        seen, st = {0}, [0]
        while st:
            for w in adj[st.pop()]:
                if w not in seen:
                    seen.add(w); st.append(w)
        if len(seen) == m:
            return edges


def adjacency(n, edges):
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    return adj


def hp(n, edges, s, t):
    """number of Hamilton paths from s to t"""
    adj = adjacency(n, edges)
    cnt = 0
    path, seen = [s], {s}

    def rec():
        nonlocal cnt
        v = path[-1]
        if len(path) == n:
            cnt += v == t
            return
        for w in adj[v]:
            if w not in seen and (w != t or len(path) == n - 1):
                seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)

    rec()
    return cnt


def relabel(edges, keep):
    idx = {v: i for i, v in enumerate(keep)}
    return {E(idx[a], idx[b]) for a, b in edges if a in idx and b in idx}, idx


def hc_count(n, edges):
    inp = f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in sorted(edges)) + "0\n"
    return int(subprocess.run([HC], input=inp, capture_output=True, text=True).stdout.split()[0])


rng = random.Random(3)
bad = tests = 0
cases = {1: 0, 2: 0}
hist = {}
for trial in range(400):
    m = rng.choice([7, 8, 9, 10])
    B = random_B(m, rng)
    h = hp(m, B, 0, 1)
    if (0, 1) not in B:
        Q, q, x, y = B | {(0, 1)}, m, 0, 1
        case = 1
    else:
        adj = adjacency(m, B)
        a, b = next(iter(adj[0] - {1})), next(iter(adj[1] - {0}))
        if a == b:                    # triangle x y a: x a y is not spanning, so hp = 0
            tests += 1; cases[3] = cases.get(3, 0) + 1
            if h != 0:
                bad += 1; print("MISMATCH triangle", m, h)
            continue
        Q, idx = relabel(B, [v for v in range(m) if v > 1])
        q, x, y = m - 2, idx[a], idx[b]
        case = 2
    adjQ = adjacency(q, Q)
    degs_ok = all(len(adjQ[v]) == (3 if v in (x, y) else 4) for v in range(q)) and x != y
    hq = hp(q, Q, x, y)
    D = Q | {E(a + q, b + q) for a, b in Q} | {E(x, x + q), E(y, y + q)}
    nd = hc_count(2 * q, D)
    tests += 1; cases[case] += 1
    if not (degs_ok and hq == h and nd == h * h):
        bad += 1
        print("MISMATCH", m, case, degs_ok, h, hq, nd)
    hist[h] = hist.get(h, 0) + 1
print(f"{tests} graphs B tested (xy not an edge: {cases[1]}, xy an edge: {cases[2]}, triangle xya: {cases.get(3, 0)})")
print("hp(B; x, y) histogram:", dict(sorted(hist.items())))
print("all checks passed" if bad == 0 else f"FAILURES: {bad}")

# (iii) => (i) of Prop. port blocks / plugs: split a vertex z of a 4-regular Hamiltonian
# graph G into u (neighbours p, c) and w (neighbours q, d), with p, q the H-neighbours of z.
# Then hp(B; u, w) = number of Hamilton cycles of G using one of zp, zc and one of zq, zd.
def ham_cycles(n, edges):
    adj = adjacency(n, edges); res = []; path = [0]; seen = {0}
    def rec():
        v = path[-1]
        if len(path) == n:
            if 0 in adj[v] and path[1] < path[-1]:
                res.append({E(path[i], path[(i + 1) % n]) for i in range(n)})
            return
        for w in adj[v]:
            if w not in seen:
                seen.add(w); path.append(w); rec(); path.pop(); seen.discard(w)
    rec(); return res

bad2 = tests2 = 0
for trial in range(200):
    n = rng.choice([7, 8, 9, 10])
    Hn = {E(i, (i + 1) % n) for i in range(n)}
    while True:                                   # random 2-factor disjoint from H
        stubs = [v for v in range(n) for _ in range(2)]; rng.shuffle(stubs)
        F0 = {E(stubs[i], stubs[i + 1]) for i in range(0, len(stubs), 2)}
        if len(F0) == n and all(a != b for a, b in F0) and not F0 & Hn:
            break
    G = Hn | F0
    z = rng.randrange(n); p, q = (z - 1) % n, (z + 1) % n
    c, d = rng.sample(sorted(b if a == z else a for a, b in F0 if z in (a, b)), 2)
    u, w = z, n                                   # u keeps the label z, w is new
    B = {e for e in G if z not in e} | {E(u, p), E(u, c), E(w, q), E(w, d)}
    lhs = hp(n + 1, B, u, w)
    rhs = sum(1 for C in ham_cycles(n, G)
              if len({E(z, p), E(z, c)} & C) == 1 and len({E(z, q), E(z, d)} & C) == 1)
    tests2 += 1
    if lhs != rhs:
        bad2 += 1; print("MISMATCH split", n, z, lhs, rhs)
print(f"(iii)=>(i): {tests2} vertex splittings tested")
print("all checks passed" if bad + bad2 == 0 else f"FAILURES: {bad + bad2}")
