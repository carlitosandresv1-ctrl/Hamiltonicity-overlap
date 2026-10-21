"""End-to-end check of the gadget-insertion lemma on random 4-regular Hamiltonian graphs.
For G = F0 u H (F0 n H = empty) and the H-edge xy = (0,1), insert gadget W:
  G' = (G - xy) + gadget(F_W u P) + {x-w0, w_{m-1}-y}.
Claim: #HC(G') = #HC(G through xy), and F' = F0 u F_W, H' = H - xy + x w0 + P + w_{m-1} y
is a 2-factor / Hamilton cycle pair with |F' n H'| = s(gadget)."""
import random, subprocess, sys
HC = sys.argv[1]
GADGETS = {
    "{2}":       (3, "01 02 12"),
    "{3}":       (4, "01 03 12 23"),
    "{1,2}":     (5, "01 02 14 23 34"),
    "{1,3}":     (6, "01 02 15 23 34 45"),
    "{1,1,2}":   (7, "01 02 14 23 36 45 56"),
    "{1,1,1,1}": (10, "01 05 18 23 26 39 45 48 67 79"),
}
def E(a, b): return (min(a, b), max(a, b))
def count(n, edges, F=()):
    inp = f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges) + f"{len(F)}\n" + "".join(f"{a} {b}\n" for a, b in F)
    c, ov = subprocess.run([HC], input=inp, capture_output=True, text=True).stdout.split()
    return int(c), int(ov)
def random_F0(n, rng):
    H = {E(i, (i + 1) % n) for i in range(n)}
    while True:
        p = list(range(n)); rng.shuffle(p)
        # random 2-factor = random cycle decomposition into cycles of length >= 3
        cuts, i = [], 0
        while i < n:
            L = rng.randint(3, max(3, n - i)) if n - i >= 6 else n - i
            cuts.append(p[i:i + L]); i += L
        if any(len(c) < 3 for c in cuts): continue
        F = {E(c[j], c[(j + 1) % len(c)]) for c in cuts for j in range(len(c))}
        if len(F) == n and not (F & H): return F, H
rng = random.Random(1)
bad = 0; tests = 0
for trial in range(60):
    n = rng.choice([9, 10, 11, 12])
    F0, H = random_F0(n, rng)
    G = F0 | H
    x, y = 0, 1
    # HCs of G through xy: subdivide xy with vertex z=n
    sub = (G - {E(x, y)}) | {E(x, n), E(y, n)}
    through, _ = count(n + 1, sorted(sub))
    for name, (m, fs) in GADGETS.items():
        W = {i: n + i for i in range(m)}
        FW = {E(W[int(t[0])], W[int(t[1])]) for t in fs.split()}
        P = {E(W[i], W[i + 1]) for i in range(m - 1)}
        Hn = (H - {E(x, y)}) | P | {E(x, W[0]), E(W[m - 1], y)}
        Fn = F0 | FW
        Gn = Fn | Hn
        N = n + m
        deg = [0] * N
        for a, b in Fn: deg[a] += 1; deg[b] += 1
        assert all(d == 2 for d in deg), "F' not 2-factor"
        hc_count, ov = count(N, sorted(Gn), sorted(Fn))
        s = len(Fn & Hn)
        exp_s = sum(int(c) for c in name.strip("{}").split(","))
        tests += 1
        ok = hc_count == through and s == exp_s
        if not ok:
            bad += 1; print("MISMATCH", n, name, hc_count, through, s)
print(f"{tests} insertions tested, mismatches: {bad}")
