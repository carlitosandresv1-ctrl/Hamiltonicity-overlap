import sys, math, json, networkx as nx
from lib import two_factors, ncyc
def components_sizes(F,H):
    D=nx.Graph(); D.add_edges_from(F^H)
    out=[]
    for comp in nx.connected_components(D):
        sub=D.subgraph(comp)
        out.append(sum(1 for e in sub.edges() if (min(e),max(e)) in F))
    return out
def alt_width(G, TF=None):
    """max_F min_H max_i l_i  (anchura alternante)"""
    n=G.number_of_nodes()
    TF=[set(F) for F in (TF if TF is not None else two_factors(G))]
    Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: return None,None
    worst=0; arg=None
    for F in TF:
        if ncyc(n,F)==1: continue
        v=min(max(components_sizes(F,h)) for h in Hs)
        if v>worst: worst=v; arg=F
    return worst, arg
if __name__=='__main__':
    mx=-1; ex=None; viol=0
    for line in sys.stdin:
        g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
        n=G.number_of_nodes()
        w,_=alt_width(G)
        if w is None: continue
        if w>math.ceil(n/2):
            viol+=1
            if viol<=3: print('VIOLA conj B:',g6,'anchura',w,'techo',math.ceil(n/2),flush=True)
        if w>mx: mx=w; ex=g6
    print(json.dumps(dict(max_anchura=mx, ejemplo=ex, violaciones=viol)))
