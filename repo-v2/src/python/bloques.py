import networkx as nx, itertools as it
from lib import ncyc
def ciclos_y_vertices(n,F):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F)
    Cs=[]
    for comp in nx.connected_components(g):
        Cs.append((set(comp), set(e for e in F if e[0] in comp and e[1] in comp)))
    return Cs
def cota_bloques(G,F):
    """max sobre subfamilias S de ciclos mutuamente no adyacentes de |S| + max(c_W,|S|)"""
    n=G.number_of_nodes(); Cs=ciclos_y_vertices(n,F); c=len(Cs)
    if c<2: return 0
    # grafo de adyacencia entre ciclos
    A=nx.Graph(); A.add_nodes_from(range(c))
    for i,j in it.combinations(range(c),2):
        if any(G.has_edge(u,v) for u in Cs[i][0] for v in Cs[j][0]): A.add_edge(i,j)
    mejor=0
    comp=nx.complement(A)
    for cl in nx.find_cliques(comp):      # conjuntos independientes en A
        for k in range(2,len(cl)+1):
            for S in it.combinations(cl,k):
                cW=c-len(S)
                if cW==0: continue        # W debe ser no vacio
                mejor=max(mejor, len(S)+max(cW,len(S)))
    return mejor
