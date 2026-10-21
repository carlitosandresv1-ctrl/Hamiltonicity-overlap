import networkx as nx, random, sys, json
from lib import two_factors, ncyc
from cosido import cond_vecino
from maxov import max_overlap
rng=random.Random(int(sys.argv[1])); lim=int(sys.argv[2])
casos=0; fallo=None
for t in range(lim):
    n=rng.choice([9,10,11,12])
    G=nx.gnp_random_graph(n,rng.uniform(0.3,0.55),seed=rng.randint(0,10**7))
    if not nx.is_connected(G): continue
    TF=[set(F) for F in two_factors(G)]
    for F in TF:
        c=ncyc(n,F)
        if c==1: continue
        if not cond_vecino(G,F,n,2): continue
        m=max_overlap(G,F)
        if m is None: continue
        casos+=1
        if (n-m)!=c and fallo is None:
            fallo=(nx.to_graph6_bytes(G,header=False).strip().decode(), c, n-m)
print(json.dumps(dict(casos_con_V2=casos, contraejemplo=fallo)))
