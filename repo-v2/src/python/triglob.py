import sys, json, networkx as nx
from lib import two_factors, ncyc
from local import ciclos_de
peor=0; ej=None; viol=0; casos=0
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode())); n=G.number_of_nodes()
    TF=[set(F) for F in two_factors(G)]; Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: continue
    for F in TF:
        Cs=ciclos_de(n,F)
        if len(Cs)<2 or any(len(C)!=3 for C in Cs): continue
        casos+=1
        d=min(len(F-h) for h in Hs)
        if d>peor: peor=d; ej=g6
        if d>n//2: viol+=1; print('VIOLA la cota global floor(n/2):',g6,d,flush=True)
print(json.dumps(dict(dos_factores_de_triangulos=casos, max_distancia=peor, cota=None, violaciones=viol, ejemplo=ej)))
