import sys, json, networkx as nx
from lib import two_factors, ncyc
from merge3 import merge_move_order
res={'sin_triangulo_orden>2':0, 'con_triangulo_orden>2':0, 'orden>3':0, 'total_2f':0}
ej=[]
for line in sys.stdin:
    g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode())); n=G.number_of_nodes()
    for F in two_factors(G):
        F=set(F)
        if ncyc(n,F)==1: continue
        res['total_2f']+=1
        k=merge_move_order(F,G,n,4)
        if k is not None and k<=2: continue
        corto=min(len(c) for c in nx.connected_components(nx.Graph(list(F))))
        if k is None or k>3: res['orden>3']+=1; ej.append((g6,'orden>3',corto))
        elif corto>=4: res['sin_triangulo_orden>2']+=1; ej.append((g6,'sin triangulo',corto))
        else: res['con_triangulo_orden>2']+=1
print(json.dumps(dict(res=res, ejemplos=ej[:6])))
