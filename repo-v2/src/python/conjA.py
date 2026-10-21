import sys, json, math, networkx as nx
from lib import two_factors, ncyc
def maxdist(G, cap):
    n=G.number_of_nodes(); TF=[set(F) for F in two_factors(G)]
    Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: return None
    worst=0
    for F in TF:
        if ncyc(n,F)==1: continue
        best=10**9
        for h in Hs:
            d=len(F-h)
            if d<best: best=d
            if best<=cap: break
        worst=max(worst,best)
    return worst
mx=-1; ex=None; viol=0; tot=0
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
    n=G.number_of_nodes(); cap=math.ceil(n/2)
    d=maxdist(G,cap)
    if d is None: continue
    tot+=1
    if d>cap:
        viol+=1
        if viol<=5: print('VIOLA conj A:',g6,d,cap,flush=True)
    if d>mx: mx=d; ex=g6
print(json.dumps(dict(grafos=tot,max_dist=mx,ejemplo=ex,violaciones=viol)))
