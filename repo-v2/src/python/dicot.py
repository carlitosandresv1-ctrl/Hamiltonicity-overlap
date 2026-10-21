import networkx as nx, itertools as it, random, sys, json
from lib import two_factors, ncyc
from maxov import max_overlap
def adyacencia_completa(G,F,n):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F)
    Cs=[set(c) for c in nx.connected_components(g)]
    for A,B in it.combinations(Cs,2):
        if not any(G.has_edge(u,v) for u in A for v in B): return False, len(Cs)
    return True, len(Cs)
rng=random.Random(int(sys.argv[1])); lim=int(sys.argv[2])
peor={}; casos=0
for t in range(lim):
    n=rng.choice([9,10,11,12])
    G=nx.gnp_random_graph(n,rng.uniform(0.25,0.5),seed=rng.randint(0,10**7))
    if not nx.is_connected(G): continue
    TF=[set(F) for F in two_factors(G)]
    rng.shuffle(TF)
    for F in TF[:8]:
        c=ncyc(n,F)
        if c==1: continue
        ok,c=adyacencia_completa(G,F,n)
        if not ok: continue
        m=max_overlap(G,F)
        if m is None: continue
        casos+=1; cor=n-m
        peor[c]=max(peor.get(c,0), cor)
print(json.dumps(dict(casos=casos, cor_max_por_c=dict(sorted(peor.items())))))
