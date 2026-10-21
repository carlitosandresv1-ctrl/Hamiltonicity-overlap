import sys, json, networkx as nx
def perfect_matchings(n, adjl):
    res=[]; used=[False]*n; cur=[]
    def rec(cnt):
        if cnt==n: res.append(frozenset(cur)); return
        v=0
        while used[v]: v+=1
        used[v]=True
        for u in adjl[v]:
            if not used[u]:
                used[u]=True; cur.append((min(u,v),max(u,v)))
                rec(cnt+2)
                cur.pop(); used[u]=False
        used[v]=False
    rec(0); return res
def single_cycle(n, F):
    # F is a 2-factor as edge set; check connected
    adj={i:[] for i in range(n)}
    for u,v in F: adj[u].append(v); adj[v].append(u)
    seen={0}; st=[0]
    while st:
        x=st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen)==n
class DSU:
    def __init__(s,n): s.p=list(range(n))
    def f(s,x):
        while s.p[x]!=x: s.p[x]=s.p[s.p[x]]; x=s.p[x]
        return x
    def u(s,a,b):
        a,b=s.f(a),s.f(b)
        if a!=b: s.p[a]=b; return True
        return False
def kstar_cubic(G):
    n=G.number_of_nodes(); adjl=[list(G[v]) for v in range(n)]
    E=set((min(u,v),max(u,v)) for u,v in G.edges())
    PMs=perfect_matchings(n,adjl)
    TF=[frozenset(E-set(M)) for M in PMs]
    if not TF: return None,0,0
    isham=[single_cycle(n,F) for F in TF]
    if not any(isham): return None,len(TF),0   # no hamiltoniano
    N=len(TF)
    pairs=[]
    for i in range(N):
        for j in range(i+1,N):
            pairs.append((len(TF[i]^TF[j])//2,i,j))
    pairs.sort()
    d=DSU(N); hamcomp=[isham[i] for i in range(N)]
    # merge; track whether each component contains a ham
    need=sum(1 for i in range(N) if not isham[i])
    # component root -> has ham
    has={i:isham[i] for i in range(N)}
    def ok():
        roots={}
        for i in range(N): roots.setdefault(d.f(i),False)
        for i in range(N):
            if isham[i]: roots[d.f(i)]=True
        return all(roots.values())
    if ok(): return 2,N,sum(isham)
    k=None
    idx=0
    while idx<len(pairs):
        w=pairs[idx][0]
        while idx<len(pairs) and pairs[idx][0]==w:
            _,i,j=pairs[idx]; d.u(i,j); idx+=1
        if ok(): k=max(w,2); break
    return k,N,sum(isham)
if __name__=='__main__':
    best=0; worst=None; cnt=0; dist={}
    for line in sys.stdin:
        g6=line.strip(); G=nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
        k,N,h=kstar_cubic(G)
        if k is None: continue
        cnt+=1; dist[k]=dist.get(k,0)+1
        if k>best: best=k; worst=(g6,N,h)
    print(json.dumps(dict(ham_graphs=cnt,dist=dict(sorted(dist.items())),max_kstar=best,worst=worst)))
