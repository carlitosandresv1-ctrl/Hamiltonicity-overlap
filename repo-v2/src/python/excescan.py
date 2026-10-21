import sys, json, networkx as nx
from lib import two_factors, ncyc
from cosido import exc_cero
tot=0; mal=[]
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode())); n=G.number_of_nodes()
    TF=[set(F) for F in two_factors(G)]
    if not any(ncyc(n,F)==1 for F in TF): continue
    tot+=1
    for F in TF:
        if ncyc(n,F)==1: continue
        if not exc_cero(G,F):
            mal.append(g6); break
print(json.dumps(dict(grafos=tot, con_exceso_positivo=len(set(mal)), ejemplos=sorted(set(mal))[:5])))
