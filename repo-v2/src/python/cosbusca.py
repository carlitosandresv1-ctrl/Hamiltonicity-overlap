import networkx as nx, random, sys, json
from lib import two_factors, ncyc
from cosido import exc_cero, cond_vecino
from maxov import max_overlap
rng=random.Random(int(sys.argv[1])); lim=int(sys.argv[2])
casos1=0; fallo1=None; casos2=0; fallo2=None
for t in range(lim):
    n=rng.choice([9,10,11,12])
    G=nx.gnp_random_graph(n,rng.uniform(0.25,0.5),seed=rng.randint(0,10**7))
    if not nx.is_connected(G): continue
    TF=[set(F) for F in two_factors(G)]
    if not any(ncyc(n,F)==1 for F in TF): continue
    for F in TF:
        c=ncyc(n,F)
        if c==1: continue
        if not cond_vecino(G,F,n,1): continue
        m=max_overlap(G,F)
        if m is None: continue
        casos1+=1
        if (n-m)!=c and fallo1 is None:
            fallo1=(nx.to_graph6_bytes(G,header=False).strip().decode(), c, n-m, cond_vecino(G,F,n,2))
print(json.dumps(dict(casos_con_condicion_V=casos1, contraejemplo=fallo1)))
