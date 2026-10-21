"""Check the counting identities behind the 'doubling' constructions on random unions
Gamma = F u H (H = 0..n-1).  A *plug* is a graph Q with two vertices x,y of degree 3 and
all others of degree 4.  Doubling: two disjoint copies of Q plus edges x1x2, y1y2.
Claim: the result is 4-regular and #HC(double) = (#Hamilton x-y paths of Q)^2.

Constructions tested:
  (A) s = 1, S = {uv}:                 Q = Gamma,              x,y = u,v
      expected #HP(Q,u->v) = #HC(Gamma) containing uv
  (B) s = 2, stretch a-b-c, ac not edge: Q = Gamma - b + ac,  x,y = a,c
      expected #HP = #HC(Gamma)  (every HC contains a-b-c)
  (C) s = 2, stretch a-b-c, F-triangle abc: Q = Gamma - {a,b,c}, x,y = a-, c+
      expected #HP = #HC(Gamma)
"""
import random, subprocess, sys
HC = sys.argv[1]
def E(a, b): return (min(a, b), max(a, b))
def count(n, edges, F=()):
    inp = f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges) + f"{len(F)}\n" + "".join(f"{a} {b}\n" for a, b in F)
    c, ov = subprocess.run([HC], input=inp, capture_output=True, text=True).stdout.split()
    return int(c)
def rand_F(n, rng):
    p = list(range(n)); rng.shuffle(p); cyc = []; i = 0
    while i < n:
        L = n - i if n - i < 6 else rng.randint(3, n - i - 3) if rng.random() < .6 else n - i
        cyc.append(p[i:i + L]); i += L
    return {E(c[j], c[(j + 1) % len(c)]) for c in cyc for j in range(len(c))}
def relabel(edges):
    vs = sorted({v for e in edges for v in e}); idx = {v: i for i, v in enumerate(vs)}
    return len(vs), {E(idx[a], idx[b]) for a, b in edges}, idx
def double(Q, x, y):
    N, Qr, idx = relabel(Q)
    x, y = idx[x], idx[y]
    D = Qr | {E(a + N, b + N) for a, b in Qr} | {E(x, x + N), E(y, y + N)}
    deg = [0] * (2 * N)
    for a, b in D: deg[a] += 1; deg[b] += 1
    assert all(d == 4 for d in deg), deg
    return count(2 * N, sorted(D))
def hp_count(Q, x, y):
    # Hamilton x-y paths of Q = HCs of Q - xy + path x-z-y
    N, Qr, idx = relabel(Q)
    x, y = idx[x], idx[y]
    return count(N + 1, sorted((Qr - {E(x, y)}) | {E(x, N), E(y, N)}))
rng = random.Random(3)
stats = {"A": [0, 0], "B": [0, 0], "C": [0, 0]}
for trial in range(4000):
    n = rng.randint(7, 11)
    H = {E(i, (i + 1) % n) for i in range(n)}
    F = rand_F(n, rng)
    if len(F) != n: continue
    S = F & H; G = F | H
    if len(S) == 1:
        (u, v), = S
        hcuv = count(n + 1, sorted((G - {E(u, v)}) | {E(u, n), E(v, n)}))
        if hcuv == 0: continue
        got = double(G, u, v); stats["A"][0] += 1; stats["A"][1] += got != hcuv ** 2
    elif len(S) == 2:
        e1, e2 = sorted(S); common = set(e1) & set(e2)
        if not common: continue
        b, = common; a = (set(e1) - {b}).pop(); c = (set(e2) - {b}).pop()
        if a == (b + 1) % n: a, c = c, a           # orient a = b-1, c = b+1
        tot = count(n, sorted(G))
        if tot == 0: continue
        if E(a, c) not in G:
            Q = (G - {E(a, b), E(b, c)}) | {E(a, c)}
            if hp_count(Q, a, c) != tot: stats["B"][1] += 1
            got = double(Q, a, c); stats["B"][0] += 1; stats["B"][1] += got != tot ** 2
        elif E(a, c) in F:
            am, cp = (a - 1) % n, (c + 1) % n
            Q = {e for e in G if not (set(e) & {a, b, c})}
            got = double(Q, am, cp); stats["C"][0] += 1; stats["C"][1] += got != tot ** 2
print({k: f"{t} tests, {bad} mismatches" for k, (t, bad) in stats.items()})
