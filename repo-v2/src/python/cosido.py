import itertools as it, networkx as nx
from lib import two_factors, ncyc
from local import ciclos_de
def ciclos_vert(n,F):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F)
    return [sorted(c) for c in nx.connected_components(g)]
def exc_cero(G,F):
    """¿existe orden ciclico de los ciclos y aristas de corte (a_i,b_i) con b_i ~ a_{i+1}?"""
    n=G.number_of_nodes(); Cs=ciclos_de(n,F); k=len(Cs)
    if k==1: return True
    pares=[]   # por ciclo: lista de pares ordenados (a,b) adyacentes en el ciclo
    for C in Cs:
        P=[]
        for (u,v) in C: P.append((u,v)); P.append((v,u))
        pares.append(P)
    idx=list(range(1,k))
    for perm in it.permutations(idx):
        orden=[0]+list(perm)
        # programacion dinamica sobre la eleccion de pares
        posibles=[(a,b) for (a,b) in pares[orden[0]]]
        for j in range(1,k):
            nuevos=[]
            for (a0,b0) in posibles:
                for (a,b) in pares[orden[j]]:
                    if G.has_edge(b0,a): nuevos.append((a0,b))
            posibles=list(set(nuevos))
            if not posibles: break
        if any(G.has_edge(b,a0) for (a0,b) in posibles): return True
    return False
def cond_vecino(G,F,n,minimo=1):
    Cs=ciclos_vert(n,F)
    for v in range(n):
        for C in Cs:
            if v in C: continue
            if sum(1 for u in C if G.has_edge(v,u))<minimo: return False
    return True
