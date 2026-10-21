"""Build Gamma_n and Delta_n straight from Definitions 5.1 / 5.4 of the paper
(own reading, no repo code) and check every stated property."""
import subprocess, sys, itertools
import networkx as nx

HC = sys.argv[1]

def cyc_edges(seq):
    return {frozenset((seq[i], seq[(i + 1) % len(seq)])) for i in range(len(seq))}

def H_edges(n):
    return {frozenset((i, (i + 1) % n)) for i in range(n)}

def zigzag(lo, n):
    L = n - lo
    z = []
    for k in range(L):
        z.append(lo + k // 2 if k % 2 == 0 else n - 1 - k // 2)
    return z

def gamma(n):
    z = zigzag(7, n)
    return cyc_edges([1, 2, 3]) | cyc_edges([0] + z + [4, 5, 6]), z

def delta(n):
    z = zigzag(8, n)
    return cyc_edges([1, 2, 3]) | cyc_edges([5, 6, 7]) | cyc_edges([0] + z + [4]), z

def count_hc(n, E, F):
    inp = f"{n} {len(E)}\n" + "".join(f"{min(e)} {max(e)}\n" for e in E)
    inp += f"{len(F)}\n" + "".join(f"{min(e)} {max(e)}\n" for e in F)
    out = subprocess.run([HC], input=inp, capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])

def check(name, build, n, stated_S):
    F, z = build(n)
    H = H_edges(n)
    G = nx.Graph([tuple(e) for e in F])
    assert G.number_of_nodes() == n and all(d == 2 for _, d in G.degree()), "not 2-factor"
    ncyc = nx.number_connected_components(G)
    S = F & H
    E = F | H
    deg = {v: 0 for v in range(n)}
    for e in E:
        for v in e: deg[v] += 1
    prof = tuple(sum(1 for v in deg if deg[v] == d) for d in (2, 3, 4))
    hcs, ov = count_hc(n, E, F)
    mu = frozenset((z[-2], z[-1]))
    okS = S == stated_S(n, mu)
    deg2 = sorted(v for v in deg if deg[v] == 2)
    return ncyc, len(S), okS, prof, deg2, hcs, ov

bad = []
for n in range(10, 34):
    for name, build, st, d2, cyc in (
        ("Gamma", gamma, lambda n, mu: {frozenset(p) for p in [(1, 2), (2, 3), (4, 5), (5, 6)]} | {mu}, [2, 5], 2),
        ("Delta", delta, lambda n, mu: {frozenset(p) for p in [(1, 2), (2, 3), (5, 6), (6, 7)]} | {mu}, [2, 6], 3),
    ):
        ncyc, s, okS, prof, deg2, hcs, ov = check(name, build, n, st)
        good = ncyc == cyc and s == 5 and okS and prof == (2, 6, n - 8) and deg2 == d2 and hcs == 1 and ov == 5
        print(f"{name} n={n}: cycles={ncyc} s={s} S-as-stated={okS} profile={prof} deg2={deg2} #HC={hcs} ov={ov} {'OK' if good else 'MISMATCH'}")
        if not good: bad.append((name, n))
print("mismatches:", bad)

# Remark 5.6: extra class at n=12
n = 12
F = cyc_edges([1, 2, 3]) | cyc_edges([5, 6, 7]) | cyc_edges([0, 8, 10, 11, 4, 9])
H = H_edges(n)
print("Rem 5.6 n=12: S =", sorted(tuple(sorted(e)) for e in F & H), "#HC,ov =", count_hc(n, F | H, F))

# Prop 5.9 example, n=8
n = 8
F = {frozenset(p) for p in [(0, 1), (0, 2), (1, 2), (3, 4), (3, 6), (4, 7), (5, 6), (5, 7)]}
H = H_edges(n)
print("Prop 5.9 n=8: S =", sorted(tuple(sorted(e)) for e in F & H), "#HC,ov =", count_hc(n, F | H, F))

# Remark 7.13 example, n=8
F = {frozenset(p) for p in [(0, 6), (6, 5), (5, 7), (7, 0), (1, 2), (2, 4), (4, 3), (3, 1)]}
print("Rem 7.13 n=8: S =", sorted(tuple(sorted(e)) for e in F & H), "#HC,ov =", count_hc(n, F | H, F))

# Conjecture 5.8 probe: n=7, triangle 0-1-2 plus 4-cycle 3-4-5-6
n = 7
F = cyc_edges([0, 1, 2]) | cyc_edges([3, 4, 5, 6])
H = H_edges(n)
print("n=7 probe: S =", sorted(tuple(sorted(e)) for e in F & H), "#HC,ov =", count_hc(n, F | H, F))
