import networkx as nx, random, math, sys, json
from maxov import max_overlap
from lib import two_factors, ncyc
rng=random.Random(int(sys.argv[1])); lim=int(sys.argv[2])
peor=0; casos=0; arg=None
for t in range(lim):
    n=rng.choice([10,11,12]); d=math.ceil(n/2)
    G=nx.gnp_random_graph(n,0.45,seed=rng.randint(0,10**7))
    libres=[e for e in nx.non_edges(G)]; rng.shuffle(libres)
    for e in libres:
        if min(x for _,x in G.degree())>=d: break
        if G.degree(e[0])<d or G.degree(e[1])<d: G.add_edge(*e)
    if min(x for _,x in G.degree())<d or not nx.is_connected(G): continue
    TF=[set(F) for F in two_factors(G)]
    nh=[F for F in TF if ncyc(n,F)>1]
    if not nh: continue
    rng.shuffle(nh)
    for F in nh[:6]:
        m=max_overlap(G,F)
        if m is None: continue
        casos+=1; ex=(n-m)-ncyc(n,F)
        if ex>peor: peor=ex; arg=(nx.to_graph6_bytes(G,header=False).strip().decode(), ncyc(n,F), n-m)
print(json.dumps(dict(dos_factores=casos, exceso_max=peor, ejemplo=arg)))
