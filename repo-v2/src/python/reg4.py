import sys, json, math, networkx as nx
from lib import two_factors, ncyc
from alt2 import comp_max
mx=(0,None); mw=(0,None); viol=0; tot=0
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode())); n=G.number_of_nodes()
    TF=[set(F) for F in two_factors(G)]
    Hs=[F for F in TF if ncyc(n,F)==1]
    if not Hs: continue
    tot+=1
    for F in TF:
        if ncyc(n,F)==1: continue
        d=min(len(F-h) for h in Hs); w=min(comp_max(F,h,F) for h in Hs)
        if d>mx[0]: mx=(d,g6)
        if w>mw[0]: mw=(w,g6)
        if d>math.ceil(n/2): viol+=1
print(json.dumps(dict(grafos=tot, max_D=mx[0], max_w=mw[0], techo=math.ceil(n/2), violaciones=viol, ejemplo=mx[1])))
