import sys, json, networkx as nx
from lib import two_factors, ncyc
def ciclos_de(n,F):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F)
    out=[]
    for comp in nx.connected_components(g):
        out.append(set(e for e in F if e[0] in comp and e[1] in comp))
    return out
def cumple_local(G):
    """¿para todo 2-factor existe H que corte cada ciclo C a lo sumo floor(|C|/2) veces?"""
    n=G.number_of_nodes(); TF=[set(F) for F in two_factors(G)]
    Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: return None
    peor=None
    for F in TF:
        if ncyc(n,F)==1: continue
        Cs=ciclos_de(n,F)
        ok=False
        for h in Hs:
            if all(len(C-h)<=len(C)//2 for C in Cs): ok=True; break
        if not ok:
            peor=sorted(len(C) for C in Cs)
            return False, peor
    return True, None
if __name__=='__main__':
    tot=0; fallos=[]
    for line in sys.stdin:
        g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
        r=cumple_local(G)
        if r is None: continue
        tot+=1
        if not r[0]:
            fallos.append((g6,r[1]))
            if len(fallos)<=4: print('FALLA la version local:',g6,'longitudes de ciclos',r[1],flush=True)
    print(json.dumps(dict(grafos=tot, fallos=len(fallos))))
