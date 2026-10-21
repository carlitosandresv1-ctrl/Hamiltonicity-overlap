import networkx as nx, random
from maxov import max_overlap
from lib import two_factors, ncyc
from cor2 import cor

rng = random.Random(7)
casos = 0
for t in range(400):
    n = rng.randint(7, 11)
    p = rng.uniform(0.3, 0.6)
    G = nx.gnp_random_graph(n, p, seed=rng.randint(0, 10**9))
    if not nx.is_connected(G):
        continue
    Es = set((min(u, v), max(u, v)) for u, v in G.edges())
    TF = two_factors(G)
    if not TF:
        continue
    if not any(ncyc(n, F) == 1 for F in TF):
        continue                      # no hamiltoniano
    for F in TF[: 12]:
        mo = max_overlap(G, F)
        c1 = n - mo
        c2 = cor(n, F, Es, tope=n)
        casos += 1
        assert c1 == c2, (n, sorted(F), c1, c2, nx.to_graph6_bytes(G, header=False))
print("OK", casos, "casos validados")
