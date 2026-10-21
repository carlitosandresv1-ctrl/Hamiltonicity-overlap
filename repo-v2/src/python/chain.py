import sys, math, json, itertools, networkx as nx
from lib import two_factors, kstar

def chain(B, a, b, m):
    """m copias de B en ciclo, uniendo b_i con a_{i+1}."""
    G=nx.Graph()
    for i in range(m):
        for u,v in B.edges(): G.add_edge((i,u),(i,v))
        for u in B.nodes(): G.add_node((i,u))
    for i in range(m): G.add_edge((i,b),((i+1)%m,a))
    return nx.convert_node_labels_to_integers(G)

best=[]
for line in sys.stdin:
    g6=line.strip(); B=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
    s=B.number_of_nodes()
    for a,b in itertools.permutations(range(s),2):
        if B.degree(a)>3 or B.degree(b)>3: continue
        m=3
        G=chain(B,a,b,m); n=G.number_of_nodes()
        if max(d for _,d in G.degree())>4: continue
        r=kstar(G)
        if r['kstar'] is None: continue
        margen=r['kstar']-math.ceil(n/2)
        if margen>=0:
            best.append((margen, r['kstar'], n, g6, a, b, r['nTF'], r['dirmax']))
best.sort(reverse=True)
print(json.dumps(best[:10]))
