import sys, json, itertools, networkx as nx
exec(open('m.py').read().split('for line in sys.stdin')[0])
def ncyc(n,F):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F); return nx.number_connected_components(g)
def analyze(G, kmax=3):
    n=G.number_of_nodes()
    adjset=[set() for _ in range(n)]; adj=[0]*n
    for u,v in G.edges(): adjset[u].add(v); adjset[v].add(u); adj[u]|=1<<v; adj[v]|=1<<u
    edges=[(min(u,v),max(u,v)) for u,v in G.edges()]
    TF=list(two_factors(n,adjset,edges))
    res={'nTF':len(TF),'ham':ham(n,adj)}
    if not TF: 
        for k in range(2,kmax+1): res['M%d'%k]=False; res['Ms%d'%k]=False
        res['comp2']=0; res['b1_2']=0
        return res
    cyc=[ncyc(n,F) for F in TF]
    diff=[[len(set(TF[i])^set(TF[j])) for j in range(len(TF))] for i in range(len(TF))]
    for k in range(2,kmax+1):
        X=nx.Graph(); X.add_nodes_from(range(len(TF)))
        for i in range(len(TF)):
            for j in range(i+1,len(TF)):
                if diff[i][j]<=2*k: X.add_edge(i,j)
        comps=list(nx.connected_components(X))
        res['M%d'%k]=all(cyc[i]==1 or any(X.has_edge(i,j) and cyc[j]<cyc[i] for j in range(len(TF))) for i in range(len(TF)))
        res['Ms%d'%k]=all(any(cyc[i]==1 for i in c) for c in comps)
        if k==2:
            res['comp2']=len(comps); res['b1_2']=X.number_of_edges()-len(TF)+len(comps)
    return res
if __name__=='__main__':
    for line in sys.stdin:
        g6=line.strip(); G=nx.from_graph6_bytes(g6.encode())
        r=analyze(G); r['g']=g6; print(json.dumps(r))
