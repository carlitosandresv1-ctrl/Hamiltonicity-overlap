import sys, math, json, networkx as nx
from lib import two_factors, ncyc
def comp_max(F,H,Fset):
    D=nx.Graph(); D.add_edges_from(F^H)
    best=0
    for comp in nx.connected_components(D):
        sub=D.subgraph(comp)
        c=sum(1 for e in sub.edges() if (min(e),max(e)) in Fset)
        if c>best: best=c
    return best
def alt_width(G, cap=None, TF=None):
    n=G.number_of_nodes()
    TF=[set(F) for F in (TF if TF is not None else two_factors(G))]
    Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: return None
    cap = cap if cap is not None else math.ceil(n/2)
    worst=0
    for F in TF:
        if ncyc(n,F)==1: continue
        best=10**9
        for h in Hs:
            v=comp_max(F,h,F)
            if v<best: best=v
            if best<=cap: break           # ya cumple la cota: no hace falta seguir
        if best>worst: worst=best
    return worst
if __name__=='__main__':
    mx=-1; ex=None; viol=0; tot=0
    for line in sys.stdin:
        g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
        n=G.number_of_nodes(); w=alt_width(G)
        if w is None: continue
        tot+=1
        if w>math.ceil(n/2):
            viol+=1
            if viol<=5: print('VIOLA conj B:',g6,'anchura',w,'techo',math.ceil(n/2),flush=True)
        if w>mx: mx=w; ex=g6
    print(json.dumps(dict(grafos=tot,max_anchura=mx,ejemplo=ex,violaciones=viol)))
