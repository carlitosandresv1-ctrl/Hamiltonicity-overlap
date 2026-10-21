import sys, json, itertools, networkx as nx
from lib import two_factors, ncyc
def neighbors_k(F, E, n, k=2):
    """2-factores alcanzables desde F con un movimiento de orden exactamente <=k"""
    out=set(); Fl=sorted(F)
    for r in range(2,k+1):
        for rem in itertools.combinations(Fl,r):
            vs=[v for e in rem for v in e]
            if len(set(vs))<2*r: continue
            rest=frozenset(F)-set(rem)
            def pair(items):
                if not items: yield []; return
                a=items[0]
                for i in range(1,len(items)):
                    b=items[i]; e=(min(a,b),max(a,b))
                    if e in E and e not in F:
                        for p in pair(items[1:i]+items[i+1:]): yield [e]+p
            for add in pair(vs):
                new=rest|frozenset(add)
                if len(new)==n: out.add(frozenset(new))
    return out
def kstar_le(G, k=2):
    """True si (M*_k) se cumple: toda componente de X_k contiene un 2-factor hamiltoniano"""
    n=G.number_of_nodes(); E=set((min(u,v),max(u,v)) for u,v in G.edges())
    TF=[frozenset(F) for F in two_factors(G)]
    if not TF: return None
    idx={F:i for i,F in enumerate(TF)}
    par=list(range(len(TF)))
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for F in TF:
        for F2 in neighbors_k(set(F),E,n,k):
            if F2 in idx:
                a,b=find(idx[F]),find(idx[F2])
                if a!=b: par[a]=b
    ham={find(idx[F]) for F in TF if ncyc(n,F)==1}
    return all(find(i) in ham for i in range(len(TF)))
if __name__=='__main__':
    ok=0; bad=[]
    for line in sys.stdin:
        g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
        r=kstar_le(G,2)
        if r is None: continue
        if r: ok+=1
        else: bad.append(g6)
    print(json.dumps(dict(con_kstar_2=ok, con_kstar_mayor=len(bad), ejemplos=bad[:5])))
