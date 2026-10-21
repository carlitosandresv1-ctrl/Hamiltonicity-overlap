import sys, json, math, networkx as nx
from lib import two_factors, ncyc
peor=0; ej=None; viol=0; tot=0
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode())); n=G.number_of_nodes()
    d=min(x for _,x in G.degree())
    if d<3: continue
    cap=math.ceil(n/(d-1))
    TF=[set(F) for F in two_factors(G)]
    Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: continue
    tot+=1; D=0
    for F in TF:
        if ncyc(n,F)==1: continue
        best=10**9
        for h in Hs:
            v=len(F-h)
            if v<best: best=v
            if best<=cap: break
        D=max(D,best)
    if D>cap:
        viol+=1
        if viol<=4: print('VIOLA D<=ceil(n/(delta-1)):',g6,'D=',D,'cota=',cap,'delta=',d,flush=True)
    if D-cap>peor-0: peor=max(peor,D-cap)
print(json.dumps(dict(grafos=tot, violaciones=viol, exceso_max=peor)))
