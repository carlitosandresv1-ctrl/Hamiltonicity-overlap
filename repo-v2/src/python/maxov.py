import networkx as nx
def max_overlap(G, F):
    """max_H |F ∩ H| sobre ciclos hamiltonianos H, por programacion dinamica sobre subconjuntos"""
    n=G.number_of_nodes()
    W=[[-1]*n for _ in range(n)]
    for u,v in G.edges():
        w=1 if (min(u,v),max(u,v)) in F else 0
        W[u][v]=w; W[v][u]=w
    NEG=-10**6
    full=(1<<n)-1
    dp=[[NEG]*n for _ in range(1<<n)]
    dp[1][0]=0
    for mask in range(1,1<<n):
        if not (mask&1): continue
        row=dp[mask]
        for v in range(n):
            cur=row[v]
            if cur<0 and not (mask==1 and v==0): continue
            if cur==NEG: continue
            Wv=W[v]
            for u in range(1,n):
                if mask>>u&1 or Wv[u]<0: continue
                nm=mask|(1<<u)
                val=cur+Wv[u]
                if val>dp[nm][u]: dp[nm][u]=val
    best=None
    for v in range(1,n):
        if W[v][0]>=0 and dp[full][v]>NEG:
            tot=dp[full][v]+W[v][0]
            if best is None or tot>best: best=tot
    return best
