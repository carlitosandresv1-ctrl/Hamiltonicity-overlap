import sys, json, networkx as nx
from lib import two_factors, ncyc
peor=0; ej=None; dist={}
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode())); n=G.number_of_nodes()
    TF=[set(F) for F in two_factors(G)]; Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: continue
    for F in TF:
        c=ncyc(n,F)
        if c==1: continue
        d=min(len(F-h) for h in Hs)
        dist[d]=dist.get(d,0)+1
        if d>peor: peor=d; ej=(g6,c)
print(json.dumps(dict(cortes=dict(sorted(dist.items())), peor=peor, ejemplo=ej)))
