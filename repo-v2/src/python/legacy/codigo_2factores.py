import sys, json, itertools, networkx as nx
exec(open('m.py').read().split('for line in sys.stdin')[0])
def ncyc(n,F):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F); return nx.number_connected_components(g)
def neighbors2opt(F, adjset, n):
    out=set(); Fl=list(F)
    for e1,e2 in itertools.combinations(Fl,2):
        a,b=e1; c,d=e2
        if len({a,b,c,d})<4: continue
        for (x,y),(z,w) in [((a,c),(b,d)),((a,d),(b,c))]:
            p=(min(x,y),max(x,y)); q=(min(z,w),max(z,w))
            if y in adjset[x] and w in adjset[z] and p not in F and q not in F:
                out.add(frozenset((F-{e1,e2})|{p,q}))
    return out
for line in sys.stdin:
    g6=line.strip(); G=nx.from_graph6_bytes(g6.encode()); n=G.number_of_nodes()
    adjset=[set() for _ in range(n)]; adj=[0]*n
    for u,v in G.edges(): adjset[u].add(v); adjset[v].add(u); adj[u]|=1<<v; adj[v]|=1<<u
    edges=[(min(u,v),max(u,v)) for u,v in G.edges()]
    TF=two_factors(n,adjset,edges)
    h=ham(n,adj)
    if not TF: print(json.dumps(dict(g=g6,n=n,ham=h,nTF=0,M=False,Mstar=False))); continue
    # build exchange graph components
    X=nx.Graph(); X.add_nodes_from(TF)
    for F in TF:
        for F2 in neighbors2opt(set(F),adjset,n):
            if F2 in TF: X.add_edge(F,F2)
    Mstar=all(any(ncyc(n,F)==1 for F in comp) for comp in nx.connected_components(X))
    M=all(can_merge(set(F),adjset,n) for F in TF)
    print(json.dumps(dict(g=g6,n=n,ham=h,nTF=len(TF),M=M,Mstar=Mstar)))
