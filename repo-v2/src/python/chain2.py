import sys, math, json, itertools, networkx as nx
from lib import kstar
def chain(B,a,b,m):
    G=nx.Graph()
    for i in range(m):
        G.add_nodes_from((i,u) for u in B.nodes())
        G.add_edges_from(((i,u),(i,v)) for u,v in B.edges())
    for i in range(m): G.add_edge((i,b),((i+1)%m,a))
    return nx.convert_node_labels_to_integers(G)
res=[]
M=[int(x) for x in sys.argv[1].split(',')]
for line in sys.stdin:
    g6=line.strip(); B=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
    s=B.number_of_nodes()
    for a,b in itertools.combinations(range(s),2):
        for m in M:
            G=chain(B,a,b,m); n=G.number_of_nodes()
            if n>20: continue
            try: r=kstar(G)
            except RecursionError: continue
            if r['kstar'] is None: continue
            res.append((r['kstar']-math.ceil(n/2), r['kstar'], n, g6, a, b, r['nTF'], r['dirmax']-math.ceil(n/2)))
res.sort(reverse=True)
print(json.dumps(res[:8]))
