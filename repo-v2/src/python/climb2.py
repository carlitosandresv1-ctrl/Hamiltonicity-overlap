import networkx as nx, random, sys, json
from maxov import max_overlap
def arranque(n, tipo, rng):
    """G contiene el 2-factor F del tipo pedido, mas aristas aleatorias"""
    G=nx.Graph(); G.add_nodes_from(range(n)); F=set()
    perm=list(range(n)); rng.shuffle(perm)
    i=0; tam = 3 if tipo=='tri' else 4
    while i<n:
        k = tam if n-i>=tam else n-i
        blo=perm[i:i+k]
        for j in range(k):
            a,b=blo[j],blo[(j+1)%k]; e=(min(a,b),max(a,b)); F.add(e); G.add_edge(*e)
        i+=k
    libres=[e for e in nx.non_edges(G)]; rng.shuffle(libres)
    G.add_edges_from(libres[:rng.randint(n//2, n)])
    return G,F
def score(G,F):
    n=G.number_of_nodes()
    if not nx.is_connected(G): return None
    m=max_overlap(G,F)
    if m is None: return None
    return n-m
def run(n, tipo, seed, iters):
    rng=random.Random(seed)
    mejor=(-1,None)
    for restart in range(4):
        G,F=arranque(n,tipo,rng); cur=score(G,F)
        if cur is None: continue
        for t in range(iters):
            H=G.copy()
            noF=[e for e in H.edges() if (min(e),max(e)) not in F]
            libres=[e for e in nx.non_edges(H)]
            if rng.random()<0.6 and noF: H.remove_edge(*rng.choice(noF))
            elif libres: H.add_edge(*rng.choice(libres))
            s=score(H,F)
            if s is not None and s>=cur: G,cur=H,s
            if s is not None and s>mejor[0]:
                mejor=(s, nx.to_graph6_bytes(G,header=False).strip().decode())
    return mejor
if __name__=='__main__':
    n=int(sys.argv[1]); tipo=sys.argv[2]; seed=int(sys.argv[3]); iters=int(sys.argv[4])
    s,g6=run(n,tipo,seed,iters)
    print(json.dumps(dict(n=n,tipo=tipo,mejores_cortes=s,cota=n//2,viola=s>n//2,grafo=g6)))
