import itertools, networkx as nx

def two_factors(G):
    """Todos los 2-factores de G como conjuntos de aristas (u<v)."""
    n=G.number_of_nodes(); V=list(range(n))
    inc=[[ (min(u,v),max(u,v)) for v in G[u] ] for u in V]
    res=[]; deg=[0]*n; chosen=set()
    def rec(v):
        if v==n: res.append(frozenset(chosen)); return
        if deg[v]==2: rec(v+1); return
        need=2-deg[v]
        cand=[e for e in inc[v] if e not in chosen and deg[e[0]+e[1]-v]<2]
        for comb in itertools.combinations(cand,need):
            us=[e[0]+e[1]-v for e in comb]
            if any(deg[u]>=2 for u in us): continue
            for e,u in zip(comb,us): chosen.add(e); deg[u]+=1; deg[v]+=1
            rec(v+1)
            for e,u in zip(comb,us): chosen.discard(e); deg[u]-=1; deg[v]-=1
    rec(0); return res

def ncyc(n,F):
    g=nx.Graph(); g.add_nodes_from(range(n)); g.add_edges_from(F)
    return nx.number_connected_components(g)

def is_ham(n,F): return ncyc(n,F)==1

def kstar(G, TF=None):
    """Orden de fusión: menor k tal que toda componente de X_k contiene un 2-factor hamiltoniano."""
    n=G.number_of_nodes()
    TF=[set(F) for F in (TF if TF is not None else two_factors(G))]
    if not TF: return dict(nTF=0, nHam=0, kstar=None, dirmax=None)
    cyc=[ncyc(n,F) for F in TF]
    Hs=[F for F,c in zip(TF,cyc) if c==1]
    if not Hs: return dict(nTF=len(TF), nHam=0, kstar=None, dirmax=None)
    N=len(TF)
    D=[[len(TF[i]^TF[j])//2 for j in range(N)] for i in range(N)]
    dirmax=max((min(len(F-h) for h in Hs) for F,c in zip(TF,cyc) if c>1), default=0)
    for k in range(2,n+1):
        X=nx.Graph(); X.add_nodes_from(range(N))
        for i in range(N):
            for j in range(i+1,N):
                if D[i][j]<=k: X.add_edge(i,j)
        if all(any(cyc[i]==1 for i in comp) for comp in nx.connected_components(X)):
            return dict(nTF=N, nHam=len(Hs), kstar=k, dirmax=dirmax)
    return dict(nTF=N, nHam=len(Hs), kstar=None, dirmax=dirmax)
