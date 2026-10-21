import sys, json, itertools, networkx as nx
from lib import two_factors, ncyc
def merge_move_order(F, G, n, kmax=3):
    """menor orden k<=kmax de un movimiento que reduce el numero de ciclos; None si no hay"""
    c0=ncyc(n,F); Fl=sorted(F); E=set((min(u,v),max(u,v)) for u,v in G.edges())
    for k in range(2,kmax+1):
        for rem in itertools.combinations(Fl,k):
            vs=[v for e in rem for v in e]
            if len(set(vs))<2*k: continue
            rest=set(F)-set(rem)
            # emparejamientos perfectos de los 2k extremos usando aristas de G fuera de F
            def pairings(items):
                if not items: yield []; return
                a=items[0]
                for i in range(1,len(items)):
                    b=items[i]; e=(min(a,b),max(a,b))
                    if e in E and e not in F:
                        for p in pairings(items[1:i]+items[i+1:]): yield [e]+p
            for add in pairings(vs):
                new=rest|set(add)
                if len(new)!=n: continue
                if ncyc(n,new)<c0: return k
    return None
def prop_M(G, kmax=3):
    n=G.number_of_nodes(); TF=[set(F) for F in two_factors(G)]
    if not TF: return None
    worst=0
    for F in TF:
        if ncyc(n,F)==1: continue
        k=merge_move_order(F,G,n,kmax)
        if k is None: return 99      # ningun movimiento de orden <=kmax reduce ciclos
        worst=max(worst,k)
    return worst
if __name__=='__main__':
    dist={}; bad=[]
    for line in sys.stdin:
        g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
        r=prop_M(G)
        if r is None: continue
        dist[r]=dist.get(r,0)+1
        if r==99 and len(bad)<5: bad.append(g6)
    print(json.dumps(dict(dist=dict(sorted(dist.items())), fallos=bad)))
