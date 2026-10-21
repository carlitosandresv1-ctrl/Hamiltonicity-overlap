import sys, json, networkx as nx
exec(open('m.py').read().split('for line in sys.stdin')[0])
def ncyc(n,F):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F); return nx.number_connected_components(g)
def kstar(G):
    n=G.number_of_nodes()
    adjset=[set() for _ in range(n)]; adj=[0]*n
    for u,v in G.edges(): adjset[u].add(v); adjset[v].add(u); adj[u]|=1<<v; adj[v]|=1<<u
    edges=[(min(u,v),max(u,v)) for u,v in G.edges()]
    TF=[set(F) for F in two_factors(n,adjset,edges)]
    h=ham(n,adj)
    if not TF: return dict(nTF=0,ham=h,kstar=None,cmax=None)
    cyc=[ncyc(n,F) for F in TF]
    N=len(TF)
    D=[[len(TF[i]^TF[j]) for j in range(N)] for i in range(N)]
    best=None
    for k in range(2,n+1):
        X=nx.Graph(); X.add_nodes_from(range(N))
        for i in range(N):
            for j in range(i+1,N):
                if D[i][j]<=2*k: X.add_edge(i,j)
        if all(any(cyc[i]==1 for i in c) for c in nx.connected_components(X)):
            best=k; break
    return dict(nTF=N,ham=h,kstar=best,cmax=max(cyc))
if __name__=='__main__':
    for line in sys.stdin:
        g6=line.strip(); r=kstar(nx.from_graph6_bytes(g6.encode())); r['g']=g6; print(json.dumps(r))
