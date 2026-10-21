import sys, json, networkx as nx
from lib import two_factors, ncyc
from merge3 import merge_move_order
res={}; ex=[]
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
    n=G.number_of_nodes(); d=min(dict(G.degree()).values())
    peor=0; fail=False
    for F in two_factors(G):
        F=set(F)
        if ncyc(n,F)==1: continue
        k=merge_move_order(F,G,n,4)
        if k is None: fail=True; break
        peor=max(peor,k)
    key=99 if fail else peor
    res[key]=res.get(key,0)+1
    if key>=3: ex.append((g6,n,d,G.number_of_edges(),key))
print(json.dumps(dict(dist=dict(sorted(res.items())), ejemplos=ex[:12])))
